from fastapi import FastAPI
from src.api.routes.document import router as document_router

app = FastAPI(
    title="Document Layout Understanding API",
    description="API for interpreting structured documents like invoices and forms",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(document_router, prefix="/document", tags=["Document"])

@app.get("/")
def root():
    return {
        "message": "Document Layout Understanding API",
        "endpoints": {
            "document_parse": "/document/parse",
            "health_check": "/document/health",
            "docs": "/docs"
        }
    }