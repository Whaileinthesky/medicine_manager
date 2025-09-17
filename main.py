# -*- coding: utf-8 -*-
# Run: python app_qt_main.py
# Needs: ui_final.py, full_system_class.py, config.yaml(DECODING_KEY)

import sys
from typing import List, Tuple

import cv2 as cv
import numpy as np
import yaml

from PySide6.QtCore import QThread, Signal, Slot
from PySide6.QtGui import QImage, QPixmap, QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QApplication, QMainWindow, QHeaderView, QTableView

# 1) UI와 백엔드 클래스 임포트
from ui_final import Ui_MainWindow
from full_system_class import OCRCamera, DURClient


# 2) UI용으로 imshow 제거한 OCR 래퍼
class UIOCRCamera(OCRCamera):
    def read_and_annotate(self) -> Tuple[np.ndarray, List[str]]:
        ok, frame = self.cap.read()
        if not ok:
            raise RuntimeError("Failed to read frame from camera")

        result = self.reader.readtext(frame)
        self.last_result = result

        # 라벨/박스 주석 (원본 로직과 동일)
        from PIL import Image, ImageDraw
        img_pil = Image.fromarray(cv.cvtColor(frame, cv.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)

        texts: List[str] = []
        for (bbox, text, prob) in result:
            texts.append(text)
            top_left = tuple(map(int, bbox[0]))
            bottom_right = tuple(map(int, bbox[2]))
            label_pos = (top_left[0], max(0, top_left[1] - self.font_size - 5))
            draw.text(label_pos, text, font=self.font, fill=(255, 0, 0, 255))

        annotated = cv.cvtColor(np.array(img_pil), cv.COLOR_RGB2BGR)
        for (bbox, text, prob) in result:
            top_left = tuple(map(int, bbox[0]))
            bottom_right = tuple(map(int, bbox[2]))
            cv.rectangle(annotated, top_left, bottom_right, (0, 255, 0), 2)

        # imshow 없음 (Qt 라벨에 그림)
        return annotated, texts


# 3) OCR 워커 스레드
class OCRWorker(QThread):
    frame_ready = Signal(QImage, list)  # (QImage, [texts])
    error = Signal(str)

    def __init__(self, cam_index=0, gpu=True, font_path="NoonnuBasicGothicRegular.ttf", parent=None):
        super().__init__(parent)
        self._camera = UIOCRCamera(
            languages=["ko"], gpu=gpu, cam_index=cam_index, font_path=font_path, font_size=32
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
                self.msleep(10)
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self._camera.close()

    def stop(self):
        self._running = False
        self.wait(1000)


# 4) MainWindow
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, cam_index=0, gpu=True):
        super().__init__()
        self.setupUi(self)

        # --- 카메라 QLabel 표시 스케일 ---
        self.camera_frame.setScaledContents(True)

        # --- 내 약 리스트 모델 (QListView) ---
        self.list_model = QStandardItemModel(self)
        self.my_medicines.setModel(self.list_model)

        # --- DUR 테이블 모델: 요청한 3개 컬럼으로 설정 ---
        self.dur_model = QStandardItemModel(0, 3, self)
        self.dur_model.setHorizontalHeaderLabels([
            "성분명",  # 1열
            "제품명",      # 2열
            "금지 사유",         # 3열
        ])
        self.DUR_data_table.setModel(self.dur_model)
        self._tune_table(self.DUR_data_table)

        # --- 최신 OCR 텍스트 저장 ---
        self._latest_texts: List[str] = []

        # --- DUR API 클라이언트 준비 ---
        self.dur_client = DURClient(api_key=self._load_api_key())

        # --- OCR 워커 시작 ---
        self.worker = OCRWorker(cam_index=cam_index, gpu=gpu, parent=self)
        self.worker.frame_ready.connect(self.on_frame_ready)
        self.worker.error.connect(self.on_worker_error)
        self.worker.start()

        # --- 버튼 배선 ---
        self.Save_Button.clicked.connect(self.on_save_clicked)
        self.quit.clicked.connect(self.close)

    # 테이블 옵션 (가독성)
    def _tune_table(self, tv: QTableView):
        tv.setAlternatingRowColors(True)
        tv.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        tv.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        tv.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        tv.horizontalHeader().setStretchLastSection(True)
        tv.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        tv.setSortingEnabled(False)

    def _load_api_key(self) -> str:
        try:
            with open("config.yaml", "r", encoding="utf-8") as f:
                cfg = yaml.safe_load(f) or {}
            key = cfg.get("DECODING_KEY", "")
            if not key:
                self.statusbar.showMessage("config.yaml의 DECODING_KEY가 비어 있습니다.", 5000)
            return key
        except Exception:
            self.statusbar.showMessage("config.yaml을 열 수 없습니다.", 5000)
            return ""

    @Slot(QImage, list)
    def on_frame_ready(self, qimg: QImage, texts: List[str]):
        self.camera_frame.setPixmap(QPixmap.fromImage(qimg))
        self._latest_texts = texts or []
        self.current_text.setText(self._latest_texts[0] if self._latest_texts else "인식된 텍스트 없음")

    @Slot(str)
    def on_worker_error(self, msg: str):
        self.statusbar.showMessage(f"Camera/OCR error: {msg}", 5000)

    # === SAVE: DUR 호출 → 표에 결과 행(들) 추가 ===
    def on_save_clicked(self):
        if not self._latest_texts:
            self.statusbar.showMessage("저장할 텍스트가 없습니다.", 2000)
            return

        item_name = (self._latest_texts[0] or "").strip()
        if not item_name:
            self.statusbar.showMessage("빈 텍스트는 저장하지 않습니다.", 2000)
            return

        # 기존 리스트에도 저장 유지
        self.list_model.appendRow(QStandardItem(item_name))

        # DUR API 호출
        try:
            resp = self.dur_client.query_usjnt_taboo(item_name=item_name, rows=50)  # 필요 시 rows 조정
            rows_added = self._append_dur_rows_from_response(resp)
            if rows_added == 0:
                self.statusbar.showMessage("DUR 결과가 없습니다.", 3000)
            else:
                self.DUR_data_table.scrollToBottom()
                self.statusbar.showMessage(f"DUR 결과 {rows_added}건 추가", 2000)
        except Exception as e:
            self.statusbar.showMessage(f"DUR 호출 오류: {e}", 5000)

    def _append_dur_rows_from_response(self, resp) -> int:
        """DUR JSON 응답에서 필요한 3필드를 뽑아 테이블에 행 추가. 추가한 행 수를 반환."""
        try:
            data = resp.json()
        except Exception:
            return 0

        # 응답 구조 안전 파싱
        items = None
        # 흔한 구조들 순서대로 시도
        items = (
            (data.get("response") or {}).get("body", {}).get("items") or
            data.get("body", {}).get("items") or
            data.get("items")
        )
        # items가 dict일 경우 'item' 키를 꺼내기
        if isinstance(items, dict):
            items = items.get("item", items)
        # 단일 항목 dict를 리스트로
        if isinstance(items, dict):
            items = [items]
        if not isinstance(items, list):
            return 0

        added = 0
        for it in items:
            # 요청한 3개 키 추출 (없으면 빈 문자열)
            ingr = str(it.get("MIXTURE_INGR_KOR_NAME", "") or "")
            name = str(it.get("MIXTURE_ITEM_NAME", "") or "")
            reason = str(it.get("PROHBT_CONTENT", "") or "")

            # 비어 있으면 건너뛰기(선택)
            if not (ingr or name or reason):
                continue

            self.dur_model.appendRow([
                QStandardItem(ingr),
                QStandardItem(name),
                QStandardItem(reason),
            ])
            added += 1

        return added

    def closeEvent(self, event):
        try:
            if self.worker.isRunning():
                self.worker.stop()
        except Exception:
            pass
        return super().closeEvent(event)


# 5) 엔트리포인트
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow(cam_index=0, gpu=True)
    win.setWindowTitle("의약품 매니저 – PySide6 + QLabel + DUR Table")
    win.show()
    sys.exit(app.exec())
