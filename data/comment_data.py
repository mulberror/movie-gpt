import csv
import pymysql as mysql

host = 'localhost'
port = 3306
user = 'root'
password = 'root'
database = 'movie_system'
charset = 'utf8mb4'

con = mysql.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=database,
    charset=charset
)

print('Connected to MySQL')
cursor = con.cursor()
print('Create sql cursor successfully')

def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def comment_data_process():
    comments = []
    error_cnt = 0
    short_comment_cnt = 0
    total_comment_cnt = 4205656
    now_count = 0
    ls = []
    now = 0
    with open('./comment.csv', 'r', encoding='utf-8') as file:
        print("Open comment.csv successfully")
        csv_reader = csv.reader(file)
        for row in csv_reader:
            user_id, comment, movie_id = row
            now_count += 1
            if now_count / total_comment_cnt * 100 > now:
                now += 1
                print('now at {:.2f}%'.format(now_count / total_comment_cnt * 100))
            if not user_id or not comment or not movie_id or not is_integer(movie_id):
                error_cnt += 1
                continue
            if len(comment) < 2:
                short_comment_cnt += 1
                continue
            # movie_id = int(movie_id)
            # if movie_id not in ls:
            #     sql = "SELECT * FROM movies WHERE id = %s"
            #     cursor.execute(sql, (int(movie_id),))
            #     movie = cursor.fetchone()
            #     if not movie:
            #         error_cnt += 1
            #         continue
            #     ls.append(movie_id)

            comments.append(row)

    print('Total comments: %d' % total_comment_cnt)
    print('Error Data:', error_cnt)
    print('Short Comment:', short_comment_cnt)

    with open('./comment.csv', 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['user_name', 'comment', 'movie_id'])
        csv_writer.writerows(comments)