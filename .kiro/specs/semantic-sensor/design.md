# Design Document

## Overview

The Semantic Description Sensor is a full-stack application that provides semantic similarity detection using sentence transformers. The system consists of a FastAPI backend that processes text using the all-MiniLM-L6-v2 model and a Vue.js frontend for user interaction. The core functionality revolves around creating "text sensors" from multi-paragraph text and checking semantic similarity against stored paragraph embeddings.

## Architecture

The system follows a clean architecture pattern with clear separation between layers:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   ML Model      │
│   (Vue/Quasar)  │◄──►│   (FastAPI)     │◄──►│ (Transformers)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Data Storage  │
                       │  (In-Memory)    │
                       └─────────────────┘
```

### Component Responsibilities

- **Frontend**: User interface for creating text sensors and checking similarity
- **Backend API**: RESTful endpoints, text processing, and similarity calculations  
- **ML Model**: Sentence transformer for generating embeddings
- **Data Storage**: In-memory storage for paragraph and embedding mappings

## Components and Interfaces

### Backend Components

#### TextSensorService
- **Purpose**: Core business logic for text sensor operations
- **Methods**:
  - `create_text_sensor(name_id: str, text: str) -> dict`
  - `check_similarity(name_id: str, text: str) -> dict`
  - `get_all_sensors() -> list`
  - `delete_sensor(name_id: str) -> bool`

#### EmbeddingService  
- **Purpose**: Handles sentence transformer operations
- **Methods**:
  - `generate_embedding(text: str) -> np.ndarray`
  - `calculate_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float`
  - `load_model() -> SentenceTransformer`

#### StorageService
- **Purpose**: Manages in-memory data storage
- **Methods**:
  - `store_paragraphs(name_id: str, paragraphs: list) -> None`
  - `store_embeddings(name_id: str, embeddings: list) -> None`
  - `get_paragraphs(name_id: str) -> list`
  - `get_embeddings(name_id: str) -> list`
  - `delete_sensor_data(name_id: str) -> bool`

### API Endpoints

#### POST /create-text-sensor/:nameId
- **Input**: `{"text": "paragraph1\nparagraph2\nparagraph3"}`
- **Output**: `{"message": "Text sensor created", "paragraphs_count": 3}`
- **Process**: Split text → Store paragraphs → Generate embeddings → Store embeddings

#### POST /text-sensor/:nameId  
- **Input**: `{"text": "description to check"}`
- **Output**: `{"confidence_score": 0.75}` (always returns actual highest score)
- **Process**: Generate embedding → Compare with stored embeddings → Return highest similarity score

#### GET /text-sensors
- **Output**: `{"sensors": ["sensor1", "sensor2"], "count": 2}`

#### DELETE /text-sensor/:nameId
- **Output**: `{"message": "Text sensor deleted"}`

## Data Models

### Text Sensor Storage Structure
```python
# Paragraph mappings
paragraph_store = {
    "nameId1": ["paragraph1", "paragraph2", "paragraph3"],
    "nameId2": ["paragraph1", "paragraph2"]
}

# Embedding mappings (parallel structure)
embedding_store = {
    "nameId1": [embedding1, embedding2, embedding3],
    "nameId2": [embedding1, embedding2]
}
```

### API Request/Response Models
```python
class CreateSensorRequest(BaseModel):
    text: str

class SimilarityRequest(BaseModel):
    text: str

class SimilarityResponse(BaseModel):
    confidence_score: float

class SensorListResponse(BaseModel):
    sensors: List[str]
    count: int
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Text Splitting Consistency
*For any* input text with newline separators, splitting the text should produce an array where the number of paragraphs equals the number of newline-separated segments
**Validates: Requirements 1.1**

### Property 2: Paragraph-Embedding Correspondence  
*For any* nameId with stored paragraphs, the number of stored embeddings should equal the number of stored paragraphs
**Validates: Requirements 1.2, 1.4**

### Property 3: Embedding Generation Determinism
*For any* paragraph text, generating an embedding should produce a vector with consistent dimensions matching the all-MiniLM-L6-v2 model output
**Validates: Requirements 1.3**

### Property 4: Sensor Replacement Completeness
*For any* existing nameId, creating a new text sensor should completely replace both paragraph and embedding data with new values
**Validates: Requirements 1.5**

### Property 5: Similarity Calculation Range
*For any* two text embeddings, cosine similarity calculation should return a value between -1 and 1
**Validates: Requirements 2.3**

### Property 6: Confidence Score Response Format
*For any* similarity check, the response should always contain the actual highest similarity score as confidence_score regardless of threshold
**Validates: Requirements 2.4**

### Property 7: Maximum Score Selection
*For any* nameId with multiple paragraphs where multiple similarities exceed 0.6, the returned confidence_score should be the maximum similarity value
**Validates: Requirements 3.4**

### Property 8: Input Validation Error Handling
*For any* invalid input (empty text, malformed JSON), the API should return appropriate HTTP error codes and descriptive messages
**Validates: Requirements 6.1, 6.4**

### Property 9: Sensor CRUD Operations
*For any* nameId, the sequence of create → list → delete operations should maintain data consistency and proper state transitions
**Validates: Requirements 4.2, 4.4, 4.5**

## Error Handling

### Input Validation Errors
- Empty or null text input → 400 Bad Request
- Missing required fields → 400 Bad Request  
- Invalid JSON format → 400 Bad Request

### Business Logic Errors
- NameId not found → 404 Not Found
- Model loading failure → 503 Service Unavailable
- Embedding generation failure → 500 Internal Server Error

### System Errors
- Memory allocation issues → 500 Internal Server Error
- Model download/loading timeout → 503 Service Unavailable

## Testing Strategy

### Unit Testing Approach
Unit tests will verify specific examples and edge cases:
- Text splitting with various newline patterns
- API endpoint request/response validation
- Error handling for invalid inputs
- CORS header verification

### Property-Based Testing Approach  
Property-based tests will verify universal properties across all inputs using **Hypothesis** for Python:
- Text splitting consistency across random input texts
- Embedding dimension consistency for any paragraph
- Similarity score ranges for any embedding pairs
- Threshold-based response logic for any similarity values
- Data structure consistency for any nameId operations

**Configuration**: Each property-based test will run a minimum of 100 iterations to ensure comprehensive coverage of the input space.

**Test Tagging**: Each property-based test will include a comment with the format: `**Feature: semantic-sensor, Property {number}: {property_text}**`

Both unit tests and property-based tests are complementary - unit tests catch concrete bugs while property tests verify general correctness across the entire input domain.