import cv2
import easyocr

# EasyOCR Reader 객체 생성 (한글 인식을 위해 'ko' 언어 모델 사용)
reader = easyocr.Reader(['en'], gpu=True)

# 카메라 열기 (기본 카메라 번호는 0)
cap = cv2.VideoCapture(0)

#카메라 사용 불가의 경우
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # 프레임 캡처
    ret, frame = cap.read()
    
    # 프레임을 화면에 표시
    cv2.imshow("Camera Feed", frame)

    # OCR을 적용할 이미지 (프레임에서 텍스트 추출)
    result = reader.readtext(frame)
 
 
    # OCR 결과 출력
    for (bbox, text, prob) in result:
        # bbox는 [(x1, y1), (x2, y2), (x3, y3), (x4, y4)] 형태일 것
        # 이를 통해 좌상단(top_left)과 우하단(bottom_right)을 추출
        top_left = tuple(map(int, bbox[0]))  # 첫 번째 좌표 (x1, y1)
        bottom_right = tuple(map(int, bbox[2])) # 세 번째 좌표 (x3, y3)
        # 사각형 그리기
        cv2.rectangle(img=frame, pt1=top_left, pt2=bottom_right, color=(0, 255, 0), thickness=2)
        
        # 텍스트 출력
        cv2.putText(frame, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # OCR 결과를 화면에 띄우기
    cv2.imshow("OCR Result", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        texts = [text for (_bbox, text, _prob) in result]
        print(texts)

    # 'q' 키를 눌러 종료
    elif key == ord('q'):
        break

# 카메라 해제 및 창 닫기
cap.release()
cv2.destroyAllWindows()
