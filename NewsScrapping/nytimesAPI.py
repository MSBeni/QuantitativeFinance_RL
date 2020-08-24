from nytimesarticle import articleAPI

key_path = "/home/i-sip_iot/s_vv/nytimesAPIkey.txt"
key_ = open(key_path, 'r').read()
api = articleAPI(key_)

res = api.search(q='market', begin_date=20200731)
print(res["response"]['docs'])
print(len(res["response"]['docs']))

keys_of_articles = ['abstract', 'web_url', 'snippet', 'lead_paragraph', 'source', 'multimedia', 'headline', 'keywords',
                    'pub_date', 'document_type', 'news_desk', 'section_name', 'byline', 'type_of_material', '_id',
                    'word_count', 'uri']

headline_keys = ['main', 'kicker', 'content_kicker', 'print_headline', 'name', 'seo', 'sub']

for el in res["response"]['docs']:
     print(el['abstract'], "\n")
     print(el['headline']['main'], "\n")
     print(el['headline']['print_headline'], "\n")
     print("####################################")
