import google.generativeai as genai
import KEY as conf
import time

import os

os.environ['http_proxy'] = "http://127.0.0.1:7890"
os.environ['https_proxy'] = "http://127.0.0.1:7890"

genai.configure(api_key=conf.GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def ask(content):
    print('DEBUG: ARRIVED ASK MODEL ===================== ')
    start_time = time.time()
    # response = model.generate_content(content)
    end_time = time.time()
    print('DEBUG: ask took {} seconds'.format(end_time - start_time))
    return '测试文本'
