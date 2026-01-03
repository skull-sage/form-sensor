# Form OCR Module - Testing Guide

This guide provides instructions for testing the Form OCR module.

## Prerequisites

1. **Backend server running**:
   ```bash
   cd sensor-backend
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   python main.py
   ```

2. **System dependencies installed**:
   - poppler-utils (for PDF conversion)

3. **Sample form PDFs** (see Sample Forms section below)

## Testing Endpoints

### 1. Process Form (Combined Operation)

Upload and process a form in one step:

```bash
curl -X POST "http://localhost:8000/form-ocr/process-form" \
  -F "file=@sample_form.pdf" \
  -F "language=en" \
  -F "use_gpu=false" \
  -F "enable_correction=true" \
  -F "confidence_threshold=0.5" \
  -F "enable_segment_detection=true"
```

**Expected Response:**
```json
{
  "form_id": "550e8400-e29b-41d4-a716-446655440000",
  "page_count": 1,
  "processing_time": 2.34,
  "pages": [
    {
      "page_number": 1,
      "original_image": "base64_encoded_image...",
      "corrected_image": "base64_encoded_image...",
      "correction_applied": true,
      "text_regions": [
        {
          "text": "Name",
          "confidence": 0.95,
          "bounding_box": [[10, 20], [100, 20], [100, 40], [10, 40]]
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

### 2. Get Form Details

Retrieve form data and processing results:

```bash
curl "http://localhost:8000/form-ocr/form/550e8400-e29b-41d4-a716-446655440000"
```

**Expected Response:**
```json
{
  "form_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "sample_form.pdf",
  "upload_date": "2024-01-01T10:00:00Z",
  "page_count": 1,
  "processing_status": "completed",
  "results": {
    "form_id": "550e8400-e29b-41d4-a716-446655440000",
    "page_count": 1,
    "processing_time": 2.34,
    "pages": [ /* page results */ ],
    "metadata": { /* processing metadata */ }
  }
}
```

### 3. List All Forms

Get list of all processed forms:

```bash
curl "http://localhost:8000/form-ocr/forms"
```

**Expected Response:**
```json
{
  "forms": [
    {
      "form_id": "550e8400-e29b-41d4-a716-446655440000",
      "filename": "sample_form.pdf",
      "upload_date": "2024-01-01T10:00:00Z",
      "page_count": 1,
      "processing_status": "completed"
    }
  ],
  "count": 1
}
```

### 4. Get Form Images

Retrieve original and corrected images:

```bash
curl "http://localhost:8000/form-ocr/form/550e8400-e29b-41d4-a716-446655440000/images"
```

**Expected Response:**
```json
{
  "form_id": "550e8400-e29b-41d4-a716-446655440000",
  "images": [
    {
      "page_number": 1,
      "original": "base64_encoded_image...",
      "corrected": "base64_encoded_image..."
    }
  ]
}
```

### 5. Delete Form

Remove form and its results:

```bash
curl -X DELETE "http://localhost:8000/form-ocr/form/550e8400-e29b-41d4-a716-446655440000"
```

**Expected Response:**
```json
{
  "message": "Form 'sample_form.pdf' (ID: 550e8400-e29b-41d4-a716-446655440000) deleted successfully"
}
```

## Error Testing

### Invalid File Format

```bash
curl -X POST "http://localhost:8000/form-ocr/process-form" \
  -F "file=@document.txt"
```

**Expected Response:** 400 Bad Request
```json
{
  "detail": "Only PDF files are allowed"
}
```

### File Too Large

Upload a file larger than 20MB.

**Expected Response:** 413 Payload Too Large
```json
{
  "detail": "File too large. Maximum size is 20MB"
}
```

### Invalid Form ID

```bash
curl "http://localhost:8000/form-ocr/form/invalid-id"
```

**Expected Response:** 400 Bad Request
```json
{
  "detail": "Invalid form ID format. Expected UUID, got 'invalid-id'"
}
```

### Form Not Found

```bash
curl "http://localhost:8000/form-ocr/form/00000000-0000-0000-0000-000000000000"
```

**Expected Response:** 404 Not Found
```json
{
  "detail": "Form with ID '00000000-0000-0000-0000-000000000000' not found"
}
```

### Invalid Confidence Threshold

```bash
curl -X POST "http://localhost:8000/form-ocr/process-form" \
  -F "file=@sample_form.pdf" \
  -F "confidence_threshold=1.5"
```

**Expected Response:** 400 Bad Request
```json
{
  "detail": "Confidence threshold must be between 0 and 1"
}
```

## Sample Forms

### Creating Test Forms

You can create test forms using various methods:

1. **Scan a physical form** using a scanner or phone camera
2. **Create a digital form** in Word/Google Docs and print to PDF
3. **Use online form generators** to create sample forms

### Recommended Test Cases

1. **Standard Form** - Clean scan with clear text
2. **Tilted Form** - Scanned at an angle (tests perspective correction)
3. **Poor Quality Scan** - Low resolution or faded text (tests OCR robustness)
4. **Multi-page Form** - Form with multiple pages
5. **Horizontal Layout** - Labels on left, inputs on right
6. **Vertical Layout** - Labels on top, inputs below
7. **Mixed Layout** - Combination of horizontal and vertical layouts
8. **Digit Boxes** - Forms with individual boxes for each digit

### Sample Form Structure

**Horizontal Layout Example:**
```
Name: ____________    Date: __________
Email: ___________    Phone: _________
```

**Vertical Layout Example:**
```
Address:
_______________________________________

City:
_______________________________________
```

**Digit Boxes Example:**
```
ID Number: [_][_][_][_][_][_]
```

## Testing Checklist

- [ ] Upload and process a standard form
- [ ] Verify perspective correction on tilted scan
- [ ] Test OCR accuracy on clear text
- [ ] Test OCR on poor quality scan
- [ ] Process multi-page form
- [ ] Verify horizontal layout detection
- [ ] Verify vertical layout detection
- [ ] Test digit box detection
- [ ] Verify form field extraction (label-value pairs)
- [ ] Test confidence filtering with different thresholds
- [ ] Retrieve form details
- [ ] List all forms
- [ ] Get form images
- [ ] Delete form
- [ ] Test error handling (invalid file, too large, etc.)
- [ ] Test with different languages (if applicable)
- [ ] Test GPU acceleration (if available)

## Performance Testing

### Measure Processing Time

```bash
time curl -X POST "http://localhost:8000/form-ocr/process-form" \
  -F "file=@sample_form.pdf" \
  -F "language=en"
```

### Expected Performance

- **Single page form**: 2-5 seconds (CPU)
- **Single page form**: 1-2 seconds (GPU)
- **Multi-page form**: 3-10 seconds (CPU)
- **Multi-page form**: 2-5 seconds (GPU)

Performance depends on:
- Image resolution
- Text density
- Hardware specifications
- GPU availability

## Debugging

### Enable Debug Logging

Add logging to see processing details:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check OCR Model Download

PaddleOCR downloads models on first run. Check `~/.paddleocr/` directory for model files.

### Verify System Dependencies

```bash
# Check poppler-utils
pdftoppm -v

# Check Python packages
pip list | grep -E "opencv|paddle|pdf2image"
```

### Common Issues

1. **"poppler not found"**: Install poppler-utils
2. **"No text found"**: PDF may be image-based, check OCR settings
3. **"Corner detection failed"**: Form boundary not clear, disable correction
4. **"OCR failed"**: Check PaddleOCR installation and model download
5. **"Memory error"**: Reduce image resolution or process fewer pages

## Integration Testing

### Test Complete Workflow

```bash
# 1. Process form
FORM_ID=$(curl -X POST "http://localhost:8000/form-ocr/process-form" \
  -F "file=@sample_form.pdf" | jq -r '.form_id')

# 2. Get form details
curl "http://localhost:8000/form-ocr/form/$FORM_ID"

# 3. Get form images
curl "http://localhost:8000/form-ocr/form/$FORM_ID/images"

# 4. List all forms
curl "http://localhost:8000/form-ocr/forms"

# 5. Delete form
curl -X DELETE "http://localhost:8000/form-ocr/form/$FORM_ID"
```

## Automated Testing

### Python Test Script

```python
import requests

BASE_URL = "http://localhost:8000/form-ocr"

# Process form
with open("sample_form.pdf", "rb") as f:
    response = requests.post(
        f"{BASE_URL}/process-form",
        files={"file": f},
        data={
            "language": "en",
            "enable_segment_detection": True
        }
    )
    assert response.status_code == 200
    form_id = response.json()["form_id"]
    print(f"Form processed: {form_id}")

# Get form details
response = requests.get(f"{BASE_URL}/form/{form_id}")
assert response.status_code == 200
print("Form details retrieved")

# Delete form
response = requests.delete(f"{BASE_URL}/form/{form_id}")
assert response.status_code == 200
print("Form deleted")
```

## Notes

- First OCR call may be slower due to model initialization
- Subsequent calls reuse cached OCR engines
- In-memory storage means data is lost on server restart
- Base64 images can be large - consider pagination for production
- Test with various form layouts to verify segment detection accuracy
