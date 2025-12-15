from pydantic import BaseModel, field_validator
from typing import Dict, List, Optional
from typing import List, Optional, Dict
from datetime import datetime

class Description(BaseModel):
    id: str
    text: str
    category: str = "general"

class DescriptionCreate(BaseModel):
    text: str
    category: str = "general"

class DescriptionResponse(Description):
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class SimilarityRequest(BaseModel):
    text: str
    threshold: float = 0.7

class MatchResult(BaseModel):
    id: str
    text: str
    category: str
    similarity: float

class SimilarityResponse(BaseModel):
    input_text: str
    matches: List[MatchResult]
    best_match: Optional[MatchResult] = None
    similarity_scores: List[float]
    threshold_used: float
    total_comparisons: int

class SimilarityCheckHistory(BaseModel):
    id: int
    input_text: str
    best_match_id: Optional[str]
    best_similarity_score: Optional[float]
    threshold_used: float
    matches_count: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

class CreateSensorRequest(BaseModel):
    text: str
    
    @field_validator('text')
    @classmethod
    def validate_text(cls, v):
        if not v or not v.strip():
            raise ValueError('Text cannot be empty or contain only whitespace')
        if len(v.strip()) > 10000:
            raise ValueError('Text is too long (maximum 10,000 characters)')
        return v.strip()


class SimilarityRequest(BaseModel):
    text: str
    
    @field_validator('text')
    @classmethod
    def validate_text(cls, v):
        if not v or not v.strip():
            raise ValueError('Text cannot be empty or contain only whitespace')
        if len(v.strip()) > 5000:
            raise ValueError('Text is too long (maximum 5,000 characters)')
        return v.strip()


class SimilarityResponse(BaseModel):
    confidence_score: float
    matched_paragraph: str


class BulkCreateRequest(BaseModel):
    sensors: Dict[str, str]  # nameId -> text mapping


class BulkCreateResponse(BaseModel):
    created: List[str]  # list of successfully created sensor nameIds
    skipped: List[str]  # list of nameIds that already existed
    failed: List[str]   # list of nameIds that failed to create


class SensorListResponse(BaseModel):
    sensors: Dict[str, str]  # nameId -> text mapping
    count: int


class CreateSensorResponse(BaseModel):
    message: str
    paragraphs_count: int


class DeleteSensorResponse(BaseModel):
    message: str


class HealthResponse(BaseModel):
    model_config = {"protected_namespaces": ()}
    
    status: str
    service: str
    model: str
    model_status: str
    model_error: Optional[str] = None