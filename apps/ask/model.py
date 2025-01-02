import google.generativeai as genai
import KEY as conf
import time

import os

os.environ['http_proxy'] = "http://127.0.0.1:7890"
os.environ['https_proxy'] = "http://127.0.0.1:7890"

genai.configure(api_key=conf.GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-pro")


def ask(content, my_history):
    print('debug: ARRIVED ASK MODEL\n ====== ')
    start_time = time.time()
    chat = model.start_chat(history=my_history)
    response = chat.send_message(content)
    end_time = time.time()
    print('DEBUG: ask took {} seconds'.format(end_time - start_time))
    return response.text


def ask_img(content, img):
    # print('debug: ARRIVED ASK MODEL\n ====== ')
    start_time = time.time()
    img_model = genai.GenerativeModel("gemini-1.5-pro")
    response = img_model.generate_content([content, img]).text
    end_time = time.time()
    print('DEBUG: response is {}'.format(response))
    print('DEBUG: ask took {} seconds'.format(end_time - start_time))
    return response
