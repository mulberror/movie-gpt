# 导入 csv 文件
import csv
import pymysql as mysql
import relation_data as rd
import comment_data as cd
import person_data as pd

import request
import json

print('0 for relation data process\n1 for comments data process\n2 for person data process\n')

s = int(input())
if s == 0:
    rd.relation_data_process()
elif s == 1:
    cd.comment_data_process()
elif s == 2:
    pd.person_data_process()