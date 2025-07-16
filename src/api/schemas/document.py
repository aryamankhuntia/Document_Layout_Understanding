from pydantic import BaseModel
from typing import Dict, List, Optional

class Entity(BaseModel):
    type: str
    text: str
    bbox: List[int]
    confidence: float

class DocumentParseResponse(BaseModel):
    success: bool
    error: Optional[str]=None
    entities: Dict[str,List[Entity]]

class HealthCheckResponse(BaseModel):
    status: str
    model_loaded: bool
    device: str