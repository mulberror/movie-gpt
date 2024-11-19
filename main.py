import json
from urllib import request
import apps.chat as mod

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
    response = {
        "success": True,
        "data": {
            "avatar": "https://avatars.githubusercontent.com/u/44761321",  # 如果需要，解注释
            "username": "admin",
            "nickname": "111111",
            "roles": ["admin"],
            "permissions": ["*:*:*"],
            "accessToken": "eyJhbGciOiJIUzUxMiJ9.admin",
            "refreshToken": "eyJhbGciOiJIUzUxMiJ9.adminRefresh",
            "expires": "2030/10/30 00:00:00"
        }
    }
    return jsonify(response)
    #
    # if not username or not password:
    #     return jsonify({"success": False, "data": {}})
    #
    # import apps.login as login_mod
    # user_id, msg = login_mod.login(username, password)
    #
    # if user_id is not None:
    #     return jsonify({
    #         "success": True,
    #         "data": {
    #             "avatar": "https://avatars.githubusercontent.com/u/44761321",
    #             "username": username,
    #             "nickname": username,
    #             "roles": ["admin"],
    #             "permissions": ["*:*:*"],
    #             "accessToken": "eyJhbGciOiJIUzUxMiJ9.admin",
    #             "refreshToken": "eyJhbGciOiJIUzUxMiJ9.adminRefresh",
    #             "expires": "2030/10/30 00:00:00"
    #         }
    #     })
    # else:
    #     return jsonify({"success": False, "data": {}})


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
                "rank": 10
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
        content, respond = mod.chat_content(int(chat_id))
        content = json.loads(content)
        respond = json.loads(respond)
        return jsonify({'success': True, 'content': content, 'respond': respond})
    except Exception as e:
        return jsonify({'success': False, 'msg': str(e)})


@app.route('/chat/ask/', methods=['GET'])
def chat_ask():
    chat_id = request.args.get('chat_id')
    content = request.args.get('content')
    if not chat_id:
        return jsonify({'success': False, 'msg': '未获取到 chat_id'})
    if chat_id.isdigit() is False:
        return jsonify({'success': False, 'msg': 'chat_id 不是数字'})
    print('DEBUG:')
    try:
        respond = mod.chat_ask(int(chat_id), content)
        return jsonify({'success': True, 'respond': respond})
    except Exception as e:
        return jsonify({'success': False, 'msg': str(e)})


if __name__ == '__main__':
    app.run(port=GLOBAL_CONFIG['port'], debug=True)
