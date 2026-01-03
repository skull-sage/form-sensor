# Form OCR Module - Design Document

## Overview

The Form OCR module provides scanned paper form document processing with perspective correction and optical character recognition. The module uses OpenCV for image preprocessing and perspective correction, and PaddleOCR for text extraction, enabling accurate digitization of paper-based forms.

## Module Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Module Router │    │  PDF Converter  │
│   (Vue/Quasar)  │◄──►│   (FastAPI)     │◄──►│   (pdf2image)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  Module Service │
                       │ (Form Processing)│
                       └─────────────────┘
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
            ┌──────────────┐    ┌──────────────┐
            │  Perspective │    │  OCR Engine  │
            │  Corrector   │    │ (PaddleOCR)  │
            │  (OpenCV)    │    └──────────────┘
            └──────────────┘
                    │
                    ▼
            ┌──────────────┐
            │  Data Store  │
            │  (In-Memory) │
            └──────────────┘
```

### Module Structure

```
sensor-backend/
├── form-ocr/                    # Form OCR module
│   ├── __init__.py
│   ├── router.py               # API endpoints with /form-ocr prefix
│   ├── services.py             # FormOCRService business logic
│   ├── schemas.py              # Pydantic models
│   ├── validators.py           # Input validation
│   ├── models.py               # Database models (optional)
│   └── processors/             # Processing utilities
│       ├── __init__.py
│       ├── pdf_processor.py    # PDF to image conversion
│       ├── perspective_corrector.py  # Perspective correction
│       ├── ocr_engine.py       # PaddleOCR wrapper
│       └── segment_detector.py # Form segment detection and field extraction
└── main.py                     # App initialization and module registration
```

## Module Components and Interfaces

### FormOCRService (services.py)
- **Purpose**: Core business logic for form OCR operations
- **Methods**:
  - `upload_form(file) -> dict` - Upload and store form PDF
  - `process_form(file, options) -> dict` - Upload, correct, and extract text in one operation
  - `correct_perspective(form_id: str) -> dict` - Apply perspective correction to form images
  - `extract_text(form_id: str, options) -> dict` - Extract text using OCR
  - `get_form(form_id: str) -> dict` - Retrieve form data and results
  - `get_all_forms() -> list` - List all processed forms
  - `delete_form(form_id: str) -> bool` - Remove form and results

### Module Router (router.py)
- **Purpose**: API endpoints with /form-ocr prefix
- **Endpoints**: See API Endpoints section below

### Validators (validators.py)
- **Purpose**: Input validation functions
- **Functions**:
  - `validate_pdf_file(file) -> bool` - Check file format and size
  - `validate_form_id(form_id: str) -> str` - Validate form ID format
  - `validate_ocr_options(options: dict) -> dict` - Validate OCR parameters

### PDF Processor (processors/pdf_processor.py)
- **Purpose**: Convert PDF pages to images
- **Functions**:
  - `pdf_to_images(pdf_bytes: bytes) -> list[np.ndarray]` - Convert PDF to image array
  - `get_page_count(pdf_bytes: bytes) -> int` - Get number of pages

### Perspective Corrector (processors/perspective_corrector.py)
- **Purpose**: Detect corners and apply perspective warp
- **Functions**:
  - `detect_corners(image: np.ndarray) -> np.ndarray` - Detect four corners of form
  - `apply_perspective_warp(image: np.ndarray, corners: np.ndarray) -> np.ndarray` - Flatten image
  - `correct_image(image: np.ndarray) -> tuple[np.ndarray, bool]` - Full correction pipeline

### OCR Engine (processors/ocr_engine.py)
- **Purpose**: Wrapper for PaddleOCR
- **Functions**:
  - `initialize_ocr(use_gpu: bool, lang: str) -> PaddleOCR` - Initialize OCR engine
  - `extract_text(image: np.ndarray, ocr: PaddleOCR) -> list[dict]` - Extract text with coordinates
  - `filter_by_confidence(results: list, threshold: float) -> list` - Filter low-confidence results

### Form Segment Detector (processors/segment_detector.py)
- **Purpose**: Detect form structure and associate labels with input fields
- **Functions**:
  - `detect_segments(text_regions: list) -> dict` - Identify labels and input fields
  - `detect_horizontal_layout(text_regions: list) -> list[tuple]` - Find label-left, input-right pairs
  - `detect_vertical_layout(text_regions: list) -> list[tuple]` - Find label-top, input-below pairs
  - `detect_digit_boxes(text_regions: list) -> list` - Identify digit input boxes
  - `extract_form_fields(segments: dict) -> list[dict]` - Convert segments to key-value pairs

## API Endpoints

### POST /form-ocr/process-form
- **Input**: Multipart form data with PDF file and optional parameters
- **Output**: 
```json
{
  "form_id": "uuid",
  "page_count": 2,
  "processing_time": 3.45,
  "pages": [
    {
      "page_number": 1,
      "original_image": "base64_string",
      "corrected_image": "base64_string",
      "correction_applied": true,
      "text_regions": [
        {
          "text": "Form Title",
          "confidence": 0.95,
          "bounding_box": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
        }
      ],
      "form_fields": [
        {
          "label": "Name",
          "value": "John Doe",
          "layout": "horizontal",
          "confidence": 0.92
        },
        {
          "label": "Date",
          "value": "2024-01-01",
          "layout": "vertical",
          "confidence": 0.88
        }
      ]
    }
  ],
  "metadata": {
    "ocr_engine": "PaddleOCR",
    "language": "en",
    "use_gpu": false,
    "segment_detection_enabled": true
  }
}
```
- **Process**: Upload PDF → Convert to images → Correct perspective → Extract text → Detect segments → Extract fields → Return results

### GET /form-ocr/form/:id
- **Output**: 
```json
{
  "form_id": "uuid",
  "filename": "form.pdf",
  "upload_date": "2024-01-01T10:00:00Z",
  "page_count": 2,
  "processing_status": "completed",
  "results": { /* processing results */ }
}
```
- **Process**: Retrieve form data and cached results

### GET /form-ocr/forms
- **Output**: 
```json
{
  "forms": [
    {
      "form_id": "uuid",
      "filename": "form.pdf",
      "upload_date": "2024-01-01T10:00:00Z",
      "page_count": 2,
      "processing_status": "completed"
    }
  ],
  "count": 10
}
```
- **Process**: List all stored forms with metadata

### DELETE /form-ocr/form/:id
- **Output**: `{"message": "Form deleted successfully"}`
- **Process**: Remove form images and OCR results

### GET /form-ocr/form/:id/images
- **Output**: 
```json
{
  "form_id": "uuid",
  "images": [
    {
      "page_number": 1,
      "original": "base64_string",
      "corrected": "base64_string"
    }
  ]
}
```
- **Process**: Return original and corrected images

## Data Models

### Form Storage Structure
```python
form_store = {
    "form_id": {
        "id": "uuid",
        "filename": "form.pdf",
        "upload_date": "2024-01-01T10:00:00Z",
        "page_count": 2,
        "file_size": 1024000,
        "processing_status": "completed",  # pending, processing, completed, failed
        "pages": [
            {
                "page_number": 1,
                "original_image": np.ndarray,
                "corrected_image": np.ndarray,
                "correction_applied": true,
                "corners_detected": [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
            }
        ],
        "ocr_results": [
            {
                "page_number": 1,
                "text_regions": [
                    {
                        "text": "Form Title",
                        "confidence": 0.95,
                        "bounding_box": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
                    }
                ]
            }
        ],
        "metadata": {
            "processing_time": 3.45,
            "ocr_engine": "PaddleOCR",
            "language": "en",
            "use_gpu": false
        }
    }
}
```

### API Request/Response Models
```python
class OCROptions(BaseModel):
    language: str = "en"
    use_gpu: bool = False
    enable_correction: bool = True
    confidence_threshold: float = 0.5
    enable_segment_detection: bool = True

class TextRegion(BaseModel):
    text: str
    confidence: float
    bounding_box: List[List[float]]

class FormField(BaseModel):
    label: str
    value: Optional[str]
    layout: str  # "horizontal" or "vertical"
    confidence: float

class PageResult(BaseModel):
    page_number: int
    original_image: str  # base64
    corrected_image: str  # base64
    correction_applied: bool
    text_regions: List[TextRegion]
    form_fields: List[FormField]

class FormProcessResponse(BaseModel):
    form_id: str
    page_count: int
    processing_time: float
    pages: List[PageResult]
    metadata: dict

class FormDetailResponse(BaseModel):
    form_id: str
    filename: str
    upload_date: str
    page_count: int
    processing_status: str
    results: Optional[FormProcessResponse]
```

## Processing Pipeline

### Step 1: PDF to Images
```python
1. Validate PDF file (format, size)
2. Convert PDF pages to numpy arrays using pdf2image
3. Store original images
4. Return image array
```

### Step 2: Perspective Correction
```python
1. Convert image to grayscale
2. Apply Gaussian blur to reduce noise
3. Detect edges using Canny edge detection
4. Find contours in edge-detected image
5. Identify largest rectangular contour (form boundary)
6. Extract four corner points
7. Calculate perspective transformation matrix
8. Apply warpPerspective to flatten image
9. Crop to form boundaries
10. Return corrected image and corners
```

**Corner Detection Algorithm:**
```python
def detect_corners(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Edge detection
    edges = cv2.Canny(blurred, 50, 150)
    
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Find largest rectangular contour
    for contour in sorted(contours, key=cv2.contourArea, reverse=True):
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        
        if len(approx) == 4:
            return approx.reshape(4, 2)
    
    return None
```

### Step 3: OCR Text Extraction
```python
1. Initialize PaddleOCR with specified language and GPU settings
2. Process corrected image through OCR engine
3. Extract text regions with bounding boxes and confidence scores
4. Filter results by confidence threshold
5. Format results as structured data
6. Return text regions array
```

### Step 4: Form Segment Detection and Field Extraction
```python
1. Analyze text region positions and bounding boxes
2. Detect horizontal layout patterns:
   - Find text regions on left side (labels)
   - Find corresponding regions on right side (inputs)
   - Associate labels with inputs based on vertical alignment
3. Detect vertical layout patterns:
   - Find text regions on top (labels)
   - Find corresponding regions below (inputs)
   - Associate labels with inputs based on horizontal alignment
4. Detect digit boxes:
   - Identify small rectangular regions in sequence
   - Group digit boxes for same field
5. Extract form fields as key-value pairs
6. Return structured form_fields array
```

**Segment Detection Algorithm:**
```python
def detect_segments(text_regions):
    labels = []
    inputs = []
    
    # Sort regions by position
    sorted_regions = sorted(text_regions, key=lambda r: (r['bbox'][0][1], r['bbox'][0][0]))
    
    for region in sorted_regions:
        bbox = region['bounding_box']
        text = region['text']
        
        # Heuristics to classify as label or input
        # Labels typically: longer text, left-aligned or top-aligned
        # Inputs typically: shorter text, right-aligned or below labels
        
        if is_label(region):
            labels.append(region)
        else:
            inputs.append(region)
    
    # Associate labels with inputs
    fields = []
    
    # Horizontal layout: label left, input right
    for label in labels:
        for input_region in inputs:
            if is_horizontally_aligned(label, input_region):
                fields.append({
                    'label': label['text'],
                    'value': input_region['text'],
                    'layout': 'horizontal'
                })
    
    # Vertical layout: label top, input below
    for label in labels:
        for input_region in inputs:
            if is_vertically_aligned(label, input_region):
                fields.append({
                    'label': label['text'],
                    'value': input_region['text'],
                    'layout': 'vertical'
                })
    
    return fields

def is_horizontally_aligned(label, input_region):
    # Check if input is to the right of label and vertically aligned
    label_y = label['bounding_box'][0][1]
    input_y = input_region['bounding_box'][0][1]
    label_x = label['bounding_box'][1][0]
    input_x = input_region['bounding_box'][0][0]
    
    vertical_threshold = 20  # pixels
    horizontal_gap = 50  # pixels
    
    return (abs(label_y - input_y) < vertical_threshold and 
            input_x > label_x and 
            input_x - label_x < horizontal_gap)

def is_vertically_aligned(label, input_region):
    # Check if input is below label and horizontally aligned
    label_x = label['bounding_box'][0][0]
    input_x = input_region['bounding_box'][0][0]
    label_y = label['bounding_box'][2][1]
    input_y = input_region['bounding_box'][0][1]
    
    horizontal_threshold = 20  # pixels
    vertical_gap = 50  # pixels
    
    return (abs(label_x - input_x) < horizontal_threshold and 
            input_y > label_y and 
            input_y - label_y < vertical_gap)
```

## Error Handling

### File Upload Errors
- Invalid file format (not PDF) → 400 Bad Request
- File too large (> 20MB) → 413 Payload Too Large
- Corrupted PDF → 422 Unprocessable Entity

### Processing Errors
- PDF conversion failure → 422 Unprocessable Entity
- Corner detection failure → Continue with original image, log warning
- OCR failure → Return empty results with error details
- Processing timeout → 504 Gateway Timeout

### Query Errors
- Form ID not found → 404 Not Found
- Invalid form ID format → 400 Bad Request

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: PDF Upload Validation
*For any* uploaded file, if the file is not a valid PDF or exceeds size limits, the system should reject it with appropriate error
**Validates: Requirements 1.1, 1.5**
**Module: form-ocr**

### Property 2: Image Conversion Completeness
*For any* valid PDF file, image conversion should return array with length equal to page count
**Validates: Requirements 1.2**
**Module: form-ocr**

### Property 3: Perspective Correction Idempotence
*For any* corrected image, applying perspective correction again should return similar image (correction is idempotent)
**Validates: Requirements 2.3**
**Module: form-ocr**

### Property 4: OCR Confidence Filtering
*For any* OCR results with confidence threshold T, all returned text regions should have confidence >= T
**Validates: Requirements 3.3, 9.4**
**Module: form-ocr**

### Property 5: Bounding Box Validity
*For any* text region, bounding box should contain exactly 4 points with valid coordinates
**Validates: Requirements 3.2**
**Module: form-ocr**

### Property 6: Processing Status Consistency
*For any* form, processing_status should be one of: pending, processing, completed, failed
**Validates: Requirements 4.4, 8.1**
**Module: form-ocr**

### Property 7: Page Count Consistency
*For any* processed form, number of page results should equal page_count
**Validates: Requirements 8.1, 8.2**
**Module: form-ocr**

### Property 8: Error Response Format
*For any* error condition, the API should return appropriate HTTP status code with descriptive message
**Validates: Requirements 7.1, 7.2, 7.5**
**Module: form-ocr**

## Testing Strategy

### Unit Testing Approach
Unit tests will verify specific examples and edge cases:
- PDF validation with various file types
- Image conversion from sample PDFs
- Corner detection with different form orientations
- OCR extraction with sample images
- API endpoint request/response validation

### Integration Testing Approach
Integration tests will verify end-to-end workflows:
- Upload form → Process → Retrieve results
- Multiple form uploads and management
- Error handling for invalid inputs
- Edge cases (rotated forms, poor quality scans)

### Test Data
- Sample form PDFs with various orientations
- Forms with different layouts
- Poor quality scans
- Multi-page forms

**Configuration**: Each test will use realistic form samples to ensure processing accuracy.

Both unit tests and integration tests are complementary - unit tests verify individual processing functions while integration tests verify the complete form OCR pipeline.

## Dependencies

### Python Packages
- **opencv-python** - Image processing and perspective correction
- **paddlepaddle** - PaddleOCR backend
- **paddleocr** - OCR engine
- **pdf2image** - PDF to image conversion
- **numpy** - Array operations
- **Pillow** - Image manipulation

### System Dependencies
- **poppler-utils** - Required by pdf2image for PDF conversion

## Performance Considerations

- **GPU Acceleration**: Optional GPU support for faster OCR processing
- **Image Caching**: Store processed images to avoid reprocessing
- **Async Processing**: Consider async processing for large documents
- **Memory Management**: Release image arrays after processing to prevent memory leaks
