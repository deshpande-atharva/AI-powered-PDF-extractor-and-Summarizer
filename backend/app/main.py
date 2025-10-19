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
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        content = await file.read()
        pdf_file = io.BytesIO(content)
        
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            
            # DEBUG: Print extracted text
            print(f"DEBUG: Extracted {len(text)} characters from PDF")
            print(f"DEBUG: First 200 chars: {text[:200]}")
            
        except Exception as e:
            print(f"ERROR reading PDF: {e}")
            raise HTTPException(status_code=422, detail=f"Could not read PDF: {str(e)}")
        
        if not text.strip():
            print("DEBUG: No text found in PDF")
            return {
                "success": False,
                "filename": file.filename,
                "data": {
                    "tables": [],
                    "summary": None,
                    "message": "No text found - might be scanned PDF"
                }
            }
        
        # DEBUG: Check if API key exists
        print(f"DEBUG: API Key present: {bool(GEMINI_API_KEY)}")
        print(f"DEBUG: API Key (first 10 chars): {GEMINI_API_KEY[:10] if GEMINI_API_KEY else 'None'}")
        
        if GEMINI_API_KEY:
            prompt = """
            Extract tabular data from this invoice text. 
            Important: 
            - Quantity should be a number without $ sign
            - Price/Rate is the unit price
            - Total/Amount is quantity × price
            
            For the invoice items table, use these exact headers:
            ["Description", "Quantity", "Unit Price", "Total"]
            
            Return ONLY valid JSON:
            {
                "tables": [
                    {
                        "title": "Invoice Items",
                        "headers": ["Description", "Quantity", "Unit Price", "Total"],
                        "rows": [
                            ["item description", "quantity as number", "price with $", "total with $"]
                        ]
                    }
                ],
                "summary": {
                    "total_amount": (final total as number),
                    "invoice_count": 1,
                    "date_range": "date range string"
                }
            }
            
            Invoice text to parse:
            """ + text[:3000]
            
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
                print(f"DEBUG: Calling Gemini API at {GEMINI_API_URL}")
                response = requests.post(GEMINI_API_URL, json=payload)
                print(f"DEBUG: Gemini response status: {response.status_code}")
                
                if response.status_code != 200:
                    print(f"DEBUG: Gemini error response: {response.text}")
                    
                response.raise_for_status()
                
                result = response.json()
                print(f"DEBUG: Gemini response keys: {result.keys()}")
                
                generated_text = result['candidates'][0]['content']['parts'][0]['text']
                print(f"DEBUG: Generated text (first 200 chars): {generated_text[:200]}")
                
                # Extract JSON from response
                if "```json" in generated_text:
                    generated_text = generated_text.split("```json")[1].split("```")[0]
                elif "{" in generated_text:
                    start = generated_text.find("{")
                    end = generated_text.rfind("}") + 1
                    generated_text = generated_text[start:end]
                
                data = json.loads(generated_text)
                print(f"DEBUG: Parsed data successfully: tables={len(data.get('tables', []))}")
                
            except requests.exceptions.RequestException as e:
                print(f"ERROR: API Request failed: {e}")
                data = {
                    "tables": [],
                    "summary": None,
                    "error": f"Could not connect to Gemini API: {str(e)}"
                }
            except json.JSONDecodeError as e:
                print(f"ERROR: JSON Parse failed: {e}")
                print(f"DEBUG: Raw text that failed to parse: {generated_text if 'generated_text' in locals() else 'N/A'}")
                data = {
                    "tables": [],
                    "summary": None,
                    "error": "Could not parse AI response"
                }
            except Exception as e:
                print(f"ERROR: Unexpected error: {e}")
                data = {
                    "tables": [],
                    "summary": None,
                    "error": str(e)
                }
        else:
            print("DEBUG: No API key configured")
            data = {
                "tables": [],
                "summary": None,
                "message": "No API key configured",
                "text_preview": text[:500]
            }
        
        print(f"DEBUG: Returning data with {len(data.get('tables', []))} tables")
        return {
            "success": True,
            "filename": file.filename,
            "data": data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR: Unexpected error in main handler: {e}")
        raise HTTPException(status_code=500, detail=str(e))