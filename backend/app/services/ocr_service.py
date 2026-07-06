from pathlib import Path

import cv2
import pytesseract
from PIL import Image


class OCRService:

    def __init__(self):

        pytesseract.pytesseract.tesseract_cmd = (
            r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        )

    def extract_text(self, image_path: Path) -> str:

        image = cv2.imread(str(image_path))

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        pil_image = Image.fromarray(gray)

        text = pytesseract.image_to_string(
            pil_image,
            lang="eng",
        )

        return text.strip()