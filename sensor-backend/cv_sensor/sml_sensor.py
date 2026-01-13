"""
Semantic Similarity Module using Sentence Transformers.

This module provides functionality to check semantic similarity between text pairs
using HuggingFace's Sentence Transformers with cosine similarity.
"""

from sentence_transformers import SentenceTransformer, util
from typing import List, Tuple
import torch


class SimilarityChecker:
    """
    A class to check semantic similarity between text pairs using Sentence Transformers.
    Uses bi-encoder to create embeddings and cosine similarity for scoring.
    Returns normalized scores between 0 and 1.
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the similarity checker with a Sentence Transformer model.
        
        Args:
            model_name: Name of the Sentence Transformer model from HuggingFace
                       Default: all-MiniLM-L6-v2 (fast, accurate, general-purpose)
                       Alternatives:
                       - "all-mpnet-base-v2" (more accurate, slower)
                       - "paraphrase-multilingual-MiniLM-L12-v2" (multilingual)
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
            text1: First text string (e.g., expected answer)
            text2: Second text string (e.g., candidate's answer)
            
        Returns:
            float: Similarity score between 0 and 1 (1 = identical, 0 = completely different)
        """
        # Encode both texts to embeddings
        embeddings = self.model.encode([text1, text2], convert_to_tensor=True)
        
        # Calculate cosine similarity
        similarity = util.cos_sim(embeddings[0], embeddings[1])
        
        # Convert to float and return (value between 0 and 1)
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
