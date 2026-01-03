# Doc Sensor Module - Design Document

## Overview

The Doc Sensor module provides CV/Resume analysis and structured data extraction from PDF documents. The module uses PDF parsing libraries and NLP techniques to extract work experience, technical skills, and educational qualifications, enabling automated CV screening and candidate profile building.

## Module Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Module Router │    │   PDF Parser    │
│   (Vue/Quasar)  │◄──►│   (FastAPI)     │◄──►│   (PyPDF2)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  Module Service │
                       │  (CV Analysis)  │
                       └─────────────────┘
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
            ┌──────────────┐    ┌──────────────┐
            │  Extractors  │    │  Data Store  │
            │  (Parsers)   │    │  (In-Memory) │
            └──────────────┘    └──────────────┘
```

### Module Structure

```
sensor-backend/
├── doc-sensor/                  # CV analysis module
│   ├── __init__.py
│   ├── router.py               # API endpoints with /doc-sensor prefix
│   ├── services.py             # CVAnalysisService business logic
│   ├── schemas.py              # Pydantic models
│   ├── validators.py           # Input validation
│   ├── models.py               # Database models (optional)
│   └── extractors.py           # CV parsing and extraction utilities
│       ├── pdf_extractor.py    # PDF text extraction
│       ├── experience_extractor.py  # Work experience parsing
│       ├── skills_extractor.py      # Stack keywords extraction
│       └── education_extractor.py   # Education parsing
└── main.py                     # App initialization and module registration
```

## Module Components and Interfaces

### CVAnalysisService (services.py)
- **Purpose**: Core business logic for CV analysis operations
- **Methods**:
  - `upload_cv(file, metadata) -> dict` - Store CV and return ID
  - `analyze_cv(cv_id: str) -> dict` - Extract structured data from CV
  - `extract_basic_info(text: str) -> dict` - Extract name, email, phone, address, social links
  - `get_cv(cv_id: str) -> dict` - Retrieve CV data and analysis
  - `get_all_cvs() -> list` - List all uploaded CVs
  - `delete_cv(cv_id: str) -> bool` - Remove CV and analysis data

### Module Router (router.py)
- **Purpose**: API endpoints with /doc-sensor prefix
- **Endpoints**: See API Endpoints section below

### Validators (validators.py)
- **Purpose**: Input validation functions
- **Functions**:
  - `validate_pdf_file(file) -> bool` - Check file format and size
  - `validate_cv_id(cv_id: str) -> str` - Validate CV ID format
  - `validate_file_size(file, max_size: int) -> bool` - Check size limits

### Extractors (extractors.py)
- **Purpose**: Extract structured data from CV text
- **Modules**:
  - **pdf_extractor.py**: Extract text from PDF files
    - `extract_text_from_pdf(file) -> str`
  - **profile_extractor.py**: Parse candidate basic information
    - `extract_basic_info(text: str) -> dict`
    - `extract_name(text: str) -> str`
    - `extract_email(text: str) -> str`
    - `extract_phone(text: str) -> str`
    - `extract_address(text: str) -> str`
    - `extract_social_links(text: str) -> dict`
  - **experience_extractor.py**: Parse work experience
    - `extract_work_experience(text: str) -> list[dict]`
    - `parse_dates(text: str) -> tuple[str, str]`
  - **skills_extractor.py**: Extract technical skills
    - `extract_skill_keywords(text: str) -> list[str]`
    - `identify_programming_languages(text: str) -> list[str]`
    - `identify_frameworks(text: str) -> list[str]`
  - **education_extractor.py**: Parse education qualifications
    - `extract_education(text: str) -> list[dict]`
    - `parse_degree(text: str) -> str`

## API Endpoints

### POST /doc-sensor/upload-cv
- **Input**: Multipart form data with PDF file
- **Output**: `{"cv_id": "uuid", "message": "CV uploaded", "pages": 3}`
- **Process**: Validate PDF → Extract text → Store CV → Return ID

### POST /doc-sensor/analyze-cv/:id
- **Input**: CV ID in URL path
- **Output**: 
```json
{
  "cv_id": "uuid",
  "basic_info": {
    "name": "John Doe",
    "email": "john.doe@email.com",
    "phone": "+1-234-567-8900",
    "address": "San Francisco, CA",
    "social_links": {
      "linkedin": "https://linkedin.com/in/johndoe",
      "github": "https://github.com/johndoe",
      "portfolio": "https://johndoe.com"
    }
  },
  "work_experience": [
    {
      "company": "Company Name",
      "start_date": "2020-01-01",
      "end_date": "2023-12-31",
      "description": "Job responsibilities..."
    }
  ],
  "skill_keywords": ["Python", "FastAPI", "React", "Docker"],
  "education": [
    {
      "degree": "Bachelor of Science in Computer Science",
      "institution": "University Name",
      "graduation_date": "2019-05-15"
    }
  ]
}
```
- **Process**: Retrieve CV text → Extract basic info → Extract experience → Extract skills → Extract education → Return structured data

### GET /doc-sensor/cv/:id
- **Output**: 
```json
{
  "cv_id": "uuid",
  "filename": "resume.pdf",
  "upload_date": "2024-01-01T10:00:00Z",
  "pages": 3,
  "raw_text": "Full CV text...",
  "analysis": { /* analysis results */ }
}
```
- **Process**: Retrieve CV data and cached analysis results

### GET /doc-sensor/cvs
- **Output**: 
```json
{
  "cvs": [
    {
      "cv_id": "uuid",
      "filename": "resume.pdf",
      "upload_date": "2024-01-01T10:00:00Z",
      "analyzed": true
    }
  ],
  "count": 10
}
```
- **Process**: List all stored CVs with metadata

### DELETE /doc-sensor/cv/:id
- **Output**: `{"message": "CV deleted successfully"}`
- **Process**: Remove CV text and analysis data

## Data Models

### CV Storage Structure
```python
cv_store = {
    "cv_id": {
        "id": "uuid",
        "filename": "resume.pdf",
        "upload_date": "2024-01-01T10:00:00Z",
        "pages": 3,
        "raw_text": "Full extracted text...",
        "file_size": 1024000,
        "analysis": {
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
            "work_experience": [...],
            "skill_keywords": [...],
            "education": [...]
        }
    }
}
```

### API Request/Response Models
```python
class CVUploadResponse(BaseModel):
    cv_id: str
    message: str
    pages: int

class BasicInfo(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    social_links: Dict[str, str]  # {"linkedin": "url", "github": "url", ...}

class WorkExperience(BaseModel):
    company: str
    start_date: Optional[str]  # ISO 8601 or "Present"
    end_date: Optional[str]
    description: str

class Education(BaseModel):
    degree: str
    institution: str
    graduation_date: Optional[str]

class CVAnalysisResponse(BaseModel):
    cv_id: str
    basic_info: BasicInfo
    work_experience: List[WorkExperience]
    skill_keywords: List[str]
    education: List[Education]

class CVDetailResponse(BaseModel):
    cv_id: str
    filename: str
    upload_date: str
    pages: int
    raw_text: str
    analysis: Optional[CVAnalysisResponse]
```

## Extraction Strategies

### Basic Info Extraction
1. **Name Extraction**: Look for name in document header (usually first few lines, often in larger font)
2. **Email Extraction**: Use regex pattern for email addresses (name@domain.com)
3. **Phone Extraction**: Use regex patterns for phone numbers (various international formats)
4. **Address Extraction**: Look for city, state, country patterns near contact information
5. **Social Links**: Extract URLs for LinkedIn, GitHub, portfolio sites using domain matching

### Work Experience Extraction
1. **Section Detection**: Identify "Experience", "Work History", "Employment" sections
2. **Company Extraction**: Use regex patterns for company names (often in bold or caps)
3. **Date Parsing**: Extract date ranges using patterns like "Jan 2020 - Dec 2023", "2020-2023", "Present"
4. **Description Extraction**: Capture bullet points and paragraphs under each position

### Skill Keywords Extraction
1. **Section Detection**: Identify "Skills", "Technical Skills", "Technologies" sections
2. **Keyword Matching**: Match against known programming languages, frameworks, tools
3. **Context Analysis**: Extract skills mentioned in work experience descriptions
4. **Deduplication**: Remove duplicates and normalize (e.g., "Javascript" → "JavaScript")

### Education Extraction
1. **Section Detection**: Identify "Education", "Academic Background", "Qualifications" sections
2. **Degree Parsing**: Extract degree types (BS, MS, PhD, Bachelor's, Master's)
3. **Institution Extraction**: Identify university/college names
4. **Date Parsing**: Extract graduation dates or expected dates

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: PDF Upload Validation
*For any* uploaded file, if the file is not a valid PDF or exceeds size limits, the system should reject it with appropriate error
**Validates: Requirements 1.1, 1.5**
**Module: doc-sensor**

### Property 2: Text Extraction Completeness
*For any* valid PDF file, text extraction should return non-empty string if PDF contains text
**Validates: Requirements 1.2**
**Module: doc-sensor**

### Property 3: Work Experience Structure
*For any* extracted work experience, each entry should contain company name and description fields (dates may be null)
**Validates: Requirements 2.2, 2.4**
**Module: doc-sensor**

### Property 4: Skill Keywords Deduplication
*For any* list of extracted skill keywords, there should be no duplicate entries
**Validates: Requirements 3.5**
**Module: doc-sensor**

### Property 5: Candidate Email Format
*For any* extracted email address, it should match standard email format pattern or be null
**Validates: Requirements 2.2**
**Module: doc-sensor**

### Property 5: Basic Info Email Format
*For any* extracted email address, it should match standard email format pattern or be null
**Validates: Requirements 2.2**
**Module: doc-sensor**

### Property 6: Education Chronological Order
*For any* list of extracted education qualifications, entries should be ordered by date (most recent first)
**Validates: Requirements 4.5**
**Module: doc-sensor**

### Property 7: JSON Response Structure
*For any* CV analysis response, the JSON should contain basic_info, work_experience, skill_keywords, and education fields (arrays may be empty, basic_info fields may be null)
**Validates: Requirements 8.1, 8.2, 8.3**
**Module: doc-sensor**

### Property 8: Date Format Consistency
*For any* parsed date, it should be in ISO 8601 format (YYYY-MM-DD), "Present", or null
**Validates: Requirements 8.5**
**Module: doc-sensor**

### Property 9: Error Response Format
*For any* error condition, the API should return appropriate HTTP status code with descriptive message
**Validates: Requirements 7.1, 7.2, 7.5**
**Module: doc-sensor**

## Error Handling

### File Upload Errors
- Invalid file format (not PDF) → 400 Bad Request
- File too large (> 10MB) → 413 Payload Too Large
- Corrupted PDF → 422 Unprocessable Entity

### Processing Errors
- PDF text extraction failure → 422 Unprocessable Entity
- No text found in PDF → 422 Unprocessable Entity with message
- Analysis timeout → 504 Gateway Timeout

### Query Errors
- CV ID not found → 404 Not Found
- Invalid CV ID format → 400 Bad Request

### Extraction Errors
- No work experience found → Return empty array (not error)
- No skills found → Return empty array (not error)
- No education found → Return empty array (not error)
- Date parsing failure → Return raw string or null

## Testing Strategy

### Unit Testing Approach
Unit tests will verify specific examples and edge cases:
- PDF validation with various file types
- Text extraction from sample PDFs
- Date parsing with different formats
- Keyword matching against known skills
- API endpoint request/response validation

### Integration Testing Approach
Integration tests will verify end-to-end workflows:
- Upload CV → Analyze → Retrieve results
- Multiple CV uploads and management
- Error handling for invalid inputs
- Edge cases (empty CVs, malformed PDFs)

### Test Data
- Sample CVs with various formats
- CVs with missing sections
- CVs with different date formats
- CVs with international formats

**Configuration**: Each test will use realistic CV samples to ensure extraction accuracy.

Both unit tests and integration tests are complementary - unit tests verify individual extraction functions while integration tests verify the complete CV analysis pipeline.
