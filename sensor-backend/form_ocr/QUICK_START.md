# Form OCR Module - Quick Start Guide

Get started with the Form OCR module in 5 minutes.

## 1. Install Dependencies

### Create Virtual Environment

```bash
cd sensor-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Python Packages

```bash
pip install -r requirements.txt
```

### System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get install poppler-utils
```

**macOS:**
```bash
brew install poppler
```

**Windows:**
Download from: https://github.com/oschwartz10612/poppler-windows/releases

## 2. Start the Server

```bash
cd sensor-backend

# Activate virtual environment (if not already activated)
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the server
python main.py
```

Or use the convenience script:

```bash
cd sensor-backend
./run.sh  # On Windows: run.bat
```

Server will start at: http://localhost:8000

## 3. Process Your First Form

### Using curl:

```bash
curl -X POST "http://localhost:8000/form-ocr/process-form" \
  -F "file=@your_form.pdf" \
  -F "language=en" \
  -F "enable_segment_detection=true"
```

### Using Python:

```python
import requests

with open("your_form.pdf", "rb") as f:
    response = requests.post(
        "http://localhost:8000/form-ocr/process-form",
        files={"file": f},
        data={
            "language": "en",
            "enable_segment_detection": True
        }
    )

result = response.json()
print(f"Form ID: {result['form_id']}")
print(f"Processing time: {result['processing_time']}s")

# Print extracted fields
for page in result['pages']:
    for field in page['form_fields']:
        print(f"{field['label']}: {field['value']}")
```

## 4. View Results

The response includes:
- **form_id**: Unique identifier for the form
- **pages**: Array of page results
  - **original_image**: Base64 encoded original image
  - **corrected_image**: Base64 encoded corrected image
  - **text_regions**: All extracted text with bounding boxes
  - **form_fields**: Detected label-value pairs

## 5. Retrieve Form Later

```bash
curl "http://localhost:8000/form-ocr/form/{form_id}"
```

## API Endpoints

- `POST /form-ocr/process-form` - Upload and process form
- `GET /form-ocr/form/:id` - Get form details
- `GET /form-ocr/forms` - List all forms
- `GET /form-ocr/form/:id/images` - Get form images
- `DELETE /form-ocr/form/:id` - Delete form

## Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| language | string | "en" | OCR language code |
| use_gpu | boolean | false | Enable GPU acceleration |
| enable_correction | boolean | true | Apply perspective correction |
| confidence_threshold | float | 0.5 | Minimum confidence (0-1) |
| enable_segment_detection | boolean | true | Detect form fields |

## Next Steps

- Read [README.md](README.md) for detailed documentation
- See [TESTING.md](TESTING.md) for testing guide
- Check [ARCHITECTURE.md](../ARCHITECTURE.md) for system architecture

## Troubleshooting

**"poppler not found"**
- Install poppler-utils (see step 1)

**"No text found in PDF"**
- PDF may be image-based
- Check if OCR is working correctly

**"Corner detection failed"**
- Form boundary not clear
- Try with `enable_correction=false`

**Slow processing**
- First run downloads OCR models (one-time)
- Enable GPU with `use_gpu=true` (requires CUDA)

## Support

For issues or questions, see:
- [README.md](README.md) - Full documentation
- [TESTING.md](TESTING.md) - Testing guide
- [../ARCHITECTURE.md](../ARCHITECTURE.md) - System architecture
