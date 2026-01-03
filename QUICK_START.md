# Quick Start Guide

## Project Overview

A modular full-stack application for semantic text analysis and document processing using AI. Currently includes:
- **form-sensor** - Form field validation using semantic similarity
- **doc-sensor** - CV/Resume analysis and structured data extraction
- **form-ocr** - Scanned paper form OCR processing with perspective correction

## Project Structure

```
form-sensor/
├── .kiro/specs/          # Specification documents per module
├── sensor-backend/       # FastAPI backend with modular structure
├── sensor-ui/            # Vue 3 + Quasar frontend
└── docs/                 # Project documentation
```

## Quick Start

### Backend Setup

```bash
cd sensor-backend

# Option 1: Use setup script (recommended)
./setup.sh  # Linux/macOS
setup.bat   # Windows

# Option 2: Manual setup
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run the server
python main.py
# Or use: ./run.sh (Linux/macOS) or run.bat (Windows)
```

Backend runs at: http://localhost:8000
API docs: http://localhost:8000/docs

### Frontend Setup

```bash
cd sensor-ui

# Install dependencies (using pnpm)
pnpm install

# Run dev server
pnpm dev
```

Frontend runs at: http://localhost:8080

## Current Modules

### form-sensor ✅
**Purpose**: Semantic text similarity for form validation

**Backend API**: `/form-sensor/*`
- Create sensors: `POST /form-sensor/create-text-sensor/:nameId`
- Check similarity: `POST /form-sensor/text-sensor/:nameId`
- List sensors: `GET /form-sensor/text-sensors`
- Delete sensor: `DELETE /form-sensor/text-sensor/:nameId`

**Frontend Routes**: `/smart-form/*`
- Manage sensors: `/smart-form/list`
- Test similarity: `/smart-form/verify`

**Specs**: `.kiro/specs/form-sensor/`

### doc-sensor ✅
**Purpose**: CV/Resume analysis and structured data extraction

**Backend API**: `/doc-sensor/*`
- Analyze CV: `POST /doc-sensor/analyze-cv` (upload + analyze in one step)
- List CVs: `GET /doc-sensor/cvs`
- Get CV details: `GET /doc-sensor/cv/:id`
- Delete CV: `DELETE /doc-sensor/cv/:id`

**Frontend Routes**: `/doc-sensor/*`
- Upload & analyze: `/doc-sensor/upload`
- CV library: `/doc-sensor/list`

**Features**:
- PDF text extraction
- Basic info extraction (name, email, phone, location, social links)
- Work experience parsing
- Skill keywords extraction
- Education qualifications parsing

**Specs**: `.kiro/specs/doc-sensor/`
**Quick Start**: `sensor-ui/src/app-main/doc-sensor/QUICK_START.md`

### form-ocr ✅
**Purpose**: Scanned paper form OCR processing with perspective correction

**Backend API**: `/form-ocr/*`
- Process form: `POST /form-ocr/process-form` (upload + OCR + segment detection)
- List forms: `GET /form-ocr/forms`
- Get form details: `GET /form-ocr/form/:id`
- Get form images: `GET /form-ocr/form/:id/images`
- Delete form: `DELETE /form-ocr/form/:id`

**Frontend Routes**: `/form-ocr/*`
- Upload & process: `/form-ocr/upload`
- Form library: `/form-ocr/list`

**Features**:
- PDF upload (max 20MB)
- Perspective correction with OpenCV
- OCR text extraction with PaddleOCR
- Form segment detection (horizontal/vertical layouts)
- Field extraction (label-value pairs)
- Multi-page support
- GPU acceleration support
- Confidence filtering

**System Requirements**:
- poppler-utils (for PDF conversion)

**Specs**: `.kiro/specs/form-ocr/`
**Quick Start**: `sensor-backend/form-ocr/QUICK_START.md`

## Development Workflow

### Spec-Driven Development

1. **Requirements** → Define what to build
2. **Design** → Plan how to build it
3. **Tasks** → Break down implementation
4. **Implement** → Build and test
5. **Update Specs** → Keep docs current

### Adding a New Module

1. Create specs: `.kiro/specs/your-module/`
2. Create backend: `sensor-backend/your-module/`
3. Create frontend: `sensor-ui/src/app-main/your-module/`
4. Register in main.py and routes.ts

See `MODULAR_STRUCTURE.md` for detailed instructions.

## Key Files

### Documentation
- `MODULAR_STRUCTURE.md` - Complete modular architecture guide
- `sensor-backend/ARCHITECTURE.md` - Backend architecture details
- `sensor-backend/MIGRATION_GUIDE.md` - Migration documentation
- `.kiro/specs/README.md` - Specs structure guide

### Configuration
- `sensor-backend/requirements.txt` - Python dependencies
- `sensor-ui/package.json` - Node dependencies
- `sensor-backend/main.py` - Backend entry point
- `sensor-ui/src/router/routes.ts` - Frontend routing

## Common Commands

### Backend
```bash
# Run server
python main.py

# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Check syntax
python -m py_compile main.py
```

### Frontend
```bash
# Development
pnpm dev

# Build for production
pnpm build

# Type checking
pnpm type-check
```

## API Testing

### Using curl

**form-sensor:**
```bash
# Health check
curl http://localhost:8000/health

# Create sensor
curl -X POST http://localhost:8000/form-sensor/create-text-sensor/test1 \
  -H "Content-Type: application/json" \
  -d '{"text": "paragraph 1\nparagraph 2"}'

# Check similarity
curl -X POST http://localhost:8000/form-sensor/text-sensor/test1 \
  -H "Content-Type: application/json" \
  -d '{"text": "similar text"}'
```

**doc-sensor:**
```bash
# Upload and analyze CV
curl -X POST http://localhost:8000/doc-sensor/analyze-cv \
  -F "file=@/path/to/resume.pdf"

# List all CVs
curl http://localhost:8000/doc-sensor/cvs

# Get CV details
curl http://localhost:8000/doc-sensor/cv/{cv_id}

# Delete CV
curl -X DELETE http://localhost:8000/doc-sensor/cv/{cv_id}
```

**form-ocr:**
```bash
# Process form
curl -X POST http://localhost:8000/form-ocr/process-form \
  -F "file=@/path/to/form.pdf" \
  -F "language=en" \
  -F "enable_segment_detection=true"

# List all forms
curl http://localhost:8000/form-ocr/forms

# Get form details
curl http://localhost:8000/form-ocr/form/{form_id}

# Get form images
curl http://localhost:8000/form-ocr/form/{form_id}/images

# Delete form
curl -X DELETE http://localhost:8000/form-ocr/form/{form_id}
```

### Using API Docs
Visit http://localhost:8000/docs for interactive API documentation.

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Sentence Transformers** - all-MiniLM-L6-v2 model (form-sensor)
- **PyPDF2** - PDF text extraction (doc-sensor)
- **PaddleOCR** - OCR engine (form-ocr)
- **OpenCV** - Image processing and perspective correction (form-ocr)
- **Scikit-learn** - Cosine similarity calculations
- **Pydantic** - Data validation

### Frontend
- **Vue 3** - Progressive JavaScript framework
- **Quasar** - Vue component framework
- **TypeScript** - Type-safe JavaScript
- **Vite** - Fast build tool

## Troubleshooting

### Backend Issues

**Model not loading**
- Check internet connection (models download on first run)
- Verify torch installation: `pip install torch`
- PaddleOCR models download to `~/.paddleocr/`

**Port already in use**
- Change port in main.py: `uvicorn.run(..., port=8001)`

**poppler-utils not found (form-ocr)**
- Ubuntu/Debian: `sudo apt-get install poppler-utils`
- macOS: `brew install poppler`
- Windows: Download from https://github.com/oschwartz10612/poppler-windows/releases

### Frontend Issues

**Dependencies not installing**
- Try: `pnpm install --force`
- Clear cache: `pnpm store prune`

**API connection errors**
- Verify backend is running at http://localhost:8000
- Check CORS configuration in main.py

## Next Steps

1. **Explore form-sensor** - Visit `/smart-form/list` for form validation
2. **Try doc-sensor** - Visit `/doc-sensor/upload` to analyze CVs
3. **Try form-ocr** - Visit `/form-ocr/upload` to process scanned forms
4. **Review specs** - Check `.kiro/specs/` for module documentation
5. **Read architecture** - See `MODULAR_STRUCTURE.md` for details
6. **Plan new modules** - Use existing modules as templates

## Resources

- FastAPI Docs: https://fastapi.tiangolo.com/
- Sentence Transformers: https://www.sbert.net/
- Vue 3 Docs: https://vuejs.org/
- Quasar Docs: https://quasar.dev/

## Support

For questions or issues:
1. Check documentation in `docs/` folder
2. Review module specs in `.kiro/specs/`
3. Consult architecture guides
