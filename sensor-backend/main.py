from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sentence_transformers import SentenceTransformer
import uvicorn
import json

from app.schemas import (
    CreateSensorRequest, SimilarityRequest, SimilarityResponse,
    BulkCreateRequest, BulkCreateResponse, SensorListResponse,
    CreateSensorResponse, DeleteSensorResponse, HealthResponse
)
from app.services import SensorService

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

# Initialize service (will be set after model loads)
sensor_service = None

# Try to load model on startup
load_model()

# Initialize service after model is loaded
if model is not None:
    sensor_service = SensorService(model, text_store, sensor_data_list)

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
    global sensor_service
    success = load_model()
    if success:
        # Reinitialize service with new model
        sensor_service = SensorService(model, text_store, sensor_data_list)
        return {"message": "Model reloaded successfully", "status": "loaded"}
    else:
        raise HTTPException(
            status_code=503, 
            detail=f"Failed to reload model: {model_error}"
        )

@app.post("/bulk-create-sensors", response_model=BulkCreateResponse)
async def bulk_create_sensors(request: BulkCreateRequest):
    """Bulk create text sensors from browser storage."""
    try:
        ensure_service_available()
        return sensor_service.bulk_create_sensors(request.sensors)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error bulk creating sensors: {str(e)}")

# Service initialization helper
def ensure_service_available():
    """Ensure the sensor service is available"""
    global sensor_service
    if sensor_service is None:
        if model is not None:
            sensor_service = SensorService(model, text_store, sensor_data_list)
        else:
            raise HTTPException(status_code=503, detail="Sensor service is not available - model not loaded")

@app.post("/create-text-sensor/{name_id}", response_model=CreateSensorResponse)
async def create_text_sensor(name_id: str, request: CreateSensorRequest):
    """Create a text sensor by splitting text into paragraphs and generating embeddings."""
    try:
        ensure_service_available()
        return sensor_service.create_sensor(name_id, request.text)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating text sensor: {str(e)}")

@app.post("/text-sensor/{name_id}", response_model=SimilarityResponse)
async def check_similarity(name_id: str, request: SimilarityRequest):
    """Check semantic similarity against a specific text sensor."""
    try:
        ensure_service_available()
        result = sensor_service.calculate_similarity(request.text, name_id)
        return SimilarityResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking similarity: {str(e)}")

@app.get("/text-sensors", response_model=SensorListResponse)
async def get_text_sensors():
    """Return mapping of nameIds to their text content and count of sensors."""
    try:
        ensure_service_available()
        result = sensor_service.get_all_sensors()
        return SensorListResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving text sensors: {str(e)}")

@app.delete("/text-sensor/{name_id}", response_model=DeleteSensorResponse)
async def delete_text_sensor(name_id: str):
    """Remove text sensor and return success confirmation."""
    try:
        ensure_service_available()
        result = sensor_service.delete_sensor(name_id)
        return DeleteSensorResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting text sensor: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)