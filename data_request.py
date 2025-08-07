import requests
import yaml

with open("config.yaml", "r", encoding='UTF-8') as f:
    cfg = yaml.safe_load(f)

api_key = cfg.get("DECODING_KEY")


url = 'http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList'

params ={'serviceKey' : api_key, 
         'pageNo' : '1', 
         'numOfRows' : '3',
         'type' : 'json',
         'itemname' : '타이레놀콜드-에스정'
         }

resp = requests.get(url, params=params)
print(f"Requested URL: {resp.url}")
print(f"Status Code: {resp.status_code}")

with open('output.txt', 'w', encoding='utf-8') as tf:
    tf.write(resp.text)
print("텍스트 형태로 output.txt에 저장했습니다.")