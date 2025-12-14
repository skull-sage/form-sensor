# Semantic Description Sensor

A full-stack application that uses sentence transformers to detect semantic similarity between text descriptions. The "sensor" metaphorically detects whether a provided text description matches predefined descriptions contextually using the `all-MiniLM-L6-v2` model.

## Features

- **Semantic Similarity Detection**: Uses sentence transformers to compare text descriptions
- **Predefined Descriptions Management**: Add, view, and delete reference descriptions
- **Configurable Threshold**: Adjust similarity threshold for matching
- **Real-time Results**: Get instant similarity scores and matches
- **Category Organization**: Organize descriptions by categories

## Tech Stack

### Backend (sensor-backend/)
- **FastAPI**: Modern Python web framework
- **Sentence Transformers**: `all-MiniLM-L6-v2` model for semantic embeddings
- **Scikit-learn**: Cosine similarity calculations
- **SQLAlchemy**: Database ORM (optional, currently using in-memory storage)

### Frontend (sensor-ui/)
- **Vue 3**: Progressive JavaScript framework
- **Quasar**: Vue.js component framework
- **TypeScript**: Type-safe JavaScript
- **Axios**: HTTP client for API calls

## Quick Start

### Backend Setup
```bash
cd sensor-backend
pip install -r requirements.txt
python main.py
```
The API will be available at `http://localhost:8000`

### Frontend Setup
```bash
cd sensor-ui
npm install  # or pnpm install
npm run dev  # or pnpm dev
```
The frontend will be available at `http://localhost:9000`

## Usage

1. **Add Predefined Descriptions**: Create reference descriptions with IDs and categories
2. **Check Similarity**: Input text to compare against predefined descriptions
3. **Adjust Threshold**: Use the slider to set minimum similarity score (0-100%)
4. **View Results**: See best matches and similarity scores

## API Endpoints

- `GET /` - Health check
- `POST /descriptions/add` - Add predefined description
- `GET /descriptions` - Get all predefined descriptions
- `DELETE /descriptions/{id}` - Delete description
- `POST /similarity/check` - Check semantic similarity

## Example Use Cases

- **Content Moderation**: Check if user input matches prohibited content patterns
- **FAQ Matching**: Find relevant FAQ entries for user questions
- **Document Classification**: Categorize documents based on description similarity
- **Duplicate Detection**: Identify similar descriptions or content