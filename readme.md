# 📄 AI-Powered PDF Data Extractor

A full-stack web application that leverages AI to automatically extract and structure tabular data from PDF invoices, built with React, FastAPI, and Google Gemini AI.

## 🎯 Problem Statement

**Project Goal:** Build a proof-of-concept containerized application that allows users to upload PDF files, uses an AI model to parse documents and extract tables, then displays the data in a clean, structured format.

**Core Requirements:**
- Handle both digital and scanned PDFs (OCR capability)
- Extract tabular data from invoices
- Return structured JSON data
- Display extracted data in readable HTML tables
- Containerize with Docker for single-command deployment
- Secure API key management through environment variables

## 💡 Approach & Solution

### Architecture Overview
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Frontend  │────▶│   Backend   │────▶│  Gemini AI  │
│   (React)   │◀────│  (FastAPI)  │◀────│    (API)    │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │                     
       ▼                   ▼                     
   Host: 3000         Host: 8000                  
   Container: 5173    Container: 8000
```

### Workflow
1. **User uploads PDF** through React interface
2. **Frontend validates** file format and size
3. **Backend processes PDF** using PyPDF2 for text extraction
4. **AI extracts tables** via Gemini API with structured prompts
5. **Data returned as JSON** with tables and summary
6. **Frontend renders** data in formatted tables

## 🛠️ Technology Stack

### Frontend
- **React 18** with TypeScript for type safety
- **Vite** for fast development and building
- **CSS3** with modern gradients and animations
- **File validation** for PDF format checking

### Backend
- **FastAPI** for high-performance async API
- **PyPDF2** for PDF text extraction
- **Google Gemini AI** for intelligent table extraction
- **Python 3.11** with type hints
- **CORS** middleware for cross-origin requests

### Infrastructure
- **Docker** for containerization
- **Docker Compose** for multi-service orchestration
- **Environment variables** for secure configuration
- **Health checks** for service reliability

## 🐳 Containerization Strategy

### Docker Implementation

The application uses a multi-container architecture with Docker Compose:
```yaml
services:
  backend:
    - Python 3.11 slim base image
    - FastAPI application on port 8000
    - Environment-based API key injection
    - Health check endpoint
    
  frontend:
    - Node 20 Alpine base image
    - Vite dev server on port 5173 (container)
    - Mapped to host port 3000
    - Depends on backend service
```

### Port Mapping
- **Frontend**: Container port 5173 → Host port 3000
- **Backend**: Container port 8000 → Host port 8000

### Key Containerization Features
- **Isolated environments** for frontend and backend
- **Single command deployment** via docker-compose
- **Environment variable management** for secrets
- **Network isolation** with Docker bridge network
- **Volume mounting** for development hot-reload
- **Non-root users** for security

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose installed
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation & Running

1. **Clone the repository**
```bash
git clone https://github.com/deshpande-atharva/AI-powered-PDF-extractor-and-Summarizer.git
cd pdf-data-extractor
```

2. **Run with Docker Compose**
```bash
# Linux/Mac
GEMINI_API_KEY=your_api_key_here docker-compose up --build

# Windows PowerShell
$env:GEMINI_API_KEY="your_api_key_here"
docker-compose up --build
```

3. **Access the application**
- Frontend: http://localhost:3000 (mapped from container port 5173)
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 📋 Features

- ✅ **PDF Upload** - Drag-and-drop or browse file selection
- ✅ **Format Validation** - Client-side PDF validation
- ✅ **Text Extraction** - Extracts text from digital PDFs
- ✅ **AI Processing** - Intelligent table identification
- ✅ **Structured Output** - JSON formatted data
- ✅ **Table Display** - Clean, responsive HTML tables
- ✅ **Summary Generation** - Invoice totals and counts
- ✅ **Error Handling** - Graceful error messages
- ✅ **Loading States** - Visual feedback during processing

## 🔒 Security Considerations

- API keys stored as environment variables, never in code
- Backend acts as proxy to AI services
- Frontend never has direct access to API keys
- `.env` files excluded from version control
- Non-root Docker containers for reduced attack surface
- Input validation on both client and server

## 📁 Project Structure
```
pdf-data-extractor/
├── backend/
│   ├── app/
│   │   └── main.py          # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile          # Backend container config
├── frontend/
│   ├── src/
│   │   ├── App.tsx         # Main React component
│   │   ├── components/     # React components
│   │   └── services/       # API services
│   ├── package.json        # Node dependencies
│   ├── vite.config.ts      # Vite configuration
│   └── Dockerfile          # Frontend container config
├── docker-compose.yml      # Multi-container orchestration
├── .env.example           # Environment template
└── README.md             # Documentation
```

## 🧪 Testing

### Test with Sample PDFs
```bash
# Generate test invoices
python generate_test_pdfs.py

# Upload through frontend UI
```

### Sample Output
```json
{
  "tables": [{
    "title": "Invoice Items",
    "headers": ["Description", "Quantity", "Unit Price", "Total"],
    "rows": [
      ["Office Chair", "3", "$1,409.04", "$4,227.12"]
    ]
  }],
  "summary": {
    "total_amount": 4309.97,
    "invoice_count": 1,
    "date_range": "2024"
  }
}
```

## 🔧 Development

### Local Development without Docker
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (separate terminal)
cd frontend
npm install
npm run dev  # Runs on port 5173
```

## 📊 Performance

- PDF processing: ~2-5 seconds for typical invoices
- Supports files up to 10MB
- Handles multi-page documents
- Concurrent request handling via async FastAPI

## 🤝 Future Enhancements

- [ ] OCR support for scanned PDFs
- [ ] Batch file processing
- [ ] Export to CSV/Excel
- [ ] Database persistence
- [ ] Authentication system
- [ ] Advanced table detection algorithms

## 📝 License

MIT License - See LICENSE file for details

## 👨‍💻 Author

Atharva Deshpande
- Email: deshpande.atha@northeastern.edu

---

*Built as a technical assessment demonstrating full-stack development, AI integration, and DevOps practices.*