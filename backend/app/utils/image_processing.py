"""
OCR image preprocessing utilities.

Applies a series of image processing steps to maximize Tesseract OCR accuracy.
"""

import numpy as np
import cv2


def preprocess_for_ocr(image: np.ndarray) -> np.ndarray:
    """
    Applies full preprocessing pipeline to a BGR or grayscale image:
    1. Convert to grayscale
    2. Denoise
    3. Adaptive threshold (binarize)
    4. Deskew
    5. Upscale if too small

    Returns a preprocessed grayscale uint8 ndarray ready for Tesseract.
    """
    # Ensure grayscale
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()

    # Upscale small images to improve OCR accuracy (Tesseract works best at ~300 DPI)
    h, w = gray.shape
    if h < 800 or w < 600:
        scale = max(800 / h, 600 / w, 1.5)
        gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    # Denoise
    gray = cv2.fastNlMeansDenoising(gray, h=10, templateWindowSize=7, searchWindowSize=21)

    # Adaptive threshold – handles uneven lighting
    binary = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        blockSize=31,
        C=15
    )

    # Deskew
    binary = _deskew(binary)

    return binary


def _deskew(image: np.ndarray) -> np.ndarray:
    """Detects and corrects skew angle using Hough line transform."""
    coords = np.column_stack(np.where(image < 128))  # find dark pixels
    if len(coords) == 0:
        return image

    angle = cv2.minAreaRect(coords)[-1]

    # minAreaRect returns angles in [-90, 0); normalize to (-45, 45]
    if angle < -45:
        angle = 90 + angle
    if abs(angle) < 0.5:
        return image  # skip trivial corrections

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        image, M, (w, h),
        flags=cv2.INTER_CUBIC,
        borderMode=cv2.BORDER_REPLICATE
    )
    return rotated
