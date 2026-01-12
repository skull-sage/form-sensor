# Doc Sensor Module - CV Analysis Summary

## Purpose

The doc-sensor module analyzes CV/Resume PDFs and extracts structured information for recruitment and candidate management systems.

## Key Features

### 1. Basic Info Extraction
- **Name**: Extracted from document header
- **Email**: Pattern matching for email addresses
- **Phone**: International phone number formats
- **Address**: City, state, country information
- **Social Links**: LinkedIn, GitHub, portfolio URLs

### 2. Work Experience Extraction
- **Company Names**: For each position held
- **Dates**: Start and end dates (or "Present" for current roles)
- **Descriptions**: Job responsibilities and achievements
- **Chronological Order**: Most recent first

### 3. Skill Keywords Extraction
- **Programming Languages**: Python, JavaScript, Java, etc.
- **Frameworks**: React, Django, FastAPI, etc.
- **Tools & Platforms**: Docker, AWS, Git, etc.
- **Deduplication**: Normalized and unique skills list

### 4. Education Qualifications
- **Degrees**: Bachelor's, Master's, PhD, Diploma, etc.
- **Institutions**: University/college names
- **Graduation Dates**: Completion or expected dates
- **Chronological Order**: Most recent first

## API Endpoints

### Upload CV
```
POST /doc-sensor/upload-cv
Input: PDF file (multipart/form-data)
Output: {"cv_id": "uuid", "message": "CV uploaded", "pages": 3}
```

### Analyze CV
```
POST /doc-sensor/analyze-cv/:id
Input: CV ID in URL
Output: Complete structured CV data (see below)
```

### Get CV Details
```
GET /doc-sensor/cv/:id
Output: CV data with analysis results
```

### List All CVs
```
GET /doc-sensor/cvs
Output: List of all uploaded CVs with metadata
```

### Delete CV
```
DELETE /doc-sensor/cv/:id
Output: Confirmation message
```

## Response Structure

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
      "github": "https://github.com/johndoe",
      "portfolio": "https://johndoe.com"
    }
  },
  "work_experience": [
    {
      "company": "Tech Corp",
      "start_date": "2020-01-01",
      "end_date": "Present",
      "description": "Led development of microservices architecture..."
    },
    {
      "company": "Previous Company",
      "start_date": "2018-06-01",
      "end_date": "2019-12-31",
      "description": "Developed web applications using React and Node.js..."
    }
  ],
  "skill_keywords": [
    "Python",
    "JavaScript",
    "React",
    "FastAPI",
    "Docker",
    "AWS",
    "PostgreSQL"
  ],
  "education": [
    {
      "degree": "Master of Science in Computer Science",
      "institution": "Stanford University",
      "graduation_date": "2018-05-15"
    },
    {
      "degree": "Bachelor of Science in Computer Engineering",
      "institution": "UC Berkeley",
      "graduation_date": "2016-05-20"
    }
  ]
}
```

## Technical Stack

### Backend Dependencies
- **PyPDF2** or **pdfplumber**: PDF text extraction
- **regex**: Pattern matching for emails, phones, dates
- **FastAPI**: REST API framework
- **Pydantic**: Data validation

### Extraction Techniques
- **Section Detection**: Identify CV sections using keywords
- **Pattern Matching**: Regex for emails, phones, URLs, dates
- **Keyword Matching**: Known skills database for technical terms
- **Date Parsing**: Multiple date format support
- **Text Normalization**: Consistent formatting and deduplication

## Error Handling

### File Validation
- Non-PDF files → 400 Bad Request
- Files > 10MB → 413 Payload Too Large
- Corrupted PDFs → 422 Unprocessable Entity

### Extraction Errors
- Missing sections → Return empty arrays (not errors)
- Unparseable dates → Return raw strings or null
- No text in PDF → 422 Unprocessable Entity

### Query Errors
- CV not found → 404 Not Found
- Invalid CV ID → 400 Bad Request

## Data Handling

### Missing Data
- All fields are optional (use null for missing data)
- Empty arrays for missing sections
- Partial extraction is acceptable

### Date Formats
- ISO 8601 format: "YYYY-MM-DD"
- Current positions: "Present"
- Missing dates: null

### Skill Normalization
- Case-insensitive matching
- Common variations handled (JS → JavaScript)
- Duplicates removed

## Implementation Phases

### Phase 1: Core Infrastructure
- PDF upload and storage
- Text extraction
- Basic API endpoints

### Phase 2: Basic Info
- Name extraction
- Email extraction
- Phone extraction
- Address extraction
- Social links extraction

### Phase 3: Work Experience
- Section detection
- Company extraction
- Date parsing
- Description extraction

### Phase 4: Skills & Education
- Skill keywords extraction
- Education qualifications extraction
- Data normalization

### Phase 5: Frontend & Polish
- Upload interface
- Results display
- Error handling
- Testing and refinement

## Success Criteria

1. Successfully extract text from 95%+ of standard PDF CVs
2. Accurately identify candidate email in 90%+ of CVs
3. Extract work experience with company names in 85%+ of CVs
4. Identify at least 70% of technical skills mentioned
5. Extract education qualifications in 80%+ of CVs
6. Handle errors gracefully with clear messages
7. Process CVs in under 5 seconds

## Next Steps

1. Review and approve requirements
2. Set up development environment
3. Install PDF processing libraries
4. Implement Phase 1 (core infrastructure)
5. Iterate through remaining phases
6. Test with real CV samples
7. Refine extraction algorithms based on results
