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


def relation_data_process():
    relationships = []

    with open('./relationships.csv', 'r', encoding='utf-8') as file:
        print("Open relationships.csv successfully")
        csv_reader = csv.reader(file)
        next(csv_reader)  # 跳过标题行

        for row in csv_reader:
            movie_id, person_id, role = row

            if not movie_id or not person_id or not role:
                raise ValueError("There is something lose in relationships.csv")

            movie_id = int(movie_id)
            person_id = int(person_id)
            if role == 'author':
                role = 0
            elif role == 'director':
                role = 1
            elif role == 'actor':
                role = 2
            else:
                return ValueError("There is role not in (author, director, actor)")
            relationships.append((movie_id, person_id, role))

    print(len(relationships))

    cursor = con.cursor()

    count = 0
    for movie_id, person_id, role in relationships:
        sql = "INSERT INTO relationships (movie_id, person_id, role) VALUES (%s, %s, %s)"
        values = (int(movie_id), int(person_id), int(role))
        try:
            cursor.execute(sql, values)
            con.commit()
        except mysql.Error as e:
            print(f"插入数据时发生错误: {e}")
            con.rollback()

        count = count + 1
        print(1.0 * count / len(relationships) * 100.0)

    return relationships