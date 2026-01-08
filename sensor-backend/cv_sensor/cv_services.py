"""
Business logic services for CV analysis operations.
"""

import uuid
from datetime import datetime
from typing import Dict, Optional
from fastapi import HTTPException, UploadFile

from .extractors import (
    extract_text_from_pdf,
    get_pdf_page_count,
    parse_cv_sections,
    extract_basic_info,
    extract_work_experience,
    extract_skill_keywords,
    extract_education
)
from .validators import validate_pdf_file, validate_file_size, validate_cv_id


class CVService:
    """Service class for CV analysis operations."""
    
    def __init__(self, cv_store: dict):
        """
        Initialize the CV service.
        
        Args:
            cv_store: Dictionary for storing CV data in memory
        """
        self.cv_store = cv_store
    
    async def upload_and_analyze_cv(self, file: UploadFile) -> dict:
        """
        Upload and analyze CV in one operation.
        
        Args:
            file: Uploaded PDF file
            
        Returns:
            dict: Complete CV analysis with cv_id and extracted data
            
        Raises:
            HTTPException: If validation or processing fails
        """
        # Validate file
        validate_pdf_file(file)
        
        # Read file content
        file_content = await file.read()
        
        # Validate file size
        validate_file_size(len(file_content))
        
        # Extract text and get page count
        try:
            raw_text = extract_text_from_pdf(file_content)
            pages = get_pdf_page_count(file_content)
        except Exception as e:
            raise HTTPException(
                status_code=422,
                detail=f"Failed to process PDF: {str(e)}"
            )
        
        if not raw_text or len(raw_text.strip()) == 0:
            raise HTTPException(
                status_code=422,
                detail="No text found in PDF. The PDF may be image-based or corrupted."
            )
        
        # Generate CV ID
        cv_id = str(uuid.uuid4())
        
        # Parse CV into sections once
        sections = parse_cv_sections(raw_text)
        
        # Extract all information using pre-parsed sections
        try:
            basic_info = extract_basic_info(raw_text, sections)
            work_experience = extract_work_experience(sections)
            skill_keywords = extract_skill_keywords(sections)
            education = extract_education(sections)
            
            # Create analysis result
            analysis = {
                "cv_id": cv_id,
                "basic_info": basic_info,
                "work_experience": work_experience,
                "skill_keywords": skill_keywords,
                "education": education
            }
            
            # Store CV data with analysis
            self.cv_store[cv_id] = {
                "id": cv_id,
                "filename": file.filename,
                "upload_date": datetime.utcnow().isoformat() + "Z",
                "pages": pages,
                "raw_text": raw_text,
                "file_size": len(file_content),
                "analysis": analysis
            }
            
            return analysis
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error analyzing CV: {str(e)}"
            )
    
    async def upload_cv(self, file: UploadFile) -> dict:
        """
        Upload and store CV PDF.
        
        Args:
            file: Uploaded PDF file
            
        Returns:
            dict: Upload response with cv_id, message, and page count
            
        Raises:
            HTTPException: If validation or processing fails
        """
        # Validate file
        validate_pdf_file(file)
        
        # Read file content
        file_content = await file.read()
        
        # Validate file size
        validate_file_size(len(file_content))
        
        # Extract text and get page count
        try:
            raw_text = extract_text_from_pdf(file_content)
            pages = get_pdf_page_count(file_content)
        except Exception as e:
            raise HTTPException(
                status_code=422,
                detail=f"Failed to process PDF: {str(e)}"
            )
        
        if not raw_text or len(raw_text.strip()) == 0:
            raise HTTPException(
                status_code=422,
                detail="No text found in PDF. The PDF may be image-based or corrupted."
            )
        
        # Generate CV ID
        cv_id = str(uuid.uuid4())
        
        # Store CV data
        self.cv_store[cv_id] = {
            "id": cv_id,
            "filename": file.filename,
            "upload_date": datetime.utcnow().isoformat() + "Z",
            "pages": pages,
            "raw_text": raw_text,
            "file_size": len(file_content),
            "analysis": None  # Will be populated when analyze is called
        }
        
        return {
            "cv_id": cv_id,
            "message": "CV uploaded successfully",
            "pages": pages
        }
    
    def analyze_cv(self, cv_id: str) -> dict:
        """
        Analyze CV and extract structured data.
        
        Args:
            cv_id: CV identifier
            
        Returns:
            dict: Complete CV analysis with basic_info, work_experience, skill_keywords, education
            
        Raises:
            HTTPException: If CV not found or analysis fails
        """
        # Validate CV ID
        validated_cv_id = validate_cv_id(cv_id)
        
        # Check if CV exists
        if validated_cv_id not in self.cv_store:
            raise HTTPException(
                status_code=404,
                detail=f"CV with ID '{validated_cv_id}' not found"
            )
        
        cv_data = self.cv_store[validated_cv_id]
        raw_text = cv_data["raw_text"]
        
        # Parse CV into sections once
        sections = parse_cv_sections(raw_text)
        
        # Extract all information using pre-parsed sections
        try:
            basic_info = extract_basic_info(raw_text, sections)
            work_experience = extract_work_experience(sections)
            skill_keywords = extract_skill_keywords(sections)
            education = extract_education(sections)
            
            # Create analysis result
            analysis = {
                "cv_id": validated_cv_id,
                "basic_info": basic_info,
                "work_experience": work_experience,
                "skill_keywords": skill_keywords,
                "education": education
            }
            
            # Store analysis in CV data
            cv_data["analysis"] = analysis
            
            return analysis
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error analyzing CV: {str(e)}"
            )
    
    def get_cv(self, cv_id: str) -> dict:
        """
        Get CV details including analysis if available.
        
        Args:
            cv_id: CV identifier
            
        Returns:
            dict: Complete CV data
            
        Raises:
            HTTPException: If CV not found
        """
        validated_cv_id = validate_cv_id(cv_id)
        
        if validated_cv_id not in self.cv_store:
            raise HTTPException(
                status_code=404,
                detail=f"CV with ID '{validated_cv_id}' not found"
            )
        
        return self.cv_store[validated_cv_id]
    
    def get_all_cvs(self) -> dict:
        """
        Get list of all uploaded CVs.
        
        Returns:
            dict: List of CVs with metadata and count
        """
        cvs = []
        
        for cv_id, cv_data in self.cv_store.items():
            cvs.append({
                "cv_id": cv_id,
                "filename": cv_data["filename"],
                "upload_date": cv_data["upload_date"],
                "analyzed": cv_data["analysis"] is not None
            })
        
        # Sort by upload date (most recent first)
        cvs.sort(key=lambda x: x["upload_date"], reverse=True)
        
        return {
            "cvs": cvs,
            "count": len(cvs)
        }
    
    def delete_cv(self, cv_id: str) -> dict:
        """
        Delete CV and its analysis.
        
        Args:
            cv_id: CV identifier
            
        Returns:
            dict: Deletion confirmation message
            
        Raises:
            HTTPException: If CV not found
        """
        validated_cv_id = validate_cv_id(cv_id)
        
        if validated_cv_id not in self.cv_store:
            raise HTTPException(
                status_code=404,
                detail=f"CV with ID '{validated_cv_id}' not found"
            )
        
        filename = self.cv_store[validated_cv_id]["filename"]
        del self.cv_store[validated_cv_id]
        
        return {
            "message": f"CV '{filename}' (ID: {validated_cv_id}) deleted successfully"
        }
    
    def get_cv_skills(self, cv_id: str) -> dict:
        """
        Get only skill keywords for a specific CV.
        
        Args:
            cv_id: CV identifier
            
        Returns:
            dict: Skill keywords list
            
        Raises:
            HTTPException: If CV not found or not analyzed
        """
        validated_cv_id = validate_cv_id(cv_id)
        
        if validated_cv_id not in self.cv_store:
            raise HTTPException(
                status_code=404,
                detail=f"CV with ID '{validated_cv_id}' not found"
            )
        
        cv_data = self.cv_store[validated_cv_id]
        
        if not cv_data["analysis"]:
            raise HTTPException(
                status_code=404,
                detail=f"CV '{validated_cv_id}' has not been analyzed yet. Call /analyze-cv first."
            )
        
        return {
            "cv_id": validated_cv_id,
            "skill_keywords": cv_data["analysis"]["skill_keywords"]
        }
