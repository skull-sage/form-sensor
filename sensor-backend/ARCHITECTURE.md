# Backend Architecture

## Modular Structure

The backend is now organized into modules, where each module contains its own:
- **Router**: API endpoints and route definitions
- **Services**: Business logic and core functionality
- **Schemas**: Pydantic models for request/response validation
- **Validators**: Input validation functions
- **Models**: Database models (if applicable)

## Current Modules

### form-sensor Module
Location: `sensor-backend/form-sensor/`

**Purpose**: Semantic text similarity detection using sentence transformers

**Components**:
- `router.py` - API endpoints with `/form-sensor` prefix
- `services.py` - SensorService class with business logic
- `schemas.py` - Pydantic models for validation
- `validators.py` - Input validation functions
- `models.py` - SQLAlchemy models (currently unused)

**API Endpoints**:
- `POST /form-sensor/create-text-sensor/{name_id}` - Create new text sensor
- `POST /form-sensor/text-sensor/{name_id}` - Check similarity against sensor
- `GET /form-sensor/text-sensors` - List all sensors
- `DELETE /form-sensor/text-sensor/{name_id}` - Delete sensor
- `POST /form-sensor/bulk-create-sensors` - Bulk create sensors

## Main Application (main.py)

The main application file:
1. Initializes FastAPI app
2. Configures CORS and middleware
3. Loads the sentence transformer model
4. Creates shared storage (text_store, sensor_data_list)
5. Initializes module services
6. Includes module routers
7. Provides global endpoints (health check, model reload)

## Adding New Modules

To add a new module:

1. Create a new folder: `sensor-backend/your-module/`
2. Add required files:
   - `__init__.py`
   - `router.py` - Define APIRouter with prefix
   - `services.py` - Business logic
   - `schemas.py` - Pydantic models
   - `validators.py` - Validation functions
   - `models.py` - Database models (optional)

3. In `main.py`:
   ```python
   from your_module import router as your_module_router
   from your_module.services import YourService
   
   # Initialize service
   your_service = YourService(dependencies)
   your_module_router.set_service(your_service)
   
   # Include router
   app.include_router(your_module_router.router)
   ```

## Benefits of Modular Architecture

- **Separation of Concerns**: Each module handles its own domain
- **Scalability**: Easy to add new features without affecting existing code
- **Maintainability**: Clear structure makes code easier to understand
- **Testability**: Modules can be tested independently
- **Reusability**: Services and validators can be shared across modules
