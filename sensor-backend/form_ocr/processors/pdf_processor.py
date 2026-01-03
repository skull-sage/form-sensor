"""
PDF image extraction utilities.
"""

import numpy as np
from io import BytesIO
from typing import List
from PIL import Image
import fitz  # PyMuPDF


def pdf_to_images(pdf_bytes: bytes) -> List[np.ndarray]:
    """
    Extract embedded images from PDF using PyMuPDF.
    
    Args:
        pdf_bytes: PDF file content as bytes
        
    Returns:
        list: List of numpy arrays (one per extracted image)
        
    Raises:
        Exception: If PDF image extraction fails
    """
    try:
        # Open PDF with PyMuPDF
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        np_images = []
        
        # Iterate through all pages
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            
            # Get list of images on the page
            image_list = page.get_images(full=True)
            
            for img_index, img_info in enumerate(image_list):
                xref = img_info[0]  # Image reference number
                
                try:
                    # Extract image
                    base_image = pdf_document.extract_image(xref)
                    image_bytes = base_image["image"]
                    
                    # Open image with PIL
                    pil_img = Image.open(BytesIO(image_bytes))
                    
                    # Convert to RGB if needed
                    if pil_img.mode != 'RGB':
                        pil_img = pil_img.convert('RGB')
                    
                    # Convert to numpy array
                    np_img = np.array(pil_img)
                    np_images.append(np_img)
                    
                except Exception as img_error:
                    print(f"Warning: Failed to extract image {img_index + 1} from page {page_num + 1}: {str(img_error)}")
                    continue
        
        pdf_document.close()
        
        if not np_images:
            raise Exception("No images found in PDF or all image extractions failed")
        
        return np_images
        
    except Exception as e:
        raise Exception(f"Failed to extract images from PDF: {str(e)}")


def get_page_count(pdf_bytes: bytes) -> int:
    """
    Get number of embedded images in PDF.
    
    Args:
        pdf_bytes: PDF file content as bytes
        
    Returns:
        int: Number of embedded images
    """
    try:
        import fitz
        
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        image_count = 0
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            image_list = page.get_images(full=True)
            image_count += len(image_list)
        
        pdf_document.close()
        return image_count
    except:
        return 0


def numpy_to_base64(image: np.ndarray) -> str:
    """
    Convert numpy array to base64 string.
    
    Args:
        image: Numpy array image
        
    Returns:
        str: Base64 encoded image
    """
    import base64
    
    # Convert numpy array to PIL Image
    pil_img = Image.fromarray(image.astype('uint8'))
    
    # Save to bytes buffer
    buffer = BytesIO()
    pil_img.save(buffer, format='PNG')
    buffer.seek(0)
    
    # Encode to base64
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    
    return f"data:image/png;base64,{img_base64}"
