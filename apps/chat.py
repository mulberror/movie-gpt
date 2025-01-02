import pymysql as mysql
import json
import apps.ask.model as mod

host = '121.36.229.1'
port = 3306
user = 'root'
password = '123456'
database = '121.36.229.1'
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
    print('DEBUG: chat_id', chat_id)
    try:
        with con.cursor() as cur:
            sql = "select content, response from chat_history where chat_id = %s"
            cur.execute(sql, (chat_id,))
            # print('DEBUG: hello')
            content, response = cur.fetchone()
            # print('DEBUG: chat_content(chat_id): ', chat_id, content, response)
            return content, response
    except mysql.MySQLError as e:
        return f"Database error: {e}"  # 数据库连接或查询失败时返回错误信息
    finally:
        cur.close()


def update_content(chat_id, content_j: json, response_j: json):
    try:
        with con.cursor() as cur:
            sql = "update chat_history set content = %s, response = %s where chat_id = %s"
            cur.execute(sql, (content_j, response_j, chat_id,))
            con.commit()
            return True
    except mysql.MySQLError as e:
        return f"Database error: {e}"
    finally:
        cur.close()


def new_chat(user_id):
    try:
        with con.cursor() as cur:
            sql = "insert into chat_history(user_id, content, response) values (%s, %s, %s)"
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
        content, response = chat_content(chat_id)
        content_data = json.loads(content)
        response_data = json.loads(response)
        n = len(content_data)
        chat_content_list = []
        chat_response_list = []
        for _, content in content_data.items():
            if _ != "0":
                chat_content_list.append({
                    "role": "user",
                    "parts": content
                })
        for _, response in response_data.items():
            if _ != "0":
                chat_response_list.append({
                    "role": "model",
                    "parts": response
                })
        chat_history = []
        for i in range(n-1):
            chat_history.append(chat_content_list[i])
            chat_history.append(chat_response_list[i])

        ask_content = ('要求:{回复内容的标题使用二级目录显示,每一个条目单独一行,**每一个换行都需要两个(!重要)**"\n",如果问电影就要包括名称,年份,豆瓣评分,导演,演员和梗概等;'
                       '或者问影人就要包括名称,出生日期,出生地点,作品,简介等;如果该问题与电影无关,回复"不好意思，该问题与电影无关"')
        ask_content += "},真正需要回答的问题:{"
        ask_content += content_s + '}:'
        print('DEBUG:', ask_content)
        response_content = mod.ask(ask_content, chat_history)

        content_data[n] = content_s
        response_data[n] = response_content

        sql_input_0 = json.dumps(content_data)
        sql_input_1 = json.dumps(response_data)
        update_content(chat_id, sql_input_0, sql_input_1)
        print(response_content)

        return response_content
    except mysql.MySQLError as e:
        return f"Database error: {e}"


def ask_for_img(chat_id: int, text, img):
    import apps.ask.model as ask_model
    text += "使用中文回答"
    response_text = ask_model.ask_img(text, img)
    try:
        content, response = chat_content(chat_id)
        content_data = json.loads(content)
        response_data = json.loads(response)
        n = len(content_data)
        content_data[n] = text + '(给了一张图片)'
        response_data[n] = response_text
        sql_input_0 = json.dumps(content_data)
        sql_input_1 = json.dumps(response_data)
        update_content(chat_id, sql_input_0, sql_input_1)
        return response_text
    except mysql.MySQLError as e:
        return f"Database error: {e}"


if __name__ == '__main__':
    a = {0: '你好', 1: '我想询问一些关于电影的问题'}
    b = {0: '你好', 1: '好的，您请问'}
    a = json.dumps(a)
    b = json.dumps(b)
    update_content(1, a, b)
