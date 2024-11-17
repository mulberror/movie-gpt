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


def login(username, pwd):
    try:
        with con.cursor() as cur:
            cur.execute('select * from user where username = %s', (username,))
            result = cur.fetchone()
            if result is None:
                return None, "未找到该用户"
            user_id, user_name, user_password = result
            if pwd == user_password:
                return user_id, "登录成功"
            else:
                return None, "登录密码错误"
    except mysql.MySQLError as e:
        return f"Database error: {e}"  # 数据库连接或查询失败时返回错误信息
    finally:
        cur.close()
