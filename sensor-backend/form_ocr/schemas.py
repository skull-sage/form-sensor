"""
Pydantic schemas for Form OCR module.
"""

from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class OCROptions(BaseModel):
    """Options for OCR processing."""
    language: str = Field(default="en", description="OCR language code")
    use_gpu: bool = Field(default=False, description="Enable GPU acceleration")
    enable_correction: bool = Field(default=True, description="Apply perspective correction")
    confidence_threshold: float = Field(default=0.5, ge=0.0, le=1.0, description="Minimum confidence score")
    enable_segment_detection: bool = Field(default=True, description="Enable form segment detection")


class TextRegion(BaseModel):
    """Text region extracted from OCR."""
    text: str = Field(description="Extracted text")
    confidence: float = Field(description="Confidence score (0-1)")
    bounding_box: List[List[float]] = Field(description="Bounding box coordinates [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]")


class FormField(BaseModel):
    """Form field with label and value."""
    label: str = Field(description="Field label/name")
    value: Optional[str] = Field(description="Field value (null if empty)")
    layout: str = Field(description="Layout type: 'horizontal' or 'vertical'")
    confidence: float = Field(description="Average confidence score")


class PageResult(BaseModel):
    """Processing result for a single page."""
    page_number: int = Field(description="Page number (1-indexed)")
    original_image: str = Field(description="Original image as base64 string")
    corrected_image: str = Field(description="Corrected image as base64 string")
    correction_applied: bool = Field(description="Whether perspective correction was applied")
    text_regions: List[TextRegion] = Field(description="All extracted text regions")
    form_fields: List[FormField] = Field(description="Detected form fields")


class FormProcessResponse(BaseModel):
    """Response for form processing."""
    form_id: str = Field(description="Unique form identifier")
    page_count: int = Field(description="Number of pages")
    processing_time: float = Field(description="Processing time in seconds")
    pages: List[PageResult] = Field(description="Results for each page")
    metadata: Dict = Field(description="Processing metadata")


class FormDetailResponse(BaseModel):
    """Detailed form information."""
    form_id: str
    filename: str
    upload_date: str
    page_count: int
    processing_status: str  # pending, processing, completed, failed
    results: Optional[FormProcessResponse]


class FormListItem(BaseModel):
    """Form list item."""
    form_id: str
    filename: str
    upload_date: str
    page_count: int
    processing_status: str


class FormListResponse(BaseModel):
    """List of forms."""
    forms: List[FormListItem]
    count: int


class DeleteFormResponse(BaseModel):
    """Form deletion response."""
    message: str


class FormImagesResponse(BaseModel):
    """Form images response."""
    form_id: str
    images: List[Dict]  # [{page_number, original, corrected}]
