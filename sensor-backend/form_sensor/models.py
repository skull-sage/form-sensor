from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class PredefinedDescription(Base):
    __tablename__ = "predefined_descriptions"
    
    id = Column(String, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    category = Column(String, default="general")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SimilarityCheck(Base):
    __tablename__ = "similarity_checks"
    
    id = Column(Integer, primary_key=True, index=True)
    input_text = Column(Text, nullable=False)
    best_match_id = Column(String)
    best_similarity_score = Column(Float)
    threshold_used = Column(Float)
    matches_count = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)