# -*- coding: utf-8 -*-
# Run with: python app_qt_main.py
# Requires: ui_final.py (PySide6 UI), full_system_class.py (OCR classes)

import sys
from typing import List, Tuple

import cv2 as cv
import numpy as np
from PIL import Image, ImageDraw

from PySide6.QtCore import QThread, Signal, Slot
from PySide6.QtGui import QImage, QPixmap, QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QApplication, QMainWindow

# 1) 가져오기: UI와 OCR 클래스
from ui_final import Ui_MainWindow  # camera_frame, current_text, my_medicines, Save_Button, quit가 정의됨
from full_system_class import OCRCamera  # 원본 OCR + EasyOCR 로직


# 2) UI 용도로 imshow를 제거한 OCR 래퍼 (상속)
class UIOCRCamera(OCRCamera):
    """UI 통합용: read_and_annotate()에서 cv.imshow를 호출하지 않는 버전"""
    def read_and_annotate(self) -> Tuple[np.ndarray, List[str]]:
        ok, frame = self.cap.read()
        if not ok:
            raise RuntimeError("Failed to read frame from camera")

        # OCR
        result = self.reader.readtext(frame)
        self.last_result = result

        # PIL로 텍스트 라벨 그리고 → OpenCV로 박스
        img_pil = Image.fromarray(cv.cvtColor(frame, cv.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)

        texts: List[str] = []
        for (bbox, text, prob) in result:
            texts.append(text)
            top_left = tuple(map(int, bbox[0]))
            label_pos = (top_left[0], max(0, top_left[1] - self.font_size - 5))
            # 원본 클래스에서 로드한 self.font 사용
            draw.text(label_pos, text, font=self.font, fill=(255, 0, 0, 255))

        annotated = cv.cvtColor(np.array(img_pil), cv.COLOR_RGB2BGR)
        for (bbox, text, prob) in result:
            top_left = tuple(map(int, bbox[0]))
            bottom_right = tuple(map(int, bbox[2]))
            cv.rectangle(annotated, top_left, bottom_right, (0, 255, 0), 2)

        # ★ imshow 없음 (UI에서 QLabel로 그릴 거라서)
        return annotated, texts


# 3) 백그라운드 워커 (QThread): 프레임/텍스트 신호로 UI 업데이트
class OCRWorker(QThread):
    frame_ready = Signal(QImage, list)   # QImage, texts
    error = Signal(str)

    def __init__(self, cam_index=0, gpu=True, font_path="NoonnuBasicGothicRegular.ttf", parent=None):
        super().__init__(parent)
        self._camera = UIOCRCamera(
            languages=["ko"], gpu=gpu, cam_index=cam_index,
            font_path=font_path, font_size=32
        )
        self._running = True

    def run(self):
        try:
            while self._running:
                annotated_bgr, texts = self._camera.read_and_annotate()
                rgb = cv.cvtColor(annotated_bgr, cv.COLOR_BGR2RGB)
                h, w, ch = rgb.shape
                qimg = QImage(rgb.data, w, h, ch * w, QImage.Format.Format_RGB888)
                self.frame_ready.emit(qimg.copy(), texts)
                self.msleep(10)  # 과한 CPU 사용 방지
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self._camera.close()

    def stop(self):
        self._running = False
        self.wait(1000)


# 4) 메인 윈도우: UI 배선
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, cam_index=0, gpu=True):
        super().__init__()
        self.setupUi(self)

        # 카메라 라벨이 UI에 이미 존재(스케일 모드 추천)
        self.camera_frame.setScaledContents(True)

        # 내 약 리스트 모델 바인딩 (QListView: my_medicines)
        self.list_model = QStandardItemModel(self)
        self.my_medicines.setModel(self.list_model)

        # 상태 저장: 최신 텍스트 배열
        self._latest_texts: List[str] = []

        # 워커 스레드 시작
        self.worker = OCRWorker(cam_index=cam_index, gpu=gpu, parent=self)
        self.worker.frame_ready.connect(self.on_frame_ready)
        self.worker.error.connect(self.on_worker_error)
        self.worker.start()

        # 버튼 연결 (SAVE, QUIT는 UI에 이미 있음)
        self.Save_Button.clicked.connect(self.on_save_clicked)
        self.quit.clicked.connect(self.close)

    @Slot(QImage, list)
    def on_frame_ready(self, qimg: QImage, texts: List[str]):
        # 1) 카메라 프레임 → QLabel(camera_frame)
        self.camera_frame.setPixmap(QPixmap.fromImage(qimg))
        # 2) 현재 텍스트 업데이트 → QLabel(current_text)
        self._latest_texts = texts or []
        self.current_text.setText(self._latest_texts[0] if self._latest_texts else "인식된 텍스트 없음")

    @Slot(str)
    def on_worker_error(self, msg: str):
        self.statusbar.showMessage(f"Camera/OCR error: {msg}", 5000)

    def on_save_clicked(self):
        if not self._latest_texts:
            self.statusbar.showMessage("저장할 텍스트가 없습니다.", 2000)
            return
        text = (self._latest_texts[0] or "").strip()
        if not text:
            self.statusbar.showMessage("빈 텍스트는 저장하지 않습니다.", 2000)
            return
        self.list_model.appendRow(QStandardItem(text))
        self.statusbar.showMessage(f"저장됨: {text}", 1500)

    def closeEvent(self, event):
        try:
            if self.worker.isRunning():
                self.worker.stop()
        except Exception:
            pass
        return super().closeEvent(event)


# 5) 실행부
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow(cam_index=0, gpu=True)
    win.setWindowTitle("의약품 매니저 – PySide6 + QLabel")
    win.show()
    sys.exit(app.exec())
