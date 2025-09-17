import requests
import yaml

with open("config.yaml", "r", encoding='UTF-8') as f:
    cfg = yaml.safe_load(f)

api_key = cfg.get("DECODING_KEY")

url = 'https://apis.data.go.kr/1471000/DURPrdlstInfoService03/getUsjntTabooInfoList03'

params ={'serviceKey' : api_key, 
         'pageNo' : '1', 
         'numOfRows' : '3',
         'typeName' : '병용금기',
         'itemName' : '',
         'type' : 'json'
         }

resp = requests.get(url, params=params)
print(f"Requested URL: {resp.url}")
print(f"Status Code: {resp.status_code}")

with open('output.txt', 'w', encoding='utf-8') as tf:
    tf.write(resp.text)
print("텍스트 형태로 output.txt에 저장했습니다.")