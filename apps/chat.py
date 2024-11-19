import pymysql as mysql
import json
import apps.ask.model as mod

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


def new_chat(user_id):
    try:
        with con.cursor() as cur:
            sql = "insert into chat_history(user_id, content, respond) values (%s, %s, %s)"
            json_empty = {"0": ""}
            obj = json.dumps(json_empty)
            cur.execute(sql, (user_id, obj, obj))
            con.commit()
            sql = "select chat_id from chat_history where user_id = %s order by chat_id desc"
            cur.execute(sql, (user_id,))
            result = cur.fetchall()
            chat_id = result[0][0]
            return chat_id
    except mysql.MySQLError as e:
        return f"Database error: {e}"
    finally:
        cur.close()


def chat_ask(chat_id: int, content_s: str):
    try:
        content, respond = chat_content(chat_id)
        content_data = json.loads(content)
        respond_data = json.loads(respond)
        n = len(content_data)
        ask_content = "该部分为上文问题{"
        for _, content in content_data.items():
            ask_content += content + ';'
        ask_content += "},以下为上文回答{"
        for _, respond in respond_data.items():
            ask_content += respond + ';'
        ask_content += ('},要求:{结果不要出现*,每一个条目单独一行,如果问电影就要包括名称,年份,豆瓣评分,导演,演员和梗概等;'
                        '或者问影人就要包括名称,出生日期,出生地点,作品等;如果该问题与电影无关,回复"不好意思，该问题与电影无关"')
        ask_content += "},真正需要回答的问题:{"
        ask_content += content_s + '}:'
        print('DEBUG:', ask_content)
        respond_content = mod.ask(ask_content)

        content_data[n] = content_s
        respond_data[n] = respond_content

        sql_input_0 = json.dumps(content_data)
        sql_input_1 = json.dumps(respond_data)
        update_content(chat_id, sql_input_0, sql_input_1)
        print(respond_content)

        return respond_content
    except mysql.MySQLError as e:
        return f"Database error: {e}"


if __name__ == '__main__':
    a = {0: '你好', 1: '我想询问一些关于电影的问题'}
    b = {0: '你好', 1: '好的，您请问'}
    a = json.dumps(a)
    b = json.dumps(b)
    update_content(1, a, b)
