# Doc Sensor Module - Requirements Document

## Module Overview

The Doc Sensor module provides CV/Resume analysis and structured data extraction. It processes PDF resumes to extract key information including work experience, technical skills, and educational qualifications, enabling automated CV screening and candidate profile building.

## Glossary

- **Doc_Sensor**: The core module that processes CV/Resume documents and extracts structured information
- **CV_Parser**: Component that extracts text and structure from PDF resumes
- **Basic_Info**: Candidate's basic information including name, email, phone, address, and social links
- **Work_Experience**: Employment history including company, dates, and role descriptions
- **Skill_Keywords**: Technical skills, programming languages, frameworks, and tools extracted from CV
- **Education_Qualification**: Academic degrees, institutions, and graduation dates
- **Date_Extraction**: Process of identifying and parsing date ranges from text
- **Keyword_Extraction**: Process of identifying technical terms and skills from text
- **Section_Detection**: Identifying different sections within a CV (experience, education, skills, contact)

## Requirements

### Requirement 1

**User Story:** As a recruiter, I want to upload CV PDFs, so that I can automatically extract candidate information.

#### Acceptance Criteria

1. WHEN a user uploads a PDF file via POST /doc-sensor/upload-cv, THE Doc_Sensor SHALL validate the file format is PDF
2. WHEN a PDF is validated, THE Doc_Sensor SHALL extract text content from all pages
3. WHEN text is extracted, THE Doc_Sensor SHALL store the raw CV text with a unique CV ID
4. WHEN storage is complete, THE Doc_Sensor SHALL return the CV ID and page count
5. WHEN a file exceeds 10MB, THE Doc_Sensor SHALL reject the upload with appropriate error message

### Requirement 2

**User Story:** As a recruiter, I want to extract candidate basic information, so that I can contact and identify candidates easily.

#### Acceptance Criteria

1. WHEN analyzing a CV, THE Doc_Sensor SHALL extract candidate name from the document header or contact section
2. WHEN extracting contact info, THE Doc_Sensor SHALL identify email address using pattern matching
3. WHEN processing contact details, THE Doc_Sensor SHALL extract phone number if present
4. WHEN scanning for location, THE Doc_Sensor SHALL extract address or city/country information
5. WHEN identifying social links, THE Doc_Sensor SHALL extract LinkedIn, GitHub, portfolio URLs, and other professional profiles

### Requirement 3

**User Story:** As a hiring manager, I want to extract work experience from CVs, so that I can quickly review candidate employment history.

#### Acceptance Criteria

1. WHEN a CV is analyzed via POST /doc-sensor/analyze-cv/:id, THE Doc_Sensor SHALL identify work experience sections
2. WHEN work experience is found, THE Doc_Sensor SHALL extract company names for each position
3. WHEN extracting positions, THE Doc_Sensor SHALL parse start and end dates (or "Present" for current roles)
4. WHEN dates are parsed, THE Doc_Sensor SHALL extract job descriptions and responsibilities
5. WHEN multiple positions exist, THE Doc_Sensor SHALL return them in chronological order (most recent first)

### Requirement 3

**User Story:** As a technical recruiter, I want to identify skill keywords from CVs, so that I can match candidates with job requirements.

#### Acceptance Criteria

1. WHEN analyzing a CV, THE Doc_Sensor SHALL identify skills sections (Skills, Technologies, Technical Skills, etc.)
2. WHEN skills sections are found, THE Doc_Sensor SHALL extract programming languages (Python, JavaScript, Java, etc.)
3. WHEN extracting skills, THE Doc_Sensor SHALL identify frameworks and libraries (React, Django, FastAPI, etc.)
4. WHEN processing skills, THE Doc_Sensor SHALL extract tools and platforms (Docker, AWS, Git, etc.)
5. WHEN skills are extracted, THE Doc_Sensor SHALL return a deduplicated list as skill_keywords

### Requirement 4

**User Story:** As an HR specialist, I want to extract education qualifications, so that I can verify candidate academic backgrounds.

#### Acceptance Criteria

1. WHEN analyzing a CV, THE Doc_Sensor SHALL identify education sections
2. WHEN education is found, THE Doc_Sensor SHALL extract degree names (Bachelor's, Master's, PhD, Diploma, etc.)
3. WHEN extracting degrees, THE Doc_Sensor SHALL identify institution names (universities, colleges)
4. WHEN processing education, THE Doc_Sensor SHALL parse graduation dates or expected graduation dates
5. WHEN multiple degrees exist, THE Doc_Sensor SHALL return them in chronological order (most recent first)

### Requirement 5

**User Story:** As a developer, I want RESTful API endpoints for CV operations, so that I can integrate CV analysis into recruitment applications.

#### Acceptance Criteria

1. WHEN the API receives POST /doc-sensor/upload-cv, THE Doc_Sensor SHALL accept PDF files and return CV ID
2. WHEN the API receives POST /doc-sensor/analyze-cv/:id, THE Doc_Sensor SHALL extract structured data and return JSON
3. WHEN the API receives GET /doc-sensor/cv/:id, THE Doc_Sensor SHALL return stored CV data and analysis results
4. WHEN the API receives GET /doc-sensor/cvs, THE Doc_Sensor SHALL return list of all uploaded CVs with metadata
5. WHEN the API receives DELETE /doc-sensor/cv/:id, THE Doc_Sensor SHALL remove CV and associated analysis data

### Requirement 6

**User Story:** As a user, I want a web interface for CV analysis, so that I can upload and review CVs without using API directly.

#### Acceptance Criteria

1. WHEN a user accesses the interface, THE Doc_Sensor SHALL display a CV upload form with drag-and-drop support
2. WHEN a user uploads a CV, THE Doc_Sensor SHALL show upload progress and analysis status
3. WHEN analysis is complete, THE Doc_Sensor SHALL display extracted work experience in a structured format
4. WHEN displaying results, THE Doc_Sensor SHALL show stack keywords as tags or chips
5. WHEN showing education, THE Doc_Sensor SHALL display qualifications in a timeline or list format

### Requirement 7

**User Story:** As a system operator, I want proper error handling for CV processing, so that the system handles edge cases gracefully.

#### Acceptance Criteria

1. WHEN invalid file formats are uploaded, THE Doc_Sensor SHALL return descriptive error messages with HTTP 400
2. WHEN PDF parsing fails, THE Doc_Sensor SHALL log errors and return HTTP 422 with details
3. WHEN no work experience is found, THE Doc_Sensor SHALL return empty array instead of error
4. WHEN date parsing fails, THE Doc_Sensor SHALL return raw date strings for manual review
5. WHEN CV ID doesn't exist, THE Doc_Sensor SHALL return HTTP 404 with clear message

### Requirement 8

**User Story:** As a data analyst, I want structured JSON output, so that I can integrate CV data into analytics pipelines.

#### Acceptance Criteria

1. WHEN analysis is complete, THE Doc_Sensor SHALL return basic_info with name, email, phone, address, and social links
2. WHEN returning work experience, THE Doc_Sensor SHALL provide array of objects with company, dates, and description
3. WHEN returning skill keywords, THE Doc_Sensor SHALL provide array of strings as skill_keywords with deduplicated skills
4. WHEN returning education, THE Doc_Sensor SHALL provide array of objects with degree, institution, and dates
5. WHEN dates are available, THE Doc_Sensor SHALL format them as ISO 8601 strings (YYYY-MM-DD) or "Present", and use null for missing data
