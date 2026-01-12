from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse 
import uvicorn
import json
 
from cv_sensor.router import router as cv_sensor_router 

app = FastAPI(
    title="Semantic Description CV Sensor API",
    description="API for semantic similarity detection using sentence transformers - Bi Encoder",
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
 

  

# Include module routers 
app.include_router(cv_sensor_router)

@app.get("/")
async def root():
    return {"message": "Semantic Description Sensor API is running"}
 

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)