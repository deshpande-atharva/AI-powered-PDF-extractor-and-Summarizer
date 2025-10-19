import google.generativeai as genai
import json
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def extract_tables(self, text: str) -> Dict[str, Any]:
        """Use Gemini to extract and structure tabular data from text"""
        try:
            prompt = """
            You are a data extraction specialist. Analyze the following text and extract all tabular data.
            Focus on invoice data including:
            - Invoice numbers
            - Dates
            - Vendor/Customer information
            - Line items with descriptions and amounts
            - Totals and subtotals
            
            Return the data in this JSON format:
            {
                "tables": [
                    {
                        "title": "Table name or description",
                        "headers": ["Column1", "Column2", ...],
                        "rows": [
                            ["value1", "value2", ...],
                            ...
                        ]
                    }
                ],
                "summary": {
                    "total_amount": 0,
                    "invoice_count": 0,
                    "date_range": "start_date - end_date"
                }
            }
            
            If no tabular data is found, return {"tables": [], "summary": null}
            
            Text to analyze:
            """
            
            response = self.model.generate_content(prompt + text)
            
            # Parse the response
            response_text = response.text
            # Clean up the response to extract JSON
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0]
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0]
            
            try:
                data = json.loads(response_text)
            except json.JSONDecodeError:
                logger.warning("Could not parse Gemini response as JSON")
                # Fallback structure
                data = {
                    "tables": [],
                    "summary": None,
                    "raw_response": response_text
                }
            
            return data
            
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            raise