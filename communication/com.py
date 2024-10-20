import request
import sys
sys.path.append('../')

import KEY

API_KEY = KEY.API_KEY
SECRET_KEY = KEY.SECRET_KEY
URL = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/txt_keywords_extraction'

text = input()