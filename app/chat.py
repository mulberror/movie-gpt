import pymysql as mysql
import json

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


def chat_list(user_id: int):
    try:
        with con.cursor() as cur:
            sql = "select chat_id from chat_history where user_id = %s"
            cur.execute(sql, (user_id,))
            result = cur.fetchall()
            ls = []
            for row in result:
                ls.append(row[0])
            return ls
    except mysql.MySQLError as e:
        return f"Database error: {e}"  # 数据库连接或查询失败时返回错误信息
    finally:
        cur.close()


def chat_content(chat_id: int):
    try:
        with con.cursor() as cur:
            sql = "select content, respond from chat_history where chat_id = %s"
            cur.execute(sql, (chat_id,))
            content, respond = cur.fetchone()
            return content, respond
    except mysql.MySQLError as e:
        return f"Database error: {e}"  # 数据库连接或查询失败时返回错误信息
    finally:
        cur.close()


def update_content(chat_id, content_j: json, respond_j: json):
    try:
        with con.cursor() as cur:
            sql = "update chat_history set content = %s, respond = %s where chat_id = %s"
            cur.execute(sql, (content_j, respond_j, chat_id,))
            con.commit()
            return True
    except mysql.MySQLError as e:
        return f"Database error: {e}"
    finally:
        cur.close()


def ask(content):
    return '你好'

def chat_ask(chat_id: int, content_s: str):
    try:
        content, respond = chat_content(chat_id)
        content_data = json.loads(content)
        respond_data = json.loads(respond)
        n = len(content_data)
        ask_content = ""
        for _, content in content_data.items():
            ask_content += content + ','
        ask_content += content_s
        print('DEBUG:', ask_content)
        respond_content = ask(ask_content)

        content_data[n] = content_s
        respond_data[n] = respond_content

        sql_input_0 = json.dumps(content_data)
        sql_input_1 = json.dumps(respond_data)
        update_content(chat_id, sql_input_0, sql_input_1)

        return respond_content
    except mysql.MySQLError as e:
        return f"Database error: {e}"


if __name__ == '__main__':
    a = {0: '你好', 1: '我想询问一些关于电影的问题'}
    b = {0: '你好', 1: '好的，您请问'}
    a = json.dumps(a)
    b = json.dumps(b)
    update_content(1, a, b)
