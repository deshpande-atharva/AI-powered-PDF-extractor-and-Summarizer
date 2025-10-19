# from fastapi import FastAPI, UploadFile, File, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# import logging
# from typing import Dict, Any
# import traceback

# from .services.pdf_processor import PDFProcessor
# from .services.ocr_service import OCRService
# from .services.gemini_service import GeminiService
# from .config import settings

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# app = FastAPI(title="PDF Data Extractor API", version="1.0.0")

# # CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Initialize services
# pdf_processor = PDFProcessor()
# ocr_service = OCRService()
# gemini_service = GeminiService(api_key=settings.GEMINI_API_KEY)

# @app.get("/")
# async def root():
#     return {"message": "PDF Data Extractor API is running"}

# @app.get("/health")
# async def health_check():
#     return {"status": "healthy"}

# @app.post("/api/extract")
# async def extract_pdf_data(file: UploadFile = File(...)) -> Dict[str, Any]:
#     """
#     Extract tabular data from uploaded PDF file
#     """
#     try:
#         # Validate file type
#         if not file.filename.lower().endswith('.pdf'):
#             raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
#         # Read file content
#         logger.info(f"Processing file: {file.filename}")
#         content = await file.read()
        
#         # Extract text from PDF
#         text_content = pdf_processor.extract_text(content)
        
#         # If no text found, try OCR
#         if not text_content.strip():
#             logger.info("No text found, attempting OCR...")
#             images = pdf_processor.pdf_to_images(content)
#             text_content = ocr_service.extract_text_from_images(images)
        
#         if not text_content.strip():
#             raise HTTPException(status_code=422, detail="Could not extract any text from the PDF")
        
#         # Use Gemini to extract and structure tabular data
#         logger.info("Sending to Gemini for table extraction...")
#         extracted_data = gemini_service.extract_tables(text_content)
        
#         return {
#             "success": True,
#             "filename": file.filename,
#             "data": extracted_data
#         }
        
#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"Error processing PDF: {str(e)}")
#         logger.error(traceback.format_exc())
#         raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")


from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import PyPDF2
import io
import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini API configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
@app.get("/")
async def root():
    return {"message": "PDF Data Extractor API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy", "api_key_configured": bool(GEMINI_API_KEY)}

@app.post("/api/extract")
async def extract_pdf_data(file: UploadFile = File(...)):
    try:
        # Validate file
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Read and extract text from PDF
        content = await file.read()
        pdf_file = io.BytesIO(content)
        
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Could not read PDF: {str(e)}")
        
        if not text.strip():
            return {
                "success": False,
                "filename": file.filename,
                "data": {
                    "tables": [],
                    "summary": None,
                    "message": "No text found - might be scanned PDF"
                }
            }
        
        # Use Gemini REST API
        if GEMINI_API_KEY:
            prompt = """
            Extract all tabular data from this text. Focus on invoice data.
            Return ONLY valid JSON with this exact structure:
            {
                "tables": [
                    {
                        "title": "Invoice Items",
                        "headers": ["Description", "Quantity", "Price", "Total"],
                        "rows": [["Item 1", "2", "$10", "$20"]]
                    }
                ],
                "summary": {
                    "total_amount": 100,
                    "invoice_count": 1,
                    "date_range": "2024-2025"
                }
            }
            
            Text: """ + text[:3000]
            
            # Call Gemini REST API
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt}
                        ]
                    }
                ]
            }
            
            try:
                response = requests.post(GEMINI_API_URL, json=payload)
                response.raise_for_status()
                
                result = response.json()
                generated_text = result['candidates'][0]['content']['parts'][0]['text']
                
                # Extract JSON from response
                if "```json" in generated_text:
                    generated_text = generated_text.split("```json")[1].split("```")[0]
                elif "{" in generated_text:
                    start = generated_text.find("{")
                    end = generated_text.rfind("}") + 1
                    generated_text = generated_text[start:end]
                
                data = json.loads(generated_text)
                
            except requests.exceptions.RequestException as e:
                print(f"API Error: {e}")
                data = {
                    "tables": [],
                    "summary": None,
                    "error": "Could not connect to Gemini API"
                }
            except json.JSONDecodeError as e:
                print(f"JSON Parse Error: {e}")
                data = {
                    "tables": [],
                    "summary": None,
                    "error": "Could not parse AI response"
                }
        else:
            data = {
                "tables": [],
                "summary": None,
                "message": "No API key configured",
                "text_preview": text[:500]
            }
        
        return {
            "success": True,
            "filename": file.filename,
            "data": data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))