from algoliasearch.search_client import SearchClient
import json

client = SearchClient.create('MXP1WFVWGE', '2eb8acc230f7fde7375935e999726a22')

# 上传 zh-search.json
zh_index = client.init_index('zh_index')

with open("./data/movies.csv", encoding='utf-8') as f:
    zh_batch = json.load(f)

zh_index.save_objects(zh_batch, {'autoGenerateObjectIDIfNotExist': True})

print('zh/search.json 上传成功')