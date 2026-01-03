"""
Perspective correction utilities using OpenCV.
"""

import cv2
import numpy as np
from typing import Tuple, Optional


def detect_corners(image: np.ndarray) -> Optional[np.ndarray]:
    """
    Detect four corners of a form in an image.
    
    Args:
        image: Input image as numpy array
        
    Returns:
        np.ndarray: Four corner points [[x1,y1], [x2,y2], [x3,y3], [x4,y4]] or None if detection fails
    """
    try:
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Edge detection using Canny
        edges = cv2.Canny(blurred, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Sort contours by area (largest first)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        
        # Find the largest rectangular contour
        for contour in contours[:10]:  # Check top 10 largest contours
            # Calculate perimeter
            perimeter = cv2.arcLength(contour, True)
            
            # Approximate the contour to a polygon
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            
            # If the approximated contour has 4 points, we found a rectangle
            if len(approx) == 4:
                # Reshape to get corner points
                corners = approx.reshape(4, 2)
                return order_points(corners)
        
        return None
        
    except Exception as e:
        print(f"Corner detection error: {str(e)}")
        return None


def order_points(pts: np.ndarray) -> np.ndarray:
    """
    Order points in consistent order: top-left, top-right, bottom-right, bottom-left.
    
    Args:
        pts: Four corner points
        
    Returns:
        np.ndarray: Ordered points
    """
    # Initialize ordered points
    rect = np.zeros((4, 2), dtype="float32")
    
    # Sum and difference to find corners
    s = pts.sum(axis=1)
    diff = np.diff(pts, axis=1)
    
    # Top-left will have smallest sum
    rect[0] = pts[np.argmin(s)]
    
    # Bottom-right will have largest sum
    rect[2] = pts[np.argmax(s)]
    
    # Top-right will have smallest difference
    rect[1] = pts[np.argmin(diff)]
    
    # Bottom-left will have largest difference
    rect[3] = pts[np.argmax(diff)]
    
    return rect


def apply_perspective_warp(image: np.ndarray, corners: np.ndarray) -> np.ndarray:
    """
    Apply perspective warp transformation to flatten the image.
    
    Args:
        image: Input image
        corners: Four corner points in order [top-left, top-right, bottom-right, bottom-left]
        
    Returns:
        np.ndarray: Warped (flattened) image
    """
    # Order the corners
    rect = order_points(corners)
    (tl, tr, br, bl) = rect
    
    # Calculate the width of the new image
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    
    # Calculate the height of the new image
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    
    # Destination points for the warped image
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]
    ], dtype="float32")
    
    # Calculate perspective transform matrix
    M = cv2.getPerspectiveTransform(rect, dst)
    
    # Apply perspective warp
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    
    return warped


def correct_image(image: np.ndarray) -> Tuple[np.ndarray, bool]:
    """
    Complete perspective correction pipeline.
    
    Args:
        image: Input image
        
    Returns:
        tuple: (corrected_image, correction_applied)
            - corrected_image: Corrected image (or original if correction failed)
            - correction_applied: Boolean indicating if correction was successful
    """
    # Detect corners
    corners = detect_corners(image)
    
    if corners is None:
        # Corner detection failed, return original image
        return image, False
    
    try:
        # Apply perspective warp
        corrected = apply_perspective_warp(image, corners)
        return corrected, True
        
    except Exception as e:
        print(f"Perspective warp error: {str(e)}")
        return image, False
