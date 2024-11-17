# coding = utf-8

import csv
import random

import pymysql
import math
from operator import itemgetter


class UserBasedCF():
    # 初始化相关参数
    def __init__(self):
        # 找到与目标用户兴趣相似的3个用户，为其推荐5个商品
        self.n_sim_user = 3
        self.n_rec_product = 5

        self.dataSet = {}

        # 将数据集划分为训练集和测试集
        self.trainSet = {}
        self.testSet = {}

        # 用户相似度矩阵
        self.user_sim_matrix = {}
        self.product_count = 0

        print('Similar user number = %d' % self.n_sim_user)
        print('Recommneded product number = %d' % self.n_rec_product)

    # 读文件得到“用户-商品”数据
    def get_dataset(self, filename, pivot=0.75):
        dataSet_len = 0
        trainSet_len = 0
        testSet_len = 0
        for line in self.load_file(filename):
            user, product, rating = line.split(',')
            # if random.random() < pivot:
            self.dataSet.setdefault(user, {})
            self.dataSet[user][product] = rating
            dataSet_len += 1
            if (random.random() < pivot):
                self.trainSet.setdefault(user, {})
                self.trainSet[user][product] = rating
                trainSet_len += 1
            else:
                self.testSet.setdefault(user, {})
                self.testSet[user][product] = rating
                testSet_len += 1
        print('Split trainingSet and testSet success!')
        print('dataSet = %s' % dataSet_len)
        print('TrainSet = %s' % trainSet_len)
        print('TestSet = %s' % testSet_len)

    # 读文件，返回文件的每一行
    def load_file(self, filename):
        with open(filename, 'r') as f:
            for i, line in enumerate(f):
                if i == 0:  # 去掉文件第一行的title
                    continue
                yield line.strip('\r\n')
        print('Load %s success!' % filename)

    # 计算用户之间的相似度
    def calc_user_sim(self):
        # 构建“商品-用户”倒排索引
        # key = productID, value = list of userIDs who have seen this product
        print('Building product-user table ...')
        product_user = {}
        for user, products in self.trainSet.items():
            for product in products:
                if product not in product_user:
                    product_user[product] = set()
                product_user[product].add(user)
        print('Build product-user table success!')

        self.product_count = len(product_user)
        print('Total product number = %d' % self.product_count)

        print('Build user co-rated products matrix ...')
        for product, users in product_user.items():
            for u in users:
                for v in users:
                    if u == v:
                        continue
                    self.user_sim_matrix.setdefault(u, {})
                    self.user_sim_matrix[u].setdefault(v, 0)
                    self.user_sim_matrix[u][v] += 1
        print('Build user co-rated products matrix success!')

        # 计算相似性
        print('Calculating user similarity matrix ...')
        for u, related_users in self.user_sim_matrix.items():
            for v, count in related_users.items():
                self.user_sim_matrix[u][v] = count / math.sqrt(len(self.trainSet[u]) * len(self.trainSet[v]))
        print('Calculate user similarity matrix success!')

    # 针对目标用户U，结合用户需求文本，产生N个推荐
    def recommend(self, user, text):
        K = self.n_sim_user
        N = self.n_rec_product
        rank = {}
        watched_products = self.trainSet[user]
        text_products = self.testSet[text]

        # v=similar user, wuv=similar factor
        for v, wuv in sorted(self.user_sim_matrix[user].items(), key=itemgetter(1), reverse=True)[0:K]:
            for product in self.trainSet[v]:
                if product in watched_products:
                    continue
                rank.setdefault(product, 0)
                rank[product] += self.evaluate(wuv, text_products)
        return sorted(rank.items(), key=itemgetter(1), reverse=True)[0:N]

    # 产生推荐并通过准确率、召回率和覆盖率进行评估
    def evaluate(self, text, text_products):
        # print("Evaluation start ...")
        N = self.n_rec_product
        # 准确率和召回率
        hit = 0
        rec_count = 0
        test_count = 0
        # 覆盖率
        all_rec_products = set()

        # 打开数据库连接
        db = pymysql.connect(host='localhost', user='root', password='123456', database='movies', charset='utf8')
        cursor = db.cursor()
        # 使用 execute()  方法执行 SQL 查询
        sql1 = "truncate table rec;"
        cursor.execute(sql1)
        db.commit()
        sql = "insert into rec(user_id,movie_id,rating ) values (%s,%s,%s)"

        for i, user, in enumerate(self.trainSet):
            test_moives = self.testSet.get(user, {})
            rec_products = self.recommend(user)
            print(user, rec_products)
            for item in rec_products:
                data = (user, item[0], item[1])
                if item[0] in test_moives:
                    hit += 1
                cursor.execute(sql, data)
            rec_count += N
            test_count += len(test_moives)
            db.commit()
            # rec_products 是推荐后的数据
            # 把user-rec-rating 存到数据库
        cursor.close()
        db.close()

        precision = hit / (1.0 * rec_count)
        recall = hit / (1.0 * test_count)
        coverage = len(all_rec_products) / (1.0 * self.product_count)
        print('precisioin=%.4f\trecall=%.4f\tcoverage=%.4f' % (precision, recall, coverage))

