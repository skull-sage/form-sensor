# Doc Sensor Module - CV Analysis

## Overview

The doc-sensor module provides CV/Resume analysis capabilities, extracting structured information from PDF documents.

## Module Structure

```
doc-sensor/
├── __init__.py          # Module initialization
├── router.py            # API endpoints with /doc-sensor prefix
├── services.py          # CVService business logic
├── schemas.py           # Pydantic models for validation
├── validators.py        # Input validation functions
├── extractors.py        # PDF parsing and data extraction
└── README.md            # This file
```

## Features Implemented

### 1. Single-Step CV Analysis
- Upload PDF and get analysis in one API call
- Validates PDF format and file size (max 10MB)
- Extracts text from PDF using PyPDF2
- Stores CV data with analysis in memory
- Returns complete structured data with unique CV ID
- **Basic Info Extraction**: Name, email, phone, address, social links
- **Work Experience**: Company names, dates, job descriptions
- **Skill Keywords**: Technical skills, programming languages, frameworks, tools
- **Education**: Degrees, institutions, graduation dates

### 2. Data Extraction
- List all uploaded CVs
- Get CV details with analysis
- Delete CVs
- Get skill keywords only

## API Endpoints

### POST /doc-sensor/analyze-cv
Upload and analyze a CV PDF file in one step.

**Request**: Multipart form data with PDF file
**Response**:
```json
{
  "cv_id": "550e8400-e29b-41d4-a716-446655440000",
  "basic_info": {
    "name": "John Doe",
    "email": "john.doe@email.com",
    "phone": "+1-234-567-8900",
    "address": "San Francisco, CA",
    "social_links": {
      "linkedin": "https://linkedin.com/in/johndoe",
      "github": "https://github.com/johndoe"
    }
  },
  "work_experience": [
    {
      "company": "Tech Corp",
      "start_date": "2020",
      "end_date": "Present",
      "description": "Led development of..."
    }
  ],
  "skill_keywords": ["Python", "React", "Docker"],
  "education": [
    {
      "degree": "Bachelor of Science in Computer Science",
      "institution": "University of California",
      "graduation_date": "2019"
    }
  ]
}
```

### GET /doc-sensor/cv/{cv_id}
Get complete CV details including raw text and analysis.

### GET /doc-sensor/cvs
List all uploaded CVs with metadata.

**Response**:
```json
{
  "cvs": [
    {
      "cv_id": "550e8400-e29b-41d4-a716-446655440000",
      "filename": "john_doe_resume.pdf",
      "upload_date": "2024-12-29T10:30:00Z",
      "analyzed": true
    }
  ],
  "count": 1
}
```

### DELETE /doc-sensor/cv/{cv_id}
Delete a CV and its analysis.

### GET /doc-sensor/cv/{cv_id}/skills
Get only skill keywords for a specific CV.

## Data Storage

All CV data is stored in memory using a dictionary:

```python
cv_store = {
    "cv_id": {
        "id": "uuid",
        "filename": "resume.pdf",
        "upload_date": "2024-12-29T10:30:00Z",
        "pages": 2,
        "raw_text": "Full extracted text...",
        "file_size": 1024000,
        "analysis": {
            "cv_id": "uuid",
            "basic_info": {...},
            "work_experience": [...],
            "skill_keywords": [...],
            "education": [...]
        }
    }
}
```

**Note**: This is an MVP implementation. Data is lost when the server restarts.

## Extraction Logic

### Basic Info
- **Name**: Extracted from first 5 lines (capitalized words)
- **Email**: Regex pattern matching
- **Phone**: Multiple phone format patterns
- **Address**: City, state, country patterns
- **Social Links**: LinkedIn, GitHub, portfolio URL extraction

### Work Experience
- Section detection using keywords
- Date range parsing (YYYY - YYYY or "Present")
- Company name extraction
- Job description aggregation

### Skill Keywords
- Section detection for skills/technologies
- Generic extraction - parses whatever is listed in the skills section
- Handles multiple formats (comma, pipe, bullet, line-separated)
- Not limited to technical skills - works for any domain
- Deduplication and sorting

### Education
- Section detection for education/qualifications
- Degree pattern matching (Bachelor's, Master's, PhD, etc.)
- Institution name extraction (University, College, Institute)
- Graduation year extraction

## Error Handling

- **400 Bad Request**: Invalid file format, invalid CV ID
- **404 Not Found**: CV not found
- **413 Payload Too Large**: File exceeds 10MB
- **422 Unprocessable Entity**: PDF parsing failed, no text found
- **500 Internal Server Error**: Unexpected errors
- **503 Service Unavailable**: Service not initialized

## Dependencies

- **PyPDF2**: PDF text extraction
- **FastAPI**: REST API framework
- **Pydantic**: Data validation
- **Python regex**: Pattern matching

## Testing

Test the API using the interactive docs at:
```
http://localhost:8000/docs
```

Or using curl:
```bash
# Analyze CV (upload and analyze in one step)
curl -X POST "http://localhost:8000/doc-sensor/analyze-cv" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@resume.pdf"

# List CVs
curl -X GET "http://localhost:8000/doc-sensor/cvs" \
  -H "accept: application/json"

# Get CV details
curl -X GET "http://localhost:8000/doc-sensor/cv/{cv_id}" \
  -H "accept: application/json"
```

## Limitations (MVP)

1. **In-Memory Storage**: Data lost on restart
2. **Simple Extraction**: Basic regex-based parsing
3. **Limited Formats**: Only PDF supported
4. **No OCR**: Image-based PDFs not supported
5. **English Only**: Optimized for English CVs
6. **Basic Date Parsing**: Limited date format support

## Future Enhancements

1. Database persistence (PostgreSQL)
2. Advanced NLP for better extraction
3. OCR support for image-based PDFs
4. Multi-language support
5. Machine learning for entity recognition
6. Batch processing
7. Export to various formats
8. Search and filtering capabilities
