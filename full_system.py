import requests
import yaml
import cv2 as cv
import easyocr
import numpy as np
from PIL import Image, ImageDraw, ImageFont

#api_key 불러오기
with open("config.yaml", "r", encoding='UTF-8') as f:
    cfg = yaml.safe_load(f)

api_key = cfg.get("DECODING_KEY")

# camera setting
reader = easyocr.Reader(['ko'], gpu=True)
cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

# 우리가 찾는 의약품
item = ''

# EasyOCR Reader 객체 생성 
reader = easyocr.Reader(['ko'], gpu=True)

# 카메라 열기 
cap = cv.VideoCapture(0)

#카메라 사용 불가의 경우
if not cap.isOpened():
    print("Cannot open camera")
    exit()


while True:
    # 프레임 캡처
    ret, frame = cap.read()
    
    img_pil = Image.fromarray(cv.cvtColor(frame, cv.COLOR_BGR2RGB))

    #img_pil object
    draw = ImageDraw.Draw(img_pil)

    #korean pont
    font_path = "NoonnuBasicGothicRegular.ttf"
    font_size = 32
    font = ImageFont.truetype(font_path, font_size)

    # OCR을 적용할 이미지 (프레임에서 텍스트 추출)
    result = reader.readtext(frame)
 
 
    # OCR 결과 출력
    for (bbox, text, prob) in result:
        top_left = tuple(map(int, bbox[0]))  # 첫 번째 좌표 (x1, y1)
        bottom_right = tuple(map(int, bbox[2])) # 세 번째 좌표 (x3, y3)
        #텍스트가 표시될 위치 설정
        position = (top_left[0], top_left[1] - font_size - 5)

        # 텍스트 출력
        draw.text(position, text, font=font, fill=(255, 0, 0, 0))

        frame = cv.cvtColor(np.array(img_pil), cv.COLOR_RGB2BGR)
        # 사각형 그리기
        cv.rectangle(img=frame, pt1=top_left, pt2=bottom_right, color=(0, 255, 0), thickness=2)

    

    # OCR 결과를 화면에 띄우기
    cv.imshow("OCR Result", frame)

    key = cv.waitKey(1) & 0xFF

    #s키를 눌러서 원하는 텍스트 저장
    if key == ord('s'):
        texts = [text for (_bbox, text, _prob) in result]
        item = texts[0]
        print(texts)#debug

    # 'q' 키를 눌러 종료
    elif key == ord('q'):
        break


#api와 통신할 url
url = 'http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList'

params ={'serviceKey' : api_key, 
         'pageNo' : '1', 
         'numOfRows' : '3',
         'type' : 'json',
         'itemName' : item
         }

#API와 통신해서 받은 정보 저장
resp = requests.get(url, params=params)
print(f"Requested URL: {resp.url}")
print(f"Status Code: {resp.status_code}")

with open('output.txt', 'w', encoding='utf-8') as tf:
    tf.write(resp.text)
print("텍스트 형태로 output.txt에 저장했습니다.")