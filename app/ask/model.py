import google.generativeai as genai
import KEY as conf

import os

os.environ['http_proxy'] = "http://127.0.0.1:7890"
os.environ['https_proxy'] = "http://127.0.0.1:7890"

genai.configure(api_key=conf.GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def ask(content):
    response = model.generate_content(content)
    return response.text
