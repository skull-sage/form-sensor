"""
Semantic Similarity Module using BiEncoder.

This module provides functionality to check semantic similarity between text pairs
using HuggingFace's BiEncoder model with cosine similarity.
"""

from sentence_transformers import SentenceTransformer, util
from typing import List, Tuple
import torch


class SimilarityChecker:
    """
    A class to check semantic similarity between text pairs using BiEncoder.
    Uses cosine similarity on independently computed embeddings for efficiency.
    """
    
    def __init__(self, model_name: str = "msmarco-MiniLM-L6-cos-v5"):
        """
        Initialize the similarity checker with a BiEncoder model.
        
        Args:
            model_name: Name of the BiEncoder model from HuggingFace
                       Default: msmarco-MiniLM-L6-cos-v5 (optimized for semantic search)
        """
        self.model = SentenceTransformer(model_name)
    
    def check_similarity(
        self, 
        text1: str, 
        text2: str
    ) -> float:
        """
        Check semantic similarity between two text strings using cosine similarity.
        
        Args:
            text1: First text string
            text2: Second text string
            
        Returns:
            float: Cosine similarity score between -1 and 1 (higher means more similar)
        """
        # Encode both texts
        embeddings = self.model.encode([text1, text2], convert_to_tensor=True)
        
        # Calculate cosine similarity
        similarity = util.cos_sim(embeddings[0], embeddings[1])
        
        return float(similarity.item())
 
# Global instance for reuse
_similarity_checker = None


def get_similarity_checker() -> SimilarityChecker:
    """
    Get or create a global SimilarityChecker instance.
    
    Returns:
        SimilarityChecker: Global similarity checker instance
    """
    global _similarity_checker
    if _similarity_checker is None:
        _similarity_checker = SimilarityChecker()
    return _similarity_checker


def check_similarity(text1: str, text2: str) -> float:
    """
    Convenience function to check similarity between two texts.
    
    Args:
        text1: First text string
        text2: Second text string
        
    Returns:
        float: Similarity score (higher means more similar)
    """
    checker = get_similarity_checker()
    return checker.check_similarity(text1, text2)
