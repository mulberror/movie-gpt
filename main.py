import json
from urllib import request
import apps.chat as mod
import base64
from PIL import Image
from io import BytesIO
import base64

from flask import Flask
from flask import request
from flask import jsonify

GLOBAL_CONFIG = {
    'port': 5010
}

app = Flask(__name__)


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    if not username or not password:
        return jsonify({"success": False, "data": {}})

    import apps.login as login_mod
    user_id, msg = login_mod.login(username, password)

    if user_id is not None:
        return jsonify({
            "success": True,
            "data": {
                "avatar": "https://avatars.githubusercontent.com/u/44761321",
                "username": username,
                "nickname": username,
                "roles": ["admin"],
                "permissions": ["*:*:*"],
                "accessToken": "eyJhbGciOiJIUzUxMiJ9.admin",
                "refreshToken": "eyJhbGciOiJIUzUxMiJ9.adminRefresh",
                "expires": "2030/10/30 00:00:00"
            }
        })
    else:
        return jsonify({"success": False, "data": {}})


@app.route('/get-async-routes', methods=['GET'])
def async_routes():
    print('DEBUG: arrive async-routes')
    permission_route = {
        "success": True,
        "data": [{
            "path": "/permission",
            "meta": {
                "title": "权限管理",
                "icon": "ep:lollipop",
                "rank": 10,
                "showLink": False
            },
            "children": [
                {
                    "path": "/permission/page/index",
                    "name": "PermissionPage",
                    "meta": {
                        "title": "页面权限",
                        "roles": ["admin", "common"]
                    }
                },
                {
                    "path": "/permission/button",
                    "meta": {
                        "title": "按钮权限",
                        "roles": ["admin", "common"]
                    },
                    "children": [
                        {
                            "path": "/permission/button/router",
                            "component": "permission/button/index",
                            "name": "PermissionButtonRouter",
                            "meta": {
                                "title": "路由返回按钮权限",
                                "auths": [
                                    "permission:btn:add",
                                    "permission:btn:edit",
                                    "permission:btn:delete"
                                ]
                            }
                        },
                        {
                            "path": "/permission/button/login",
                            "component": "permission/button/perms",
                            "name": "PermissionButtonLogin",
                            "meta": {
                                "title": "登录接口返回按钮权限"
                            }
                        }
                    ]
                }
            ]
        }]
    }
    return jsonify(permission_route)


@app.route('/chat/list/', methods=['GET'])
def chat_list():  # 返回该用户的聊天总数
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'msg': '未获取到 user_id'})
    if user_id.isdigit() is False:
        return jsonify({'success': False, 'msg': 'user_id 不是数字'})
    try:
        result = mod.chat_list(int(user_id))
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'msg': str(e)})


@app.route('/chat/newchat/', methods=['GET'])
def new_chat():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'msg': '未获取到 user_id'})
    if user_id.isdigit() is False:
        return jsonify({'success': False, 'msg': 'user_id 不是数字'})
    try:
        result = mod.new_chat(int(user_id))
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'msg': str(e)})

@app.route('/chat/content/', methods=['GET'])
def chat_content():
    chat_id = request.args.get('chat_id')
    print(chat_id)
    if not chat_id:
        return jsonify({'success': False, 'msg': '未获取到 chat_id'})
    if chat_id.isdigit() is False:
        return jsonify({'success': False, 'msg': 'chat_id 不是数字'})
    try:
        content, response = mod.chat_content(int(chat_id))
        content = json.loads(content)
        response = json.loads(response)
        return jsonify({'success': True, 'content': content, 'response': response})
    except Exception as e:
        return jsonify({'success': False, 'msg': str(e)})


@app.route('/search', methods=['GET'])
def search():
    content = '爱情'
    import apps.search as rsearch
    result = rsearch.get_search_results(content)
    index = 0
    result_list = []
    for data in result:
        print('DEBUG:', data)
        index += 1
        current = {
            "index": index,
            "isSetup": True,
            "type": 4,
            "banner": "https://tdesign.gtimg.com/tdesign-pro/cloud-server.jpg",
            "name": data['name'],
            "description": data['summary'],
            "url": data['img'],
        }
        result_list.append(current)

    return jsonify({
        'success': True,
        'data': {
            'list': result_list
        }
    })


@app.route('/chat/ask/', methods=['GET'])
def chat_ask():
    chat_id = request.args.get('chat_id')
    content = request.args.get('content')
    print("DEBUG:", chat_id, content)
    if not chat_id:
        return jsonify({'success': False, 'msg': '未获取到 chat_id'})
    if chat_id.isdigit() is False:
        return jsonify({'success': False, 'msg': 'chat_id 不是数字'})
    try:
        response = mod.chat_ask(int(chat_id), content)
        return jsonify({'success': True, 'response': response})
    except Exception as e:
        return jsonify({'success': False, 'msg': str(e)})


@app.route('/chat/ask-img', methods=['POST'])
def chat_ask_img():
    data = request.get_json()
    text = data.get('text')
    chat_id = data.get('chat_id')
    filename = data.get('image')

    base64_img = filename

    if base64_img.startswith('data:image'):
        base64_img = base64_img.split(',')[1]

    binary_data = base64.b64decode(base64_img)
    bytes_io = BytesIO(binary_data)
    img = Image.open(bytes_io)
    if not img:
        return jsonify({'success': False, 'response': 'receive image error'}), 400
    try:
        response = mod.ask_for_img(int(chat_id), text, img)
        return jsonify({'success': True, 'response': response})
    except Exception as e:
        return jsonify({'success': False, 'msg': str(e)}), 400


if __name__ == '__main__':
    app.run(port=GLOBAL_CONFIG['port'], debug=True)
