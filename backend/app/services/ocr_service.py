import pytesseract
from PIL import Image
from typing import List
import logging

logger = logging.getLogger(__name__)

class OCRService:
    def extract_text_from_images(self, images: List[Image.Image]) -> str:
        """Extract text from images using OCR"""
        text = ""
        try:
            for i, image in enumerate(images):
                logger.info(f"Running OCR on page {i+1}")
                page_text = pytesseract.image_to_string(image)
                text += page_text + "\n"
            return text
        except Exception as e:
            logger.error(f"OCR error: {str(e)}")
            return ""