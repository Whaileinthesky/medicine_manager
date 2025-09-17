import sys
from typing import List
import cv2 as cv
import numpy as np
import yaml
from PySide6.QtCore import QThread, Signal, Slot, QObject
from PySide6.QtGui import QImage, QPixmap, QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QApplication, QMainWindow, QHeaderView, QTableView
from ui_final import Ui_MainWindow
from api_client import DURClient
from ocr import UIOCRCamera

class OCRWorker(QThread):
    """
    A QThread worker for performing OCR in the background.
    """
    frame_ready = Signal(QImage, list)
    error = Signal(str)

    def __init__(self, cam_index: int = 0, gpu: bool = True, parent: QObject = None):
        super().__init__(parent)
        font_path = "assets/NoonnuBasicGothicRegular.ttf"
        self._camera = UIOCRCamera(
            languages=["ko", "en"], gpu=gpu, cam_index=cam_index, font_path=font_path
        )
        self._is_running = True

    def run(self):
        """
        Continuously captures frames from the camera, processes them, and emits the result.
        """
        try:
            while self._is_running:
                annotated_bgr, texts = self._camera.read_and_annotate()
                rgb_image = cv.cvtColor(annotated_bgr, cv.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
                self.frame_ready.emit(qt_image.copy(), texts)
                self.msleep(10)  # Small delay to prevent high CPU usage
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self._camera.close()

    def stop(self):
        """
        Stops the worker thread.
        """
        self._is_running = False
        self.wait(1000)


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    The main window of the application.
    """
    def __init__(self, cam_index: int = 0, gpu: bool = True):
        super().__init__()
        self.setupUi(self)

        self.camera_view.setScaledContents(True)

        self.my_medicine_list_model = QStandardItemModel(self)
        self.my_medicines_list_view.setModel(self.my_medicine_list_model)

        self.dur_table_model = QStandardItemModel(0, 3, self)
        self.dur_table_model.setHorizontalHeaderLabels(
            ["Ingredient", "Product Name", "Reason for Contraindication"]
        )
        self.dur_table_view.setModel(self.dur_table_model)
        self._configure_dur_table()

        self._latest_ocr_texts: List[str] = []
        self.api_key = self._load_api_key()
        if self.api_key:
            self.dur_client = DURClient(api_key=self.api_key)
        else:
            self.dur_client = None
            self.status_bar.showMessage("DUR Client could not be initialized.", 5000)

        self.ocr_worker = OCRWorker(cam_index=cam_index, gpu=gpu, parent=self)
        self.ocr_worker.frame_ready.connect(self.on_frame_ready)
        self.ocr_worker.error.connect(self.on_worker_error)
        self.ocr_worker.start()

        self.add_medicine_button.clicked.connect(self.on_add_medicine_clicked)
        self.quit_button.clicked.connect(self.close)

    def _configure_dur_table(self):
        """
        Configures the appearance and behavior of the DUR table.
        """
        self.dur_table_view.setAlternatingRowColors(True)
        self.dur_table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.dur_table_view.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.dur_table_view.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)
        self.dur_table_view.horizontalHeader().setStretchLastSection(True)
        self.dur_table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.dur_table_view.setSortingEnabled(False)

    def _load_api_key(self) -> str:
        """
        Loads the API key from the config.yaml file.
        """
        try:
            with open("config.yaml", "r", encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}
            api_key = config.get("DECODING_KEY", "")
            if not api_key:
                self.status_bar.showMessage("API key is missing from config.yaml.", 5000)
            return api_key
        except FileNotFoundError:
            self.status_bar.showMessage("config.yaml not found.", 5000)
            return ""

    @Slot(QImage, list)
    def on_frame_ready(self, qt_image: QImage, texts: List[str]):
        """
        Slot to handle a new frame from the OCR worker.
        """
        self.camera_view.setPixmap(QPixmap.fromImage(qt_image))
        self._latest_ocr_texts = texts or []
        self.ocr_result_label.setText(
            self._latest_ocr_texts[0] if self._latest_ocr_texts else "No text detected"
        )

    @Slot(str)
    def on_worker_error(self, message: str):
        """
        Slot to handle an error from the OCR worker.
        """
        self.status_bar.showMessage(f"Camera/OCR error: {message}", 5000)

    def on_add_medicine_clicked(self):
        """
        Handles the 'Add Medicine' button click.
        Adds the detected medicine to the list and checks for interactions.
        """
        if not self._latest_ocr_texts:
            self.status_bar.showMessage("No text to add.", 2000)
            return

        item_name = (self._latest_ocr_texts[0] or "").strip()
        if not item_name:
            self.status_bar.showMessage("Cannot add empty text.", 2000)
            return

        self.my_medicine_list_model.appendRow(QStandardItem(item_name))
        self._check_for_drug_interactions(item_name)

    def _check_for_drug_interactions(self, item_name: str):
        """
        Queries the DUR API for interactions and populates the table.
        """
        if not self.dur_client:
            self.status_bar.showMessage("DUR client is not available.", 5000)
            return

        try:
            response = self.dur_client.query_drug_interaction(item_name=item_name, rows=50)
            rows_added = self._populate_dur_table_from_response(response.json())
            if rows_added == 0:
                self.status_bar.showMessage("No drug interaction results found.", 3000)
            else:
                self.dur_table_view.scrollToBottom()
                self.status_bar.showMessage(f"Added {rows_added} DUR results.", 2000)
        except Exception as e:
            self.status_bar.showMessage(f"DUR API error: {e}", 5000)

    def _populate_dur_table_from_response(self, response_data: dict) -> int:
        """
        Parses the DUR API JSON response and adds rows to the table.
        """
        items = self._extract_items_from_response(response_data)
        if not items:
            return 0

        added_count = 0
        for item in items:
            ingredient = str(item.get("MIXTURE_INGR_KOR_NAME", "") or "")
            product_name = str(item.get("MIXTURE_ITEM_NAME", "") or "")
            reason = str(item.get("PROHBT_CONTENT", "") or "")

            if not (ingredient or product_name or reason):
                continue

            self.dur_table_model.appendRow([
                QStandardItem(ingredient),
                QStandardItem(product_name),
                QStandardItem(reason),
            ])
            added_count += 1
        return added_count

    def _extract_items_from_response(self, response_data: dict) -> List[dict]:
        """
        Safely extracts the list of items from the API response.
        """
        try:
            items = response_data.get("body", {}).get("items", [])
            if isinstance(items, dict):  # API can return a dict for a single item
                items = items.get("item", [])
            if isinstance(items, dict): # or a dict with a single item
                return [items]
            return items
        except (AttributeError, TypeError):
            return []


    def closeEvent(self, event):
        """
        Handles the window close event to stop the worker thread.
        """
        if self.ocr_worker.isRunning():
            self.ocr_worker.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(cam_index=0, gpu=True)
    window.setWindowTitle("Medicine Interaction Checker")
    window.show()
    sys.exit(app.exec())
