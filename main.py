import json
from urllib import request

from flask import Flask
from flask import request
from flask import jsonify

GLOBAL_CONFIG = {
    'port': 5010
}

app = Flask(__name__)


@app.route('/login/', methods=['POST'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    print(username, password)

    if not username or not password:
        return jsonify({'status': False, 'msg': '用户名或密码不为空'}), 400

    import app.login as mod
    user_id, msg = mod.login(username, password)

    if user_id is not None:
        return jsonify({'status': True, 'user_id': user_id, 'msg': msg})
    else:
        return jsonify({'status': False, 'msg': msg})


@app.route('/chat/list/', methods=['GET'])
def chat_list():  # 返回该用户的聊天总数
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'status': False, 'msg': '未获取到 user_id'})
    if user_id.isdigit() is False:
        return jsonify({'status': False, 'msg': 'user_id 不是数字'})
    import app.chat as mod
    try:
        result = mod.chat_list(int(user_id))
        return jsonify({'status': True, 'result': result})
    except Exception as e:
        return jsonify({'status': False, 'msg': str(e)})


@app.route('/chat/content/', methods=['GET'])
def chat_content():
    chat_id = request.args.get('chat_id')
    if not chat_id:
        return jsonify({'status': False, 'msg': '未获取到 chat_id'})
    if chat_id.isdigit() is False:
        return jsonify({'status': False, 'msg': 'chat_id 不是数字'})
    import app.chat as mod
    try:
        content, respond = mod.chat_content(int(chat_id))
        content = json.loads(content)
        respond = json.loads(respond)
        return jsonify({'status': True, 'content': content, 'respond': respond})
    except Exception as e:
        return jsonify({'status': False, 'msg': str(e)})


@app.route('/chat/ask/', methods=['GET'])
def chat_ask():
    chat_id = request.args.get('chat_id')
    content = request.args.get('content')
    if not chat_id:
        return jsonify({'status': False, 'msg': '未获取到 chat_id'})
    if chat_id.isdigit() is False:
        return jsonify({'status': False, 'msg': 'chat_id 不是数字'})
    import app.chat as mod
    try:
        respond = mod.chat_ask(int(chat_id), content)
        return jsonify({'status': True, 'respond': respond})
    except Exception as e:
        return jsonify({'status': False, 'msg': str(e)})


if __name__ == '__main__':
    app.run(port=GLOBAL_CONFIG['port'], debug=True)
