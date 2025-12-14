# Implementation Plan

- [x] 1. Set up core backend structure and dependencies
  - Install sentence-transformers and required dependencies
  - Configure FastAPI with CORS for frontend communication
  - Create basic project structure with main.py
  - _Requirements: 4.1, 7.1_

- [x] 2. Implement text sensor creation endpoint
  - [x] 2.1 Create POST /create-text-sensor/:nameId endpoint
    - Parse nameId from URL path
    - Accept {"text": "paragraphs"} in request body
    - Split text by newlines into paragraph array
    - Store paragraph mapping: nameId → [paragraphs]
    - _Requirements: 1.1, 1.2_

  - [x] 2.2 Implement embedding generation and storage
    - Load all-MiniLM-L6-v2 sentence transformer model
    - Generate embeddings for each paragraph
    - Store embedding mapping: nameId → [embeddings] parallel to paragraphs
    - Return success response with paragraph count
    - _Requirements: 1.3, 1.4_

  - [ ]* 2.3 Write property test for text splitting consistency
    - **Property 1: Text Splitting Consistency**
    - **Validates: Requirements 1.1**

  - [ ]* 2.4 Write property test for paragraph-embedding correspondence
    - **Property 2: Paragraph-Embedding Correspondence**
    - **Validates: Requirements 1.2, 1.4**

- [x] 3. Implement similarity checking endpoint
  - [x] 3.1 Create POST /text-sensor/:nameId endpoint
    - Parse nameId from URL path
    - Accept {"text": "description"} in request body
    - Generate embedding for input text
    - Retrieve stored embeddings for nameId
    - _Requirements: 2.1, 2.2_

  - [x] 3.2 Implement cosine similarity calculation and response logic
    - Calculate cosine similarity between input and all stored embeddings
    - Return highest similarity score as {"confidence_score": score} regardless of threshold
    - Frontend can use 0.6 threshold for guidance but API always returns actual score
    - _Requirements: 2.3, 2.4, 3.2, 3.4, 3.5_

  - [ ]* 3.3 Write property test for similarity calculation range
    - **Property 5: Similarity Calculation Range**
    - **Validates: Requirements 2.3**

  - [ ]* 3.4 Write property test for confidence score response format
    - **Property 6: Confidence Score Response Format**
    - **Validates: Requirements 2.4**

- [x] 4. Implement sensor management endpoints
  - [x] 4.1 Create GET /text-sensors endpoint
    - Return list of all stored nameIds
    - Return count of sensors
    - Format: {"sensors": [...], "count": N}
    - _Requirements: 4.4_

  - [x] 4.2 Create DELETE /text-sensor/:nameId endpoint
    - Remove paragraph mapping for nameId
    - Remove embedding mapping for nameId
    - Return success confirmation
    - _Requirements: 4.5_

  - [ ]* 4.3 Write property test for sensor CRUD operations
    - **Property 9: Sensor CRUD Operations**
    - **Validates: Requirements 4.2, 4.4, 4.5**

- [x] 5. Add error handling and validation
  - [x] 5.1 Implement input validation
    - Validate JSON request bodies
    - Handle empty/null text inputs
    - Return appropriate HTTP status codes
    - _Requirements: 6.1, 6.4_

  - [x] 5.2 Add nameId existence checking
    - Return 404 when nameId not found for similarity checking
    - Handle model loading failures gracefully
    - _Requirements: 6.2_

  - [ ]* 5.3 Write property test for input validation error handling
    - **Property 8: Input Validation Error Handling**
    - **Validates: Requirements 6.1, 6.4**

- [ ] 6. Update frontend for new API endpoints
  - [ ] 6.1 Modify SemanticSensor.vue for new endpoint structure
    - Update API calls to use /create-text-sensor/:nameId
    - Update API calls to use /text-sensor/:nameId
    - Handle {"confidence_score": score} response format
    - _Requirements: 5.1, 5.3_

  - [ ] 6.2 Add nameId management to frontend
    - Add input field for nameId when creating sensors
    - Add dropdown/selection for nameId when checking similarity
    - Display list of available sensors
    - _Requirements: 5.2, 5.4_

- [ ] 7. Final integration and testing
  - [ ] 7.1 Test complete workflow end-to-end
    - Create text sensor with multiple paragraphs
    - Check similarity with various input texts
    - Verify confidence scores and threshold behavior
    - Test sensor listing and deletion
    - _Requirements: All_

  - [ ] 7.2 Ensure all tests pass, ask the user if questions arise