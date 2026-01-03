# Form OCR Module

Scanned paper form document processing with perspective correction and OCR.

## Features

- **PDF Upload**: Upload scanned form documents as PDF files (max 20MB)
- **Perspective Correction**: Automatic detection and correction of tilted/angled scans using OpenCV
- **OCR Text Extraction**: Accurate text extraction using PaddleOCR with multilingual support
- **Form Segment Detection**: Identify labels and input fields in different layouts
  - Horizontal layout: label left, input right (with digit boxes for numeric inputs)
  - Vertical layout: label top, input box(es) below
- **Field Extraction**: Extract form data as structured key-value pairs
- **Multi-page Support**: Process forms with multiple pages
- **Confidence Filtering**: Filter low-confidence OCR results
- **GPU Support**: Optional GPU acceleration for faster processing

## API Endpoints

### POST /form-ocr/process-form

Upload and process a form PDF in one step.

**Request:**
- Multipart form data
- `file`: PDF file (required, max 20MB)
- `language`: OCR language code (optional, default: "en")
- `use_gpu`: Enable GPU acceleration (optional, default: false)
- `enable_correction`: Apply perspective correction (optional, default: true)
- `confidence_threshold`: Minimum confidence score 0-1 (optional, default: 0.5)
- `enable_segment_detection`: Enable form segment detection (optional, default: true)

**Response:**
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
        }
      ]
    }
  ],
  "metadata": {
    "ocr_engine": "PaddleOCR",
    "language": "en",
    "use_gpu": false,
    "segment_detection_enabled": true,
    "confidence_threshold": 0.5
  }
}
```

### GET /form-ocr/form/:id

Get form details including processing results.

**Response:**
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

### GET /form-ocr/forms

Get list of all processed forms.

**Response:**
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

### DELETE /form-ocr/form/:id

Delete a form and its processing results.

**Response:**
```json
{
  "message": "Form 'form.pdf' (ID: uuid) deleted successfully"
}
```

### GET /form-ocr/form/:id/images

Get original and corrected images for a form.

**Response:**
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

## Installation

### Python Dependencies

Install required packages:

```bash
cd sensor-backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

Required packages:
- opencv-python
- paddlepaddle
- paddleocr
- pdf2image
- numpy
- Pillow

### System Dependencies

**poppler-utils** is required for PDF to image conversion:

**Ubuntu/Debian:**
```bash
sudo apt-get install poppler-utils
```

**macOS:**
```bash
brew install poppler
```

**Windows:**
Download and install from: https://github.com/oschwartz10612/poppler-windows/releases

### GPU Support (Optional)

For GPU acceleration, install paddlepaddle-gpu instead of paddlepaddle:

```bash
pip uninstall paddlepaddle
pip install paddlepaddle-gpu
```

Requires CUDA-compatible GPU and CUDA toolkit.

## Usage Examples

### Process a Form

```bash
curl -X POST "http://localhost:8000/form-ocr/process-form" \
  -F "file=@form.pdf" \
  -F "language=en" \
  -F "enable_segment_detection=true"
```

### Get Form Details

```bash
curl "http://localhost:8000/form-ocr/form/{form_id}"
```

### List All Forms

```bash
curl "http://localhost:8000/form-ocr/forms"
```

### Delete a Form

```bash
curl -X DELETE "http://localhost:8000/form-ocr/form/{form_id}"
```

## Processing Pipeline

1. **PDF to Images**: Convert PDF pages to numpy arrays using pdf2image
2. **Perspective Correction**: 
   - Convert to grayscale
   - Apply Gaussian blur
   - Detect edges using Canny
   - Find contours and identify form boundary
   - Extract corner points
   - Apply perspective warp to flatten image
3. **OCR Text Extraction**:
   - Initialize PaddleOCR with specified language
   - Process corrected image
   - Extract text with bounding boxes and confidence scores
   - Filter by confidence threshold
4. **Form Segment Detection**:
   - Analyze text region positions
   - Detect horizontal layout (label left, input right)
   - Detect vertical layout (label top, input below)
   - Detect digit boxes for numeric inputs
   - Associate labels with inputs
5. **Field Extraction**: Convert segments to key-value pairs

## Error Handling

- **400 Bad Request**: Invalid file format or parameters
- **413 Payload Too Large**: File exceeds 20MB limit
- **422 Unprocessable Entity**: Corrupted PDF or processing failure
- **404 Not Found**: Form ID not found
- **500 Internal Server Error**: Unexpected processing error

## Performance Considerations

- **GPU Acceleration**: Enable `use_gpu=true` for faster processing (requires GPU)
- **Image Caching**: Processed images are cached in memory
- **OCR Engine Caching**: OCR engines are cached by language and GPU settings
- **Memory Management**: Large forms may require significant memory

## Limitations

- Maximum file size: 20MB
- Perspective correction may fail on forms without clear boundaries
- OCR accuracy depends on image quality and form layout
- Segment detection works best with standard form layouts
- In-memory storage (MVP) - data is lost on server restart

## Module Structure

```
form-ocr/
├── __init__.py              # Module initialization
├── router.py                # API endpoints
├── services.py              # Business logic
├── schemas.py               # Pydantic models
├── validators.py            # Input validation
├── processors/              # Processing utilities
│   ├── __init__.py
│   ├── pdf_processor.py     # PDF to image conversion
│   ├── perspective_corrector.py  # Perspective correction
│   ├── ocr_engine.py        # PaddleOCR wrapper
│   └── segment_detector.py  # Form segment detection
├── README.md                # This file
└── TESTING.md               # Testing guide
```

## Supported Languages

PaddleOCR supports multiple languages:
- `en`: English
- `ch`: Chinese
- `fr`: French
- `german`: German
- `korean`: Korean
- `japan`: Japanese

See PaddleOCR documentation for full language list.

## Notes

- PaddleOCR downloads models on first run (requires internet connection)
- Model files are cached in `~/.paddleocr/`
- First OCR call may be slower due to model initialization
- Subsequent calls reuse cached OCR engines for better performance
