# Form OCR Module - Implementation Plan

## Module: form-ocr
**Purpose**: Scanned paper form document processing with perspective correction and OCR

## Implementation Tasks

- [x] 1. Set up module structure and dependencies
  - [x] 1.1 Create form-ocr module folder structure
    - Create __init__.py, router.py, services.py, schemas.py, validators.py
    - Create processors/ subfolder with __init__.py
    - _Requirements: 5.1_
  
  - [x] 1.2 Install dependencies
    - Add opencv-python to requirements.txt
    - Add paddlepaddle and paddleocr to requirements.txt
    - Add pdf2image to requirements.txt
    - Add numpy and Pillow to requirements.txt
    - Document system dependency: poppler-utils
    - _Requirements: 1.2, 2.1, 3.1_

- [x] 2. Implement PDF to image conversion
  - [x] 2.1 Create pdf_processor.py in processors/
    - Implement pdf_to_images(pdf_bytes) function
    - Handle multi-page PDFs
    - Handle corrupted PDFs with error messages
    - Return list of numpy arrays
    - _Requirements: 1.2_
  
  - [x] 2.2 Create file validators
    - Implement validate_pdf_file(file) in validators.py
    - Check file extension is .pdf
    - Validate file size <= 20MB
    - Return descriptive error messages
    - _Requirements: 1.1, 1.5_

- [x] 3. Implement perspective correction
  - [x] 3.1 Create perspective_corrector.py in processors/
    - Implement detect_corners(image) function using OpenCV
    - Apply Gaussian blur and Canny edge detection
    - Find contours and identify largest rectangular contour
    - Extract four corner points
    - _Requirements: 2.1_
  
  - [x] 3.2 Implement perspective warp
    - Create apply_perspective_warp(image, corners) function
    - Calculate perspective transformation matrix
    - Apply warpPerspective to flatten image
    - Crop to form boundaries
    - _Requirements: 2.2, 2.3, 2.4_
  
  - [x] 3.3 Create correction pipeline
    - Implement correct_image(image) function
    - Combine corner detection and warping
    - Handle corner detection failures gracefully
    - Return corrected image and success flag
    - _Requirements: 2.5_

- [x] 4. Implement OCR text extraction
  - [x] 4.1 Create ocr_engine.py in processors/
    - Implement initialize_ocr(use_gpu, lang) function
    - Wrap PaddleOCR initialization
    - Handle GPU availability
    - _Requirements: 3.1, 9.1, 9.2_
  
  - [x] 4.2 Implement text extraction
    - Create extract_text(image, ocr) function
    - Process image through PaddleOCR
    - Extract text with bounding boxes and confidence scores
    - Format results as structured data
    - _Requirements: 3.2, 3.3_
  
  - [x] 4.3 Implement confidence filtering
    - Create filter_by_confidence(results, threshold) function
    - Filter low-confidence results
    - Return filtered text regions
    - _Requirements: 3.3, 9.4_

- [x] 5. Implement form segment detection and field extraction
  - [ ] 5.1 Create segment_detector.py in processors/
    - Implement detect_segments(text_regions) function
    - Classify text regions as labels or inputs
    - _Requirements: 10.1_
  
  - [ ] 5.2 Implement horizontal layout detection
    - Create detect_horizontal_layout(text_regions) function
    - Find label-left, input-right pairs
    - Check vertical alignment
    - _Requirements: 10.2_
  
  - [ ] 5.3 Implement vertical layout detection
    - Create detect_vertical_layout(text_regions) function
    - Find label-top, input-below pairs
    - Check horizontal alignment
    - _Requirements: 10.3_
  
  - [ ] 5.4 Implement digit box detection
    - Create detect_digit_boxes(text_regions) function
    - Identify small rectangular regions in sequence
    - Group digit boxes for same field
    - _Requirements: 10.4_
  
  - [ ] 5.5 Implement field extraction
    - Create extract_form_fields(segments) function
    - Convert segments to key-value pairs
    - Associate labels with inputs
    - Handle empty input fields
    - _Requirements: 10.5, 11.1, 11.2, 11.3, 11.4, 11.5_

- [ ] 6. Implement form processing endpoint
  - [ ] 6.1 Create POST /form-ocr/process-form endpoint
    - Accept multipart form data with PDF file
    - Accept optional OCR parameters (language, use_gpu, enable_segment_detection, etc.)
    - Validate file and parameters
    - Convert PDF to images
    - Apply perspective correction to each page
    - Extract text using OCR
    - Detect form segments and extract fields
    - Generate unique form ID
    - Store all results
    - Return FormProcessResponse with form_fields
    - _Requirements: 1.1, 1.2, 2.1-2.5, 3.1-3.5, 4.1-4.5, 10.1-10.5, 11.1-11.5_
  
  - [ ] 6.2 Create response schemas
    - Define OCROptions in schemas.py (add enable_segment_detection)
    - Define TextRegion model
    - Define FormField model
    - Define PageResult model (add form_fields)
    - Define FormProcessResponse model
    - _Requirements: 4.2, 8.1, 8.2, 8.3, 8.4, 11.3_

- [ ] 7. Implement form management endpoints
  - [ ] 7.1 Create GET /form-ocr/form/:id endpoint
    - Return full form data and OCR results
    - _Requirements: 5.2_
  
  - [ ] 7.2 Create GET /form-ocr/forms endpoint
    - Return list of all forms with metadata
    - _Requirements: 5.3_
  
  - [ ] 7.3 Create DELETE /form-ocr/form/:id endpoint
    - Remove form from storage
    - _Requirements: 5.4_
  
  - [ ] 6.4 Create GET /form-ocr/form/:id/images endpoint
    - Return original and corrected images
    - _Requirements: 5.5_
  
  - [ ] 6.5 Create response schemas
    - Define FormDetailResponse
    - Define FormListResponse
    - Define DeleteFormResponse
    - Define FormImagesResponse
    - _Requirements: 5.2, 5.3, 5.4, 5.5_

- [ ] 7. Implement error handling
  - [ ] 7.1 Add file validation error handling
    - Return 400 for invalid formats
    - Return 413 for large files
    - Return 422 for corrupted PDFs
    - _Requirements: 7.1, 7.2_
  
  - [ ] 7.2 Add processing error handling
    - Handle PDF conversion failures
    - Handle corner detection failures (continue with warning)
    - Handle OCR failures (return empty results)
    - _Requirements: 7.2, 7.3, 7.4_
  
  - [ ] 7.3 Add form not found error handling
    - Return 404 when form_id doesn't exist
    - _Requirements: 7.5_

- [ ] 8. Implement FormOCRService
  - [ ] 8.1 Create FormOCRService class
    - Implement process_form() method (combined operation)
    - Implement upload_form() method (separate upload)
    - Implement correct_perspective() method
    - Implement extract_text() method
    - Implement get_form() method
    - Implement get_all_forms() method
    - Implement delete_form() method
    - Implement get_form_images() method
    - _Requirements: All_
  
  - [ ] 8.2 Initialize service in main.py
    - Create form_store dictionary
    - Initialize FormOCRService
    - Set service in router using set_service()
    - Include router with /form-ocr prefix
    - _Requirements: 5.1_

- [ ] 9. Create documentation
  - [ ] 9.1 Create README.md
    - Module overview and features
    - API endpoint documentation
    - Usage examples
    - Installation instructions for system dependencies
  
  - [ ] 9.2 Create TESTING.md
    - Testing instructions
    - Sample curl commands
    - Expected responses
    - Sample form PDFs for testing

- [ ] 10. Implement frontend components
  - [ ] 10.1 Create form-upload.vue component
    - File upload form with file picker
    - File validation (PDF only, max 20MB)
    - Processing progress indicator
    - Success/error messages
    - _Requirements: 6.1, 6.2_
  
  - [ ] 10.2 Create form-results.vue component
    - Display original and corrected images side-by-side
    - Show extracted text with confidence scores
    - Highlight text regions on images
    - Download buttons for images and text
    - _Requirements: 6.3, 6.4, 6.5, 10.1-10.5_
  
  - [ ] 10.3 Create form-list.vue component
    - Display list of processed forms
    - Show processing status
    - View, download, delete buttons
    - _Requirements: 6.1_
  
  - [ ] 10.4 Create route configuration
    - Create route-config.ts
    - Define routes: /form-ocr/upload, /form-ocr/list
    - Register in main router
    - _Requirements: 6.1_

- [ ] 11. Testing and validation
  - [ ] 11.1 Create test form samples
    - Prepare sample form PDFs with various orientations
    - Include poor quality scans
    - Include multi-page forms
    - _Requirements: All_
  
  - [ ] 11.2 Test complete workflow
    - Upload and process sample forms
    - Verify perspective correction accuracy
    - Verify OCR extraction accuracy
    - Test error handling
    - _Requirements: All_
  
  - [ ] 11.3 Verify data structure compliance
    - Ensure responses match schemas
    - Verify bounding box formats
    - Check confidence score ranges
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

## Implementation Summary

### To Be Implemented
**Backend:**
- Module structure with router, services, schemas, validators, processors
- PDF to image conversion with pdf2image
- Perspective correction with OpenCV (corner detection, perspective warp)
- OCR text extraction with PaddleOCR
- **Form segment detection and field extraction** (NEW)
  - Horizontal layout detection (label left, input right)
  - Vertical layout detection (label top, input below)
  - Digit box detection for numeric inputs
  - Label-value association
- Combined processing endpoint (POST /form-ocr/process-form)
- Form management endpoints (GET, DELETE)
- Error handling and validation
- In-memory storage (MVP)
- Documentation (README.md, TESTING.md)

**Frontend:**
- Route configuration and registration
- Main container with tab navigation
- Form upload and processing component
- Results display with image comparison
- **Form fields display as key-value pairs** (NEW)
- Form library and management component
- Download functionality

### Key Features
- **Perspective Correction**: Automatic detection and correction of tilted/angled scans
- **OCR Engine**: PaddleOCR for accurate text extraction
- **Form Segment Detection**: Identify labels and input fields in different layouts (NEW)
- **Field Extraction**: Extract form data as structured key-value pairs (NEW)
- **Multi-page Support**: Process forms with multiple pages
- **Confidence Filtering**: Filter low-confidence OCR results
- **GPU Support**: Optional GPU acceleration for faster processing

## Design Decisions

1. **OpenCV for perspective correction**: Industry-standard library with robust corner detection
2. **PaddleOCR**: Open-source, multilingual OCR with good accuracy
3. **Combined endpoint**: Single API call for upload, correction, and OCR (simpler workflow)
4. **Base64 images**: Return images as base64 strings for easy frontend display
5. **In-memory storage**: MVP approach, can be replaced with database + file storage

## Notes

- System dependency: poppler-utils must be installed for pdf2image
- PaddleOCR downloads models on first run (requires internet connection)
- GPU support requires CUDA-compatible GPU and paddlepaddle-gpu
- Perspective correction may fail on forms without clear boundaries
- OCR accuracy depends on image quality and form layout
