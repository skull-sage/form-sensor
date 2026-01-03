"""
Form segment detection and field extraction utilities.
"""

from typing import List, Dict, Tuple, Optional


def detect_segments(text_regions: List[Dict]) -> Dict:
    """
    Detect form segments (labels and input fields).
    
    Args:
        text_regions: List of text regions from OCR
        
    Returns:
        dict: Detected segments with labels and inputs
    """
    if not text_regions:
        return {'labels': [], 'inputs': [], 'fields': []}
    
    # Sort regions by position (top to bottom, left to right)
    sorted_regions = sorted(
        text_regions,
        key=lambda r: (r['bounding_box'][0][1], r['bounding_box'][0][0])
    )
    
    # Classify regions as labels or inputs
    labels = []
    inputs = []
    
    for region in sorted_regions:
        if is_label(region):
            labels.append(region)
        else:
            inputs.append(region)
    
    return {
        'labels': labels,
        'inputs': inputs,
        'sorted_regions': sorted_regions
    }


def is_label(region: Dict) -> bool:
    """
    Heuristic to determine if a text region is a label.
    
    Args:
        region: Text region
        
    Returns:
        bool: True if likely a label
    """
    text = region['text'].strip()
    
    # Labels typically:
    # - End with colon (:)
    # - Are longer (more than 2 characters)
    # - Contain alphabetic characters
    # - May contain common label words
    
    if text.endswith(':'):
        return True
    
    if len(text) > 2 and any(c.isalpha() for c in text):
        # Check for common label patterns
        label_keywords = ['name', 'date', 'address', 'phone', 'email', 'number', 'id', 'code']
        text_lower = text.lower()
        if any(keyword in text_lower for keyword in label_keywords):
            return True
    
    # Default: longer text is more likely a label
    return len(text) > 5


def detect_horizontal_layout(text_regions: List[Dict]) -> List[Tuple[Dict, Dict]]:
    """
    Detect horizontal layout (label left, input right).
    
    Args:
        text_regions: List of text regions
        
    Returns:
        list: List of (label, input) pairs
    """
    segments = detect_segments(text_regions)
    labels = segments['labels']
    inputs = segments['inputs']
    
    pairs = []
    
    for label in labels:
        # Find input to the right of this label
        best_match = None
        min_distance = float('inf')
        
        label_bbox = label['bounding_box']
        label_y = label_bbox[0][1]  # Top y coordinate
        label_right_x = label_bbox[1][0]  # Right x coordinate
        
        for input_region in inputs:
            input_bbox = input_region['bounding_box']
            input_y = input_bbox[0][1]
            input_left_x = input_bbox[0][0]
            
            # Check if vertically aligned
            if is_horizontally_aligned(label, input_region):
                # Calculate distance
                distance = input_left_x - label_right_x
                
                if distance > 0 and distance < min_distance:
                    min_distance = distance
                    best_match = input_region
        
        if best_match:
            pairs.append((label, best_match))
    
    return pairs


def detect_vertical_layout(text_regions: List[Dict]) -> List[Tuple[Dict, Dict]]:
    """
    Detect vertical layout (label top, input below).
    
    Args:
        text_regions: List of text regions
        
    Returns:
        list: List of (label, input) pairs
    """
    segments = detect_segments(text_regions)
    labels = segments['labels']
    inputs = segments['inputs']
    
    pairs = []
    
    for label in labels:
        # Find input below this label
        best_match = None
        min_distance = float('inf')
        
        label_bbox = label['bounding_box']
        label_x = label_bbox[0][0]  # Left x coordinate
        label_bottom_y = label_bbox[2][1]  # Bottom y coordinate
        
        for input_region in inputs:
            input_bbox = input_region['bounding_box']
            input_x = input_bbox[0][0]
            input_top_y = input_bbox[0][1]
            
            # Check if horizontally aligned
            if is_vertically_aligned(label, input_region):
                # Calculate distance
                distance = input_top_y - label_bottom_y
                
                if distance > 0 and distance < min_distance:
                    min_distance = distance
                    best_match = input_region
        
        if best_match:
            pairs.append((label, best_match))
    
    return pairs


def is_horizontally_aligned(label: Dict, input_region: Dict, threshold: int = 30) -> bool:
    """
    Check if input is to the right of label and vertically aligned.
    
    Args:
        label: Label region
        input_region: Input region
        threshold: Vertical alignment threshold in pixels
        
    Returns:
        bool: True if horizontally aligned
    """
    label_bbox = label['bounding_box']
    input_bbox = input_region['bounding_box']
    
    label_y = label_bbox[0][1]
    input_y = input_bbox[0][1]
    label_right_x = label_bbox[1][0]
    input_left_x = input_bbox[0][0]
    
    # Check vertical alignment
    vertical_aligned = abs(label_y - input_y) < threshold
    
    # Check if input is to the right
    horizontal_gap = input_left_x - label_right_x
    is_right = horizontal_gap > 0 and horizontal_gap < 200  # Max 200 pixels gap
    
    return vertical_aligned and is_right


def is_vertically_aligned(label: Dict, input_region: Dict, threshold: int = 30) -> bool:
    """
    Check if input is below label and horizontally aligned.
    
    Args:
        label: Label region
        input_region: Input region
        threshold: Horizontal alignment threshold in pixels
        
    Returns:
        bool: True if vertically aligned
    """
    label_bbox = label['bounding_box']
    input_bbox = input_region['bounding_box']
    
    label_x = label_bbox[0][0]
    input_x = input_bbox[0][0]
    label_bottom_y = label_bbox[2][1]
    input_top_y = input_bbox[0][1]
    
    # Check horizontal alignment
    horizontal_aligned = abs(label_x - input_x) < threshold
    
    # Check if input is below
    vertical_gap = input_top_y - label_bottom_y
    is_below = vertical_gap > 0 and vertical_gap < 100  # Max 100 pixels gap
    
    return horizontal_aligned and is_below


def detect_digit_boxes(text_regions: List[Dict]) -> List[List[Dict]]:
    """
    Detect digit boxes (small rectangular regions in sequence).
    
    Args:
        text_regions: List of text regions
        
    Returns:
        list: List of digit box groups
    """
    # Filter for single digit/character regions
    digit_regions = []
    
    for region in text_regions:
        text = region['text'].strip()
        bbox = region['bounding_box']
        
        # Calculate width and height
        width = bbox[1][0] - bbox[0][0]
        height = bbox[2][1] - bbox[0][1]
        
        # Digit boxes are typically small and square-ish
        if len(text) <= 2 and width < 50 and height < 50:
            digit_regions.append(region)
    
    # Group digit boxes that are close together
    groups = []
    used = set()
    
    for i, region in enumerate(digit_regions):
        if i in used:
            continue
        
        group = [region]
        used.add(i)
        
        # Find nearby digit boxes
        for j, other in enumerate(digit_regions):
            if j in used:
                continue
            
            if are_adjacent(region, other):
                group.append(other)
                used.add(j)
        
        if len(group) > 1:
            groups.append(group)
    
    return groups


def are_adjacent(region1: Dict, region2: Dict, threshold: int = 20) -> bool:
    """
    Check if two regions are adjacent.
    
    Args:
        region1: First region
        region2: Second region
        threshold: Distance threshold in pixels
        
    Returns:
        bool: True if adjacent
    """
    bbox1 = region1['bounding_box']
    bbox2 = region2['bounding_box']
    
    # Check if vertically aligned
    y_diff = abs(bbox1[0][1] - bbox2[0][1])
    
    # Check horizontal distance
    x_dist = abs(bbox1[1][0] - bbox2[0][0])
    
    return y_diff < threshold and x_dist < threshold * 2


def extract_form_fields(segments: Dict) -> List[Dict]:
    """
    Extract form fields as key-value pairs.
    
    Args:
        segments: Detected segments from detect_segments()
        
    Returns:
        list: List of form fields with label, value, layout, confidence
    """
    fields = []
    
    # Get text regions from segments
    text_regions = segments.get('sorted_regions', [])
    
    if not text_regions:
        return fields
    
    # Detect horizontal layout fields
    horizontal_pairs = detect_horizontal_layout(text_regions)
    for label, input_region in horizontal_pairs:
        fields.append({
            'label': label['text'].rstrip(':').strip(),
            'value': input_region['text'].strip() if input_region['text'].strip() else None,
            'layout': 'horizontal',
            'confidence': (label['confidence'] + input_region['confidence']) / 2
        })
    
    # Detect vertical layout fields
    vertical_pairs = detect_vertical_layout(text_regions)
    for label, input_region in vertical_pairs:
        # Avoid duplicates
        label_text = label['text'].rstrip(':').strip()
        if not any(f['label'] == label_text for f in fields):
            fields.append({
                'label': label_text,
                'value': input_region['text'].strip() if input_region['text'].strip() else None,
                'layout': 'vertical',
                'confidence': (label['confidence'] + input_region['confidence']) / 2
            })
    
    # Detect digit boxes and group them
    digit_groups = detect_digit_boxes(text_regions)
    for group in digit_groups:
        # Concatenate digits
        value = ''.join([r['text'].strip() for r in group])
        avg_confidence = sum([r['confidence'] for r in group]) / len(group)
        
        # Try to find a label for this digit group
        # (This is a simplified approach - could be improved)
        fields.append({
            'label': 'Digit Field',
            'value': value,
            'layout': 'digit_boxes',
            'confidence': avg_confidence
        })
    
    return fields
