import pytesseract
from PIL import Image
import numpy as np

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

def extract_text_blocks(image_path, config='--psm 11'):
    """Extract text blocks from an image using Tesseract OCR"""
    try:
        image = Image.open(image_path)
        data = pytesseract.image_to_data(
            np.array(image), 
            output_type=pytesseract.Output.DICT,
            config=config
        )
        
        blocks = []
        for i in range(len(data['text'])):
            if int(data['conf'][i]) > 60:  # Confidence threshold
                block = {
                    'text': data['text'][i],
                    'bbox': (
                        data['left'][i],
                        data['top'][i],
                        data['width'][i],
                        data['height'][i]
                    ),
                    'page_num': 0  # For multi-page docs
                }
                blocks.append(block)
        return blocks
    except Exception as e:
        print(f"OCR Error: {str(e)}")
        return []