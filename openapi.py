import requests

url = 'https://apis.data.go.kr/1471000/DURPrdlstInfoService03/getOdsnAtentInfoList03?serviceKey=I4dBVv%2BMef8KeUzJpsbXVyI2FzJRDvaaTrqjwDp3NSU1lZoosPsZFaxekYcWHETBTVLXBnjKr8gE5kiPoAS%2FXA%3D%3D&pageNo=1&numOfRows=3&type=json&typeName=%EB%85%B8%EC%9D%B8%EC%A3%BC%EC%9D%98&ingrCode=D000893&itemName=%ED%8E%98%EB%8B%88%EB%9D%BC%EB%AF%BC%EC%A3%BC%EC%82%AC(%ED%81%B4%EB%A1%9C%EB%A5%B4%ED%8E%98%EB%8B%88%EB%9D%BC%EB%AF%BC%EB%A7%90%EB%A0%88%EC%82%B0%EC%97%BC)&start_change_date=20140521&end_change_date=20140521&itemSeq=196000010'

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status() # HTTP 오류가 발생하면 예외 발생
    print("API 호출 성공!")
except requests.exceptions.RequestException as e:
    print(f"API 호출 중 오류 발생: {e}")
