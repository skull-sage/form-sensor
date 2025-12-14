from pydantic import BaseModel
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