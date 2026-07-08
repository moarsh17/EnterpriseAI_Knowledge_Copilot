"""
OCR service using Tesseract.

Accepts PIL images or numpy arrays directly to avoid
unnecessary temp-file I/O inside the ingestion pipeline.
"""

from pathlib import Path

import cv2
import numpy as np
import pytesseract
from PIL import Image

from app.utils.image_processing import preprocess_for_ocr


class OCRService:

    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = (
            r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        )

    # ------------------------------------------------------------------ #
    # In-memory extraction (primary path for PDF ingestion pipeline)      #
    # ------------------------------------------------------------------ #

    def extract_from_image_array(self, image: np.ndarray) -> str:
        """
        Run OCR on a BGR or grayscale numpy array.
        Applies full preprocessing before sending to Tesseract.
        """
        preprocessed = preprocess_for_ocr(image)
        pil_image = Image.fromarray(preprocessed)
        text = pytesseract.image_to_string(pil_image, lang="eng")
        return text.strip()

    def extract_from_pil(self, image: Image.Image) -> str:
        """
        Run OCR on an already-opened PIL image.
        Converts to numpy array, preprocesses, then runs Tesseract.
        """
        arr = np.array(image.convert("RGB"))
        bgr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
        return self.extract_from_image_array(bgr)

    # ------------------------------------------------------------------ #
    # File-based extraction (kept for ImageLoader compatibility)          #
    # ------------------------------------------------------------------ #

    def extract_text(self, image_path: Path) -> str:
        """
        Run OCR on an image file path.
        Preserved for backward compatibility with ImageLoader.
        """
        image = cv2.imread(str(image_path))
        if image is None:
            return ""
        return self.extract_from_image_array(image)