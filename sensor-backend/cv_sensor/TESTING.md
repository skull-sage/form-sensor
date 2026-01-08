# Testing the Doc Sensor Module

## Prerequisites

1. Install PyPDF2:
```bash
pip install PyPDF2>=3.0.0
```

2. Start the backend server:
```bash
cd sensor-backend
python main.py
```

3. Server should be running at: http://localhost:8000

## Testing Steps

### 1. Check API Documentation

Visit: http://localhost:8000/docs

You should see the doc-sensor endpoints under the "doc-sensor" tag.

### 2. Test Analyze CV (Upload + Analysis in One Step)

**Using the API Docs:**
1. Go to http://localhost:8000/docs
2. Find `POST /doc-sensor/analyze-cv`
3. Click "Try it out"
4. Upload a PDF file
5. Click "Execute"

**Using curl:**
```bash
curl -X POST "http://localhost:8000/doc-sensor/analyze-cv" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/resume.pdf"
```

**Expected Response:**
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
  "work_experience": [...],
  "skill_keywords": [...],
  "education": [...]
}
```

**Save the `cv_id` for next steps!**

### 3. Test List CVs

**Using curl:**
```bash
curl -X GET "http://localhost:8000/doc-sensor/cvs" \
  -H "accept: application/json"
```

**Expected Response:**
```json
{
  "cvs": [
    {
      "cv_id": "550e8400-e29b-41d4-a716-446655440000",
      "filename": "resume.pdf",
      "upload_date": "2024-12-29T10:30:00Z",
      "analyzed": true
    }
  ],
  "count": 1
}
```

### 4. Test Get CV Details

**Using curl:**
```bash
curl -X GET "http://localhost:8000/doc-sensor/cv/YOUR_CV_ID" \
  -H "accept: application/json"
```

### 5. Test Get Skills Only

**Using curl:**
```bash
curl -X GET "http://localhost:8000/doc-sensor/cv/YOUR_CV_ID/skills" \
  -H "accept: application/json"
```

**Expected Response:**
```json
{
  "cv_id": "550e8400-e29b-41d4-a716-446655440000",
  "skill_keywords": ["Python", "React", "Docker", "AWS"]
}
```

### 6. Test Delete CV

**Using curl:**
```bash
curl -X DELETE "http://localhost:8000/doc-sensor/cv/YOUR_CV_ID" \
  -H "accept: application/json"
```

**Expected Response:**
```json
{
  "message": "CV 'resume.pdf' (ID: 550e8400-...) deleted successfully"
}
```

## Error Testing

### Test Invalid File Format

Upload a non-PDF file (e.g., .txt, .docx):

**Expected Response:** 400 Bad Request
```json
{
  "detail": "Invalid file format. Expected PDF, got: document.txt"
}
```

### Test File Too Large

Upload a file > 10MB:

**Expected Response:** 413 Payload Too Large
```json
{
  "detail": "File too large. Maximum size: 10.0MB, uploaded: 15.2MB"
}
```

### Test Invalid CV ID

Try to analyze with wrong CV ID:

**Expected Response:** 404 Not Found
```json
{
  "detail": "CV with ID 'invalid-id' not found"
}
```

### Test Image-Based PDF

Upload a PDF with only images (no text):

**Expected Response:** 422 Unprocessable Entity
```json
{
  "detail": "No text found in PDF. The PDF may be image-based or corrupted."
}
```

## Sample Test CV

Create a simple test CV (test_resume.txt) and convert to PDF:

```
John Doe
john.doe@email.com | +1-234-567-8900 | San Francisco, CA
https://linkedin.com/in/johndoe | https://github.com/johndoe

EXPERIENCE

Senior Software Engineer
Tech Corp | 2020 - Present
- Led development of microservices architecture using Python and FastAPI
- Implemented CI/CD pipelines with Docker and Kubernetes
- Mentored junior developers and conducted code reviews

Software Developer
Previous Company | 2018 - 2020
- Developed web applications using React and Node.js
- Worked with PostgreSQL and MongoDB databases
- Collaborated with cross-functional teams

SKILLS

Python, JavaScript, React, FastAPI, Django, Node.js, Docker, Kubernetes, 
AWS, PostgreSQL, MongoDB, Git, CI/CD, Agile

EDUCATION

Bachelor of Science in Computer Science
University of California | 2018
```

## Verification Checklist

- [ ] CV upload and analysis works in one step
- [ ] Analysis extracts basic info (name, email, phone)
- [ ] Analysis extracts work experience with dates
- [ ] Analysis extracts skill keywords (generic, not tech-specific)
- [ ] Analysis extracts education
- [ ] List CVs shows uploaded CVs
- [ ] Get CV details returns complete data
- [ ] Get skills returns skill keywords only
- [ ] Delete CV removes the CV
- [ ] Invalid file format returns 400
- [ ] File too large returns 413
- [ ] Image-based PDF returns 422

## Troubleshooting

### PyPDF2 Not Found
```bash
pip install PyPDF2
```

### Server Not Starting
Check if port 8000 is already in use:
```bash
# Windows
netstat -ano | findstr :8000

# Kill process if needed
taskkill /PID <PID> /F
```

### PDF Extraction Returns Empty Text
- Ensure PDF contains actual text (not just images)
- Try a different PDF
- Check PDF is not password-protected

## Next Steps

After successful testing:
1. Test with real CV samples
2. Verify extraction accuracy
3. Refine extraction algorithms if needed
4. Implement frontend UI
5. Add more comprehensive error handling
