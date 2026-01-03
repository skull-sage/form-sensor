from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sentence_transformers import SentenceTransformer
import uvicorn
import json

from form_sensor.schemas import HealthResponse
from form_sensor.services import SensorService
from form_sensor import router as form_sensor_router
from doc_sensor.services import CVService
from doc_sensor import router as doc_sensor_router
from form_ocr.services import FormOCRService
import form_ocr as form_ocr_module

app = FastAPI(
    title="Semantic Description Sensor API",
    description="API for semantic similarity detection using sentence transformers",
    version="1.0.0"
)

# Configure CORS - Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors with descriptive messages"""
    error_details = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        error_details.append(f"{field}: {message}")
    
    return JSONResponse(
        status_code=400,
        content={
            "error": "Validation Error",
            "message": "Invalid input data",
            "details": error_details
        }
    )

@app.exception_handler(json.JSONDecodeError)
async def json_decode_exception_handler(request: Request, exc: json.JSONDecodeError):
    """Handle malformed JSON requests"""
    return JSONResponse(
        status_code=400,
        content={
            "error": "Invalid JSON",
            "message": "Request body contains malformed JSON",
            "details": [str(exc)]
        }
    )

# Load the sentence transformer model
model = None
model_error = None

def load_model():
    """Load the sentence transformer model with proper error handling"""
    global model, model_error
    try:
        print("Loading sentence transformer model...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        model_error = None
        print("Model loaded successfully")
        return True
    except Exception as e:
        error_msg = f"Failed to load sentence transformer model: {str(e)}"
        print(error_msg)
        model_error = error_msg
        model = None
        return False

# In-memory storage for text sensors
text_store = {}  # nameId -> original full text
sensor_data_list = {}  # nameId -> [(paragraph, embedding), (paragraph, embedding), ...]

# In-memory storage for CV analysis
cv_store = {}  # cv_id -> {id, filename, upload_date, pages, raw_text, file_size, analysis}

# In-memory storage for Form OCR
form_store = {}  # form_id -> {id, filename, upload_date, page_count, file_size, processing_status, pages, metadata}

# Initialize services (will be set after model loads)
sensor_service = None
cv_service = None
form_ocr_service = None

# Try to load model on startup
load_model()

# Initialize service after model is loaded
if model is not None:
    sensor_service = SensorService(model, text_store, sensor_data_list)
    form_sensor_router.set_service(sensor_service)

# Initialize CV service (doesn't need ML model)
cv_service = CVService(cv_store)
doc_sensor_router.set_service(cv_service)

# Initialize Form OCR service (doesn't need ML model)
form_ocr_service = FormOCRService(form_store)
form_ocr_module.set_service(form_ocr_service)

# Include module routers
app.include_router(form_sensor_router.router)
app.include_router(doc_sensor_router.router)
app.include_router(form_ocr_module.router)

@app.get("/")
async def root():
    return {"message": "Semantic Description Sensor API is running"}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    model_status = "loaded" if model is not None else "failed"
    health_status = "healthy" if model is not None else "degraded"
    
    return HealthResponse(
        status=health_status,
        service="semantic-sensor-api",
        model="all-MiniLM-L6-v2",
        model_status=model_status,
        model_error=model_error
    )

@app.post("/reload-model")
async def reload_model():
    """Reload the sentence transformer model"""
    global sensor_service, cv_service, form_ocr_service
    success = load_model()
    if success:
        # Reinitialize form-sensor service with new model
        sensor_service = SensorService(model, text_store, sensor_data_list)
        form_sensor_router.set_service(sensor_service)
        
        # Reinitialize CV service (doesn't need model)
        cv_service = CVService(cv_store)
        doc_sensor_router.set_service(cv_service)
        
        # Reinitialize Form OCR service (doesn't need model)
        form_ocr_service = FormOCRService(form_store)
        form_ocr_router.set_service(form_ocr_service)
        
        return {"message": "Model reloaded successfully", "status": "loaded"}
    else:
        raise HTTPException(
            status_code=503, 
            detail=f"Failed to reload model: {model_error}"
        )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)