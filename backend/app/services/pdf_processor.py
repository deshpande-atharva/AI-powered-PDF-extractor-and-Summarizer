import PyPDF2
import io
from PIL import Image
import pdf2image
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class PDFProcessor:
    def extract_text(self, pdf_content: bytes) -> str:
        """Extract text from a PDF file"""
        try:
            pdf_file = io.BytesIO(pdf_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
            
            return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            return ""
    
    def pdf_to_images(self, pdf_content: bytes) -> List[Image.Image]:
        """Convert PDF pages to images for OCR"""
        try:
            images = pdf2image.convert_from_bytes(pdf_content, dpi=300)
            return images
        except Exception as e:
            logger.error(f"Error converting PDF to images: {str(e)}")
            return []