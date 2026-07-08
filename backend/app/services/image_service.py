"""
Embedded image extraction service using PyMuPDF.

Extracts embedded raster images from a PDF page for downstream OCR processing.
"""

from __future__ import annotations

from typing import Generator

import fitz  # PyMuPDF
import numpy as np
import cv2

from app.core.logging import logger


class ImageService:
    """
    Extracts embedded images from a single PyMuPDF page object.
    Returns images as BGR numpy arrays ready for OCR preprocessing.
    """

    def extract_images_from_page(
        self,
        pdf_document: fitz.Document,
        page: fitz.Page,
        min_width: int = 100,
        min_height: int = 100,
    ) -> Generator[np.ndarray, None, None]:
        """
        Yield BGR numpy arrays for each embedded image on the page
        that meets the minimum dimension requirements.

        Args:
            pdf_document: The open fitz.Document (needed to look up xrefs).
            page: The fitz.Page to scan for embedded images.
            min_width: Skip images narrower than this (avoid icons/bullets).
            min_height: Skip images shorter than this.
        """
        image_list = page.get_images(full=True)

        for img_info in image_list:
            xref = img_info[0]
            try:
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]

                # Decode to numpy array
                nparr = np.frombuffer(image_bytes, np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                if image is None:
                    continue

                h, w = image.shape[:2]
                if w < min_width or h < min_height:
                    continue

                yield image

            except Exception as e:
                logger.warning(f"Failed to extract image (xref={xref}): {e}")
