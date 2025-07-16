from fastapi import APIRouter, UploadFile, File, HTTPException
from src.api.services.document_parser import DocumentParser
from src.api.schemas.document import DocumentParseResponse, HealthCheckResponse
from PIL import Image
import io

router = APIRouter()

MODEL_PATH = "models/trained/layoutlmv3-funsd-final"
document_parser=DocumentParser(MODEL_PATH)

@router.post("/parse", response_model=DocumentParseResponse)
async def parse_document(file: UploadFile = File(...)):
    try:
        content = await file.read()
        image = Image.open(io.BytesIO(content)).convert("RGB")

        entities = document_parser.parse_document(image)

        return{
            "success":True,
            "entities":entities
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Document Processing Failed: {str(e)}"
        )
    
@router.get("/health",response_model=HealthCheckResponse)
def health_check():
    return{
        "status":"OK",
        "model_loaded":True,
        "device":str(document_parser.device)
    }