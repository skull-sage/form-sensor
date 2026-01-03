"""
Business logic services for Form OCR operations.
"""

import uuid
import time
from datetime import datetime
from typing import Dict
from fastapi import HTTPException, UploadFile

from .validators import validate_pdf_file, validate_file_size, validate_form_id, validate_ocr_options
from .schemas import OCROptions, TextRegion, FormField, PageResult, FormProcessResponse
from .processors.pdf_processor import pdf_to_images, get_page_count, numpy_to_base64
from .processors.perspective_corrector import correct_image
from .processors.ocr_engine import initialize_ocr, extract_text, filter_by_confidence
from .processors.segment_detector import detect_segments, extract_form_fields


class FormOCRService:
    """Service class for Form OCR operations."""
    
    def __init__(self, form_store: dict):
        """
        Initialize the Form OCR service.
        
        Args:
            form_store: Dictionary for storing form data in memory
        """
        self.form_store = form_store
        self.ocr_engines = {}  # Cache OCR engines by (use_gpu, language)
    
    def _get_ocr_engine(self, use_gpu: bool, language: str):
        """Get or create OCR engine with caching."""
        cache_key = (use_gpu, language)
        if cache_key not in self.ocr_engines:
            self.ocr_engines[cache_key] = initialize_ocr(use_gpu, language)
        return self.ocr_engines[cache_key]
    
    async def process_form(self, file: UploadFile, options: OCROptions) -> FormProcessResponse:
        """
        Process form PDF: upload, correct perspective, extract text, detect segments.
        
        Args:
            file: Uploaded PDF file
            options: OCR processing options
            
        Returns:
            FormProcessResponse: Complete processing results
            
        Raises:
            HTTPException: If validation or processing fails
        """
        start_time = time.time()
        
        # Validate file
        validate_pdf_file(file)
        
        # Read file content
        file_content = await file.read()
        
        # Validate file size (20MB)
        validate_file_size(len(file_content), max_size=20 * 1024 * 1024)
        
        # Validate OCR options
        validate_ocr_options(options.model_dump())
        
        # Convert PDF to images
        try:
            images = pdf_to_images(file_content)
            page_count = len(images)
        except Exception as e:
            raise HTTPException(
                status_code=422,
                detail=f"Failed to process PDF: {str(e)}"
            )
        
        if not images:
            raise HTTPException(
                status_code=422,
                detail="No pages found in PDF. The PDF may be corrupted."
            )
        
        # Generate form ID
        form_id = str(uuid.uuid4())
        
        # Initialize OCR engine
        try:
            ocr = self._get_ocr_engine(options.use_gpu, options.language)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize OCR engine: {str(e)}"
            )
        
        # Process each page
        pages_data = []
        page_results = []
        
        for page_num, original_image in enumerate(images, start=1):
            # Apply perspective correction if enabled
            corrected_image = original_image
            correction_applied = False
            
            if options.enable_correction:
                try:
                    corrected_image, correction_applied = correct_image(original_image)
                except Exception as e:
                    # Log warning but continue with original image
                    print(f"Warning: Perspective correction failed for page {page_num}: {str(e)}")
                    corrected_image = original_image
                    correction_applied = False
            
            # Extract text using OCR
            try:
                text_regions_raw = extract_text(corrected_image, ocr)
                # Filter by confidence threshold
                text_regions_filtered = filter_by_confidence(
                    text_regions_raw, 
                    options.confidence_threshold
                )
            except Exception as e:
                # Log error but continue with empty results
                print(f"Warning: OCR failed for page {page_num}: {str(e)}")
                text_regions_filtered = []
            
            # Convert to TextRegion schema
            text_regions = [
                TextRegion(
                    text=region["text"],
                    confidence=region["confidence"],
                    bounding_box=region["bounding_box"]
                )
                for region in text_regions_filtered
            ]
            
            # Detect form segments and extract fields if enabled
            form_fields = []
            if options.enable_segment_detection and text_regions_filtered:
                try:
                    segments = detect_segments(text_regions_filtered)
                    fields_raw = extract_form_fields(segments)
                    form_fields = [
                        FormField(
                            label=field["label"],
                            value=field.get("value"),
                            layout=field["layout"],
                            confidence=field["confidence"]
                        )
                        for field in fields_raw
                    ]
                except Exception as e:
                    # Log error but continue with empty fields
                    print(f"Warning: Segment detection failed for page {page_num}: {str(e)}")
                    form_fields = []
            
            # Convert images to base64
            original_base64 = numpy_to_base64(original_image)
            corrected_base64 = numpy_to_base64(corrected_image)
            
            # Create page result
            page_result = PageResult(
                page_number=page_num,
                original_image=original_base64,
                corrected_image=corrected_base64,
                correction_applied=correction_applied,
                text_regions=text_regions,
                form_fields=form_fields
            )
            
            page_results.append(page_result)
            
            # Store page data for later retrieval
            pages_data.append({
                "page_number": page_num,
                "original_image": original_image,
                "corrected_image": corrected_image,
                "correction_applied": correction_applied,
                "text_regions": text_regions_filtered,
                "form_fields": [field.model_dump() for field in form_fields]
            })
        
        processing_time = time.time() - start_time
        
        # Create metadata
        metadata = {
            "ocr_engine": "EasyOCR",
            "language": options.language,
            "use_gpu": options.use_gpu,
            "segment_detection_enabled": options.enable_segment_detection,
            "confidence_threshold": options.confidence_threshold
        }
        
        # Store form data
        self.form_store[form_id] = {
            "id": form_id,
            "filename": file.filename,
            "upload_date": datetime.utcnow().isoformat() + "Z",
            "page_count": page_count,
            "file_size": len(file_content),
            "processing_status": "completed",
            "pages": pages_data,
            "metadata": metadata,
            "processing_time": processing_time
        }
        
        # Create response
        response = FormProcessResponse(
            form_id=form_id,
            page_count=page_count,
            processing_time=round(processing_time, 2),
            pages=page_results,
            metadata=metadata
        )
        
        return response
    
    def get_form(self, form_id: str) -> Dict:
        """
        Get form details including processing results.
        
        Args:
            form_id: Form identifier
            
        Returns:
            dict: Complete form data
            
        Raises:
            HTTPException: If form not found
        """
        validated_form_id = validate_form_id(form_id)
        
        if validated_form_id not in self.form_store:
            raise HTTPException(
                status_code=404,
                detail=f"Form with ID '{validated_form_id}' not found"
            )
        
        form_data = self.form_store[validated_form_id]
        
        # Convert stored data to response format
        page_results = []
        for page_data in form_data["pages"]:
            text_regions = [
                TextRegion(
                    text=region["text"],
                    confidence=region["confidence"],
                    bounding_box=region["bounding_box"]
                )
                for region in page_data["text_regions"]
            ]
            
            form_fields = [
                FormField(**field)
                for field in page_data["form_fields"]
            ]
            
            page_result = PageResult(
                page_number=page_data["page_number"],
                original_image=numpy_to_base64(page_data["original_image"]),
                corrected_image=numpy_to_base64(page_data["corrected_image"]),
                correction_applied=page_data["correction_applied"],
                text_regions=text_regions,
                form_fields=form_fields
            )
            page_results.append(page_result)
        
        results = FormProcessResponse(
            form_id=form_data["id"],
            page_count=form_data["page_count"],
            processing_time=form_data["processing_time"],
            pages=page_results,
            metadata=form_data["metadata"]
        )
        
        return {
            "form_id": form_data["id"],
            "filename": form_data["filename"],
            "upload_date": form_data["upload_date"],
            "page_count": form_data["page_count"],
            "processing_status": form_data["processing_status"],
            "results": results
        }
    
    def get_all_forms(self) -> Dict:
        """
        Get list of all processed forms.
        
        Returns:
            dict: List of forms with metadata and count
        """
        forms = []
        
        for form_id, form_data in self.form_store.items():
            forms.append({
                "form_id": form_id,
                "filename": form_data["filename"],
                "upload_date": form_data["upload_date"],
                "page_count": form_data["page_count"],
                "processing_status": form_data["processing_status"]
            })
        
        # Sort by upload date (most recent first)
        forms.sort(key=lambda x: x["upload_date"], reverse=True)
        
        return {
            "forms": forms,
            "count": len(forms)
        }
    
    def delete_form(self, form_id: str) -> Dict:
        """
        Delete form and its processing results.
        
        Args:
            form_id: Form identifier
            
        Returns:
            dict: Deletion confirmation message
            
        Raises:
            HTTPException: If form not found
        """
        validated_form_id = validate_form_id(form_id)
        
        if validated_form_id not in self.form_store:
            raise HTTPException(
                status_code=404,
                detail=f"Form with ID '{validated_form_id}' not found"
            )
        
        filename = self.form_store[validated_form_id]["filename"]
        del self.form_store[validated_form_id]
        
        return {
            "message": f"Form '{filename}' (ID: {validated_form_id}) deleted successfully"
        }
    
    def get_form_images(self, form_id: str) -> Dict:
        """
        Get original and corrected images for a form.
        
        Args:
            form_id: Form identifier
            
        Returns:
            dict: Images as base64 strings for each page
            
        Raises:
            HTTPException: If form not found
        """
        validated_form_id = validate_form_id(form_id)
        
        if validated_form_id not in self.form_store:
            raise HTTPException(
                status_code=404,
                detail=f"Form with ID '{validated_form_id}' not found"
            )
        
        form_data = self.form_store[validated_form_id]
        
        images = []
        for page_data in form_data["pages"]:
            images.append({
                "page_number": page_data["page_number"],
                "original": numpy_to_base64(page_data["original_image"]),
                "corrected": numpy_to_base64(page_data["corrected_image"])
            })
        
        return {
            "form_id": validated_form_id,
            "images": images
        }
