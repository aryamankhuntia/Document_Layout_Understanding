import io
import logging
from fastapi import UploadFile, HTTPException
from PIL import Image
from pdf2image import convert_from_bytes
from .document_parser import DocumentParser  # Local import
import os

logger = logging.getLogger(__name__)

# Initialize parser only once
parser = None

async def parse_document(file: UploadFile):
    global parser
    
    try:
        # Initialize parser if not already initialized
        if parser is None:
            logger.info("Initializing DocumentParser")
            model_path = os.getenv("MODEL_PATH", "models/trained/layoutlmv3-funsd-final")
            parser = DocumentParser(model_path)
        
        # Read file content
        contents = await file.read()
        
        # Handle PDF files
        if file.content_type == "application/pdf":
            logger.info("Processing PDF file")
            images = convert_from_bytes(contents)
            if not images:
                raise HTTPException(status_code=400, detail="PDF conversion failed")
            # Process first page only
            image = images[0]
        # Handle image files
        else:
            logger.info(f"Processing image file: {file.content_type}")
            image = Image.open(io.BytesIO(contents))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Process document
        result = parser.parse_document(image)
        logger.info(f"Document processed. Found {sum(len(v) for v in result['entities'].values())} entities")
        return result
        
    except Exception as e:
        logger.error(f"Document processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Document processing failed: {str(e)}")
    finally:
        await file.close()