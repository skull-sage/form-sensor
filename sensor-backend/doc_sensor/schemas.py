"""
Pydantic schemas for CV analysis API requests and responses.
"""

from pydantic import BaseModel, field_validator
from typing import List, Optional, Dict
from datetime import datetime


class BasicInfo(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    social_links: Dict[str, str] = {}


class WorkExperience(BaseModel):
    company: str
    start_date: Optional[str] = None  # ISO 8601 or "Present"
    end_date: Optional[str] = None
    description: str


class Education(BaseModel):
    degree: str
    institution: str
    graduation_date: Optional[str] = None


class CVAnalysisResponse(BaseModel):
    cv_id: str
    basic_info: BasicInfo
    work_experience: List[WorkExperience]
    skill_keywords: List[str]
    education: List[Education]


class CVDetailResponse(BaseModel):
    cv_id: str
    filename: str
    upload_date: str
    pages: int
    raw_text: str
    analysis: Optional[CVAnalysisResponse] = None


class CVListItem(BaseModel):
    cv_id: str
    filename: str
    upload_date: str
    analyzed: bool


class CVListResponse(BaseModel):
    cvs: List[CVListItem]
    count: int


class DeleteCVResponse(BaseModel):
    message: str
