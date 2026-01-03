"""
OCR engine wrapper for EasyOCR.
"""

import numpy as np
from typing import List, Dict, Optional


def initialize_ocr(use_gpu: bool = False, lang: str = 'en'):
    """
    Initialize EasyOCR engine.
    
    Args:
        use_gpu: Enable GPU acceleration
        lang: Language code ('en', 'ch_sim', 'fr', 'de', 'ko', 'ja')
        
    Returns:
        easyocr.Reader: Initialized OCR engine
    """
    try:
        import easyocr
        
        # Map language codes to EasyOCR format
        lang_map = {
            'en': 'en',
            'ch': 'ch_sim',
            'fr': 'fr',
            'german': 'de',
            'korean': 'ko',
            'japan': 'ja'
        }
        
        ocr_lang = lang_map.get(lang, 'en')
        
        # Initialize EasyOCR Reader
        reader = easyocr.Reader([ocr_lang], gpu=use_gpu)
        
        return reader
        
    except Exception as e:
        raise Exception(f"Failed to initialize OCR engine: {str(e)}")


def extract_text(image: np.ndarray, ocr, confidence_threshold: float = 0.5) -> List[Dict]:
    """
    Extract text from image using OCR.
    
    Args:
        image: Input image as numpy array
        ocr: Initialized EasyOCR Reader
        confidence_threshold: Minimum confidence score (0-1)
        
    Returns:
        list: List of text regions with text, confidence, and bounding box
    """
    try:
        # Validate image
        if image is None or image.size == 0:
            print("Warning: Empty or invalid image provided to OCR")
            return []
        
        # Ensure image is in correct format (H, W, C) with 3 channels
        if len(image.shape) == 2:
            # Grayscale - convert to RGB
            image = np.stack([image] * 3, axis=-1)
        elif len(image.shape) == 3 and image.shape[2] == 4:
            # RGBA - convert to RGB
            image = image[:, :, :3]
        elif len(image.shape) != 3 or image.shape[2] != 3:
            print(f"Warning: Unexpected image shape: {image.shape}")
            return []
        
        # Run OCR with EasyOCR
        # Returns list of (bbox, text, confidence)
        results = ocr.readtext(image)
        
        if not results:
            return []
        
        # Extract text regions
        text_regions = []
        
        for result in results:
            try:
                bbox = result[0]  # [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
                text = result[1]   # text string
                confidence = result[2]  # confidence score
                
                # Skip empty text
                if not text or text.strip() == '':
                    continue
                
                # Filter by confidence
                if confidence >= confidence_threshold:
                    text_regions.append({
                        'text': text,
                        'confidence': float(confidence),
                        'bounding_box': [[float(x), float(y)] for x, y in bbox]
                    })
            except Exception as line_error:
                # Silently skip problematic lines
                continue
        
        return text_regions
        
    except Exception as e:
        print(f"OCR extraction error: {str(e)}")
        return []


def filter_by_confidence(results: List[Dict], threshold: float) -> List[Dict]:
    """
    Filter OCR results by confidence threshold.
    
    Args:
        results: List of text regions
        threshold: Minimum confidence score (0-1)
        
    Returns:
        list: Filtered text regions
    """
    return [r for r in results if r['confidence'] >= threshold]
