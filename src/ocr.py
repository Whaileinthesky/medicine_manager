import os
from typing import List, Tuple

import cv2 as cv
import easyocr
import numpy as np
from PIL import Image, ImageDraw, ImageFont


class OCRCamera:
    """Handles camera interaction and OCR processing."""

    def __init__(
        self,
        languages: List[str] = ["ko"],
        gpu: bool = True,
        cam_index: int = 0,
        font_path: str = "assets/NoonnuBasicGothicRegular.ttf",
        font_size: int = 32,
    ):
        self.languages = languages
        self.gpu = gpu
        self.cam_index = cam_index
        self.font_path = font_path
        self.font_size = font_size

        self.reader = self._initialize_reader()
        self.cap = self._initialize_camera()
        self.font = self._load_font()
        self.last_result = []

    def _initialize_reader(self) -> easyocr.Reader:
        """Initializes the EasyOCR reader, with a fallback to CPU if GPU fails."""
        try:
            return easyocr.Reader(self.languages, gpu=self.gpu)
        except Exception as e:
            print(f"Failed to initialize EasyOCR with GPU, falling back to CPU. Error: {e}")
            return easyocr.Reader(self.languages, gpu=False)

    def _initialize_camera(self) -> cv.VideoCapture:
        """Initializes the camera capture."""
        cap = cv.VideoCapture(self.cam_index, cv.CAP_DSHOW if os.name == "nt" else 0)
        if not cap.isOpened():
            raise RuntimeError("Cannot open camera")
        return cap

    def _load_font(self) -> ImageFont.FreeTypeFont:
        """Loads the specified font, with a fallback to the default font."""
        try:
            return ImageFont.truetype(self.font_path, self.font_size)
        except IOError:
            print(f"Could not load font from {self.font_path}, falling back to default font.")
            return ImageFont.load_default()

    def read_and_annotate(self) -> Tuple[np.ndarray, List[str]]:
        """
        Reads a frame, performs OCR, and returns the annotated frame and recognized texts.
        This method displays the annotated frame in a separate window.
        """
        ok, frame = self.cap.read()
        if not ok:
            raise RuntimeError("Failed to read frame from camera")

        annotated_frame, texts = self.process_frame(frame)
        cv.imshow("OCR Result", annotated_frame)
        return annotated_frame, texts

    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, List[str]]:
        """Performs OCR on a frame and annotates it with bounding boxes and text."""
        result = self.reader.readtext(frame)
        self.last_result = result

        img_pil = Image.fromarray(cv.cvtColor(frame, cv.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)
        texts: List[str] = []

        for (bbox, text, prob) in result:
            texts.append(text)
            top_left = tuple(map(int, bbox[0]))
            label_pos = (top_left[0], max(0, top_left[1] - self.font_size - 5))
            draw.text(label_pos, text, font=self.font, fill=(255, 0, 0, 255))

        annotated_frame_pil = np.array(img_pil)
        annotated_frame_bgr = cv.cvtColor(annotated_frame_pil, cv.COLOR_RGB2BGR)

        for (bbox, text, prob) in result:
            top_left = tuple(map(int, bbox[0]))
            bottom_right = tuple(map(int, bbox[2]))
            cv.rectangle(annotated_frame_bgr, top_left, bottom_right, (0, 255, 0), 2)

        return annotated_frame_bgr, texts


    def close(self):
        """Releases the camera and destroys all OpenCV windows."""
        if self.cap.isOpened():
            self.cap.release()
        cv.destroyAllWindows()


class UIOCRCamera(OCRCamera):
    """
    An OCRCamera subclass that is optimized for UI applications.
    It overrides the read_and_annotate method to not display a window.
    """
    def read_and_annotate(self) -> Tuple[np.ndarray, List[str]]:
        """
        Reads a frame, performs OCR, and returns the annotated frame and recognized texts
        without displaying a window.
        """
        ok, frame = self.cap.read()
        if not ok:
            raise RuntimeError("Failed to read frame from camera")

        return self.process_frame(frame)
