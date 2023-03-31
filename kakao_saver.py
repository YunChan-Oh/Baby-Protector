import requests
import json
#https://kauth.kakao.com/oauth/authorize?client_id=	b9b6556ddc0734a31be1af6fded0c70d&redirect_uri=https://naver.com&response_type=code&scope=talk_message
url = 'https://kauth.kakao.com/oauth/token'
rest_api_key = 'b9b6556ddc0734a31be1af6fded0c70d'
redirect_uri = 'https://naver.com'
#authorize_code = 'iMQyUm87CpBXPa6aABrkdsYot-H83DBQV2wXDwHLXVIvjIKlV9tYiBKAeRwnXaIqRGOeXworDNQAAAGA9jurzg'
authorize_code = 'ZLdPVAyqzThFYpMB8Zv8S4mnp56tP94CAwj2Op7t-ZEbgwpOJQQ63wZtagYBtgpLFAaM-Ao9cxcAAAGCq3fbUg'

data = {
    'grant_type':'authorization_code',
    'client_id':rest_api_key,
    'redirect_uri':redirect_uri,
    'code': authorize_code,
    }

response = requests.post(url, data=data)
tokens = response.json()
print(tokens)



with open("kakao_code.json","w") as fp:
    json.dump(tokens, fp)