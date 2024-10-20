import requests

API_KEY = "dlLQTZwS6es2GlyEgJo4OSn7"
SECRET_KEY = "JdVpbrlRXCCnUTirMTKKYuiXroKh8pxZ"


def main():
    url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/txt_keywords_extraction?access_token=" + get_access_token()

    payload = "{\"text\":[\"现在再看这部电影，依旧能获得很高的分数。有条不絮的剧情描述，简单而不故弄玄虚。个性鲜明的人物刻画，幽默超前的台词，天马行空的创意特效，热血与温情兼备的情感刻画。周星驰先生，真正为喜剧电影而生的天才。\"],\"num\":5}"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

    for item in response.json():
        print(item)


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


if __name__ == '__main__':
    main()
