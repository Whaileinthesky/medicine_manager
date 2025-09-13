import os
import sys
import json
import time
import yaml
import cv2 as cv
import numpy as np
import requests
from typing import List, Tuple
from PIL import Image, ImageDraw, ImageFont

import easyocr


class OCRCamera:
    """OpenCV + EasyOCR로 프레임을 읽고 텍스트 박스/라벨을 그려 반환"""
    def __init__(
        self,
        languages: List[str] = ["ko"],
        gpu: bool = True,
        cam_index: int = 0,
        font_path: str = "NoonnuBasicGothicRegular.ttf",
        font_size: int = 32,
        window_name: str = "OCR Result",
    ):
        self.languages = languages
        self.gpu = gpu
        self.cam_index = cam_index
        self.window_name = window_name

        # EasyOCR 초기화 (GPU 실패 시 자동 폴백)
        self.reader = self._init_reader(gpu)

        # 카메라
        self.cap = cv.VideoCapture(self.cam_index, cv.CAP_DSHOW if os.name == "nt" else 0)
        if not self.cap.isOpened():
            raise RuntimeError("Cannot open camera")

        # 폰트 로드 (없으면 기본 폰트 폴백)
        self.font_size = font_size
        self.font = self._load_font(font_path, font_size)

        # 최근 결과
        self.last_result = []  # List[Tuple[bbox, text, prob]]

    @staticmethod
    def _init_reader(gpu: bool):
        try:
            return easyocr.Reader(['ko'], gpu=gpu)
        except Exception:
            # Jetson/환경에 따라 GPU 초기화 실패 시 CPU 폴백
            return easyocr.Reader(['ko'], gpu=False)

    @staticmethod
    def _load_font(font_path: str, font_size: int):
        try:
            return ImageFont.truetype(font_path, font_size)
        except Exception:
            # 시스템 기본 폰트 폴백
            return ImageFont.load_default()

    def read_and_annotate(self) -> Tuple[np.ndarray, List[str]]:
        """프레임을 읽고 OCR 수행 → 주석(텍스트/박스)이 포함된 프레임과 텍스트 리스트 반환"""
        ok, frame = self.cap.read()
        if not ok:
            raise RuntimeError("Failed to read frame from camera")

        # OCR 수행 (원본 BGR 프레임 사용)
        result = self.reader.readtext(frame)
        self.last_result = result

        # PIL로 그리기 → 다시 OpenCV 프레임으로 변환
        img_pil = Image.fromarray(cv.cvtColor(frame, cv.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)

        texts: List[str] = []
        for (bbox, text, prob) in result:
            texts.append(text)
            # bbox: 4점; 좌상/우하 추출
            top_left = tuple(map(int, bbox[0]))
            bottom_right = tuple(map(int, bbox[2]))

            # 라벨 위치
            label_pos = (top_left[0], max(0, top_left[1] - self.font_size - 5))
            # 텍스트(빨강), 사각형(녹색)
            draw.text(label_pos, text, font=self.font, fill=(255, 0, 0, 255))

            # OpenCV로 변환 후 박스 그리기 위해 변환을 뒤에서 통합
        annotated = cv.cvtColor(np.array(img_pil), cv.COLOR_RGB2BGR)
        # 사각형은 OpenCV로
        for (bbox, text, prob) in result:
            top_left = tuple(map(int, bbox[0]))
            bottom_right = tuple(map(int, bbox[2]))
            cv.rectangle(annotated, top_left, bottom_right, (0, 255, 0), 2)

        # 화면 표시
        cv.imshow(self.window_name, annotated)

        return annotated, texts

    def close(self):
        try:
            self.cap.release()
        finally:
            cv.destroyAllWindows()


class DURClient:
    """식약처 DUR(병용금기) API 클라이언트"""
    BASE = "https://apis.data.go.kr/1471000/DURPrdlstInfoService03/getUsjntTabooInfoList03"

    def __init__(self, api_key: str, timeout: float = 10.0):
        if not api_key:
            raise ValueError("API key(DECODING_KEY)가 비어 있습니다. config.yaml을 확인하세요.")
        self.api_key = api_key
        self.timeout = timeout

    def query_usjnt_taboo(
        self,
        item_name: str,
        page_no: int = 1,
        rows: int = 3,
        type_name: str = "병용금기",
        output: str = "json",
    ) -> requests.Response:
        """병용금기 목록 조회"""
        params = {
            "serviceKey": self.api_key,
            "pageNo": str(page_no),
            "numOfRows": str(rows),
            "typeName": type_name,
            "itemName": item_name,
            "type": output,
        }
        resp = requests.get(self.BASE, params=params, timeout=self.timeout)
        return resp


class MedicineManagerApp:
    """앱 오케스트레이션: 카메라 루프 + 키 입력 처리 + DUR API 호출 및 결과 저장"""
    def __init__(
        self,
        config_path: str = "config.yaml",
        font_path: str = "NoonnuBasicGothicRegular.ttf",
        gpu: bool = True,
        cam_index: int = 0,
    ):
        # 설정 로드
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
        api_key = cfg.get("DECODING_KEY", "")

        self.camera = OCRCamera(
            languages=["ko"],
            gpu=gpu,
            cam_index=cam_index,
            font_path=font_path,
            font_size=32,
            window_name="OCR Result",
        )
        self.client = DURClient(api_key=api_key)
        self.selected_item = ""  # 's'로 선택된 텍스트

    def run(self):
        try:
            while True:
                _, texts = self.camera.read_and_annotate()
                key = cv.waitKey(1) & 0xFF

                if key == ord("s"):
                    if texts:
                        self.selected_item = texts[0]
                        print(f"[선택됨] item = {self.selected_item}")
                    else:
                        print("[알림] 현재 프레임에서 텍스트가 인식되지 않았습니다.")

                elif key == ord("q"):
                    print("종료 요청(q) 수신. 루프를 종료합니다.")
                    break

            # 종료 후 DUR 조회
            if self.selected_item:
                print("[DUR] 병용금기 조회 요청:", self.selected_item)
                resp = self.client.query_usjnt_taboo(item_name=self.selected_item)
                print(f"Requested URL: {resp.url}")
                print(f"Status Code: {resp.status_code}")

                # 저장 (원문 텍스트 그대로)
                with open("output.txt", "w", encoding="utf-8") as tf:
                    tf.write(resp.text)
                print("텍스트 형태로 output.txt에 저장했습니다.")

                # JSON일 경우 보기 좋게 pretty-print도 함께 저장
                try:
                    data = resp.json()
                    with open("output_pretty.json", "w", encoding="utf-8") as jf:
                        json.dump(data, jf, ensure_ascii=False, indent=2)
                    print("JSON 형태로 output_pretty.json에도 저장했습니다.")
                except Exception:
                    pass
            else:
                print("[알림] 선택된 item이 없어 DUR 조회를 생략합니다.")

        finally:
            self.camera.close()


def main():
    # 환경에 맞게 옵션 조정 가능
    app = MedicineManagerApp(
        config_path="config.yaml",
        font_path="NoonnuBasicGothicRegular.ttf",
        gpu=True,        
        cam_index=0,     # 카메라 인덱스
    )
    app.run()


if __name__ == "__main__":
    main()
