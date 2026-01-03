# Modular Project Structure

## Overview

This project follows a modular architecture where each feature is organized as a self-contained module with its own code, specifications, and documentation.

## Directory Structure

```
form-sensor/
├── .kiro/
│   └── specs/                          # Specification documents
│       ├── README.md                   # Specs structure guide
│       ├── form-sensor/                # Form sensor module specs
│       │   ├── requirements.md         # User stories & acceptance criteria
│       │   ├── design.md              # Architecture & design decisions
│       │   └── tasks.md               # Implementation tasks & progress
│       └── doc-sensor/                 # Document sensor module specs (template)
│           ├── requirements.md
│           ├── design.md
│           └── tasks.md
│
├── sensor-backend/                     # Backend application
│   ├── form-sensor/                    # Form sensor module
│   │   ├── __init__.py
│   │   ├── router.py                  # API endpoints (/form-sensor/*)
│   │   ├── services.py                # Business logic
│   │   ├── schemas.py                 # Pydantic models
│   │   ├── validators.py              # Input validation
│   │   └── models.py                  # Database models
│   │
│   ├── main.py                        # App initialization & module registration
│   ├── ARCHITECTURE.md                # Backend architecture guide
│   ├── MIGRATION_GUIDE.md             # Migration documentation
│   └── requirements.txt               # Python dependencies
│
├── sensor-ui/                          # Frontend application
│   └── src/
│       └── app-main/
│           └── form-sensor/            # Form sensor UI components
│               ├── index.vue          # Module layout
│               ├── field-list.vue     # Sensor management
│               ├── field-verify.vue   # Similarity checking
│               ├── route-config.ts    # Module routes
│               └── README.md          # Component documentation
│
└── README.md                           # Project overview
```

## Module Organization

### Backend Modules (sensor-backend/)

Each backend module contains:
- **router.py**: API endpoints with module prefix (e.g., `/form-sensor/*`)
- **services.py**: Business logic and core functionality
- **schemas.py**: Pydantic models for request/response validation
- **validators.py**: Input validation functions
- **models.py**: Database models (SQLAlchemy)

### Frontend Modules (sensor-ui/src/app-main/)

Each frontend module contains:
- **index.vue**: Module layout and navigation
- **Component files**: Feature-specific Vue components
- **route-config.ts**: Module routing configuration
- **README.md**: Component documentation

### Specification Modules (.kiro/specs/)

Each spec module contains:
- **requirements.md**: User stories and acceptance criteria
- **design.md**: Architecture and design decisions
- **tasks.md**: Implementation tasks and progress tracking

## Current Modules

### 1. form-sensor
**Status**: ✅ Implemented
**Purpose**: Semantic text similarity detection for form field validation

**Backend**: `sensor-backend/form-sensor/`
- API Prefix: `/form-sensor`
- Endpoints: create-text-sensor, text-sensor, text-sensors, bulk-create-sensors

**Frontend**: `sensor-ui/src/app-main/form-sensor/`
- Routes: `/smart-form/list`, `/smart-form/verify`
- Components: field-list.vue, field-verify.vue

**Specs**: `.kiro/specs/form-sensor/`
- Requirements: 7 user stories with acceptance criteria
- Design: Architecture, API endpoints, data models
- Tasks: Implementation checklist with progress tracking

### 2. doc-sensor
**Status**: ✅ Implemented
**Purpose**: CV/Resume document analysis and information extraction

**Backend**: `sensor-backend/doc-sensor/`
- API Prefix: `/doc-sensor`
- Endpoints: analyze-cv, cv/:id, cvs, cv/:id/skills

**Frontend**: `sensor-ui/src/app-main/doc-sensor/`
- Routes: `/doc-sensor/upload`, `/doc-sensor/list`
- Components: cv-upload.vue, cv-list.vue

**Specs**: `.kiro/specs/doc-sensor/`
- Requirements: 12 user stories with acceptance criteria
- Design: Architecture, API endpoints, data models
- Tasks: Implementation checklist with progress tracking

### 3. form-ocr
**Status**: ✅ Implemented
**Purpose**: Scanned paper form document processing with perspective correction and OCR

**Backend**: `sensor-backend/form-ocr/`
- API Prefix: `/form-ocr`
- Endpoints: process-form, form/:id, forms, form/:id/images
- Features: PDF upload, perspective correction (OpenCV), OCR (PaddleOCR), form segment detection, field extraction

**Frontend**: `sensor-ui/src/app-main/form-ocr/` (to be implemented)
- Planned Routes: `/form-ocr/upload`, `/form-ocr/list`
- Planned Components: form-upload.vue, form-results.vue, form-list.vue

**Specs**: `.kiro/specs/form-ocr/`
- Requirements: 12 requirements including perspective correction and segment detection
- Design: Complete architecture with processing pipeline
- Tasks: Backend implementation completed, frontend pending

## Adding a New Module

### 1. Create Specifications

```bash
# Create spec folder
mkdir .kiro/specs/your-module

# Create spec files
touch .kiro/specs/your-module/requirements.md
touch .kiro/specs/your-module/design.md
touch .kiro/specs/your-module/tasks.md
```

Follow the templates in `.kiro/specs/README.md`

### 2. Create Backend Module

```bash
# Create module folder
mkdir sensor-backend/your-module

# Create module files
touch sensor-backend/your-module/__init__.py
touch sensor-backend/your-module/router.py
touch sensor-backend/your-module/services.py
touch sensor-backend/your-module/schemas.py
touch sensor-backend/your-module/validators.py
touch sensor-backend/your-module/models.py
```

### 3. Register Module in main.py

```python
from your_module import router as your_module_router
from your_module.services import YourService

# Initialize service
your_service = YourService(dependencies)
your_module_router.set_service(your_service)

# Include router
app.include_router(your_module_router.router)
```

### 4. Create Frontend Module

```bash
# Create module folder
mkdir sensor-ui/src/app-main/your-module

# Create component files
touch sensor-ui/src/app-main/your-module/index.vue
touch sensor-ui/src/app-main/your-module/route-config.ts
touch sensor-ui/src/app-main/your-module/README.md
```

### 5. Register Routes

Update `sensor-ui/src/router/routes.ts`:

```typescript
import YourModuleRoute from 'src/app-main/your-module/route-config'

const routes: RouteRecordRaw[] = [
  // ... existing routes
  {
    ...YourModuleRoute
  }
]
```

## Benefits of Modular Structure

1. **Separation of Concerns**: Each module handles its own domain
2. **Scalability**: Easy to add new features without affecting existing code
3. **Maintainability**: Clear structure makes code easier to understand
4. **Testability**: Modules can be tested independently
5. **Collaboration**: Multiple developers can work on different modules
6. **Documentation**: Specs serve as living documentation
7. **Traceability**: Clear mapping from requirements → design → implementation

## Development Workflow

1. **Plan**: Write requirements.md for the module
2. **Design**: Create design.md with architecture decisions
3. **Task**: Break down implementation in tasks.md
4. **Implement**: Follow tasks.md, checking off completed items
5. **Test**: Verify against requirements and properties
6. **Document**: Update specs as requirements evolve
7. **Review**: Review specs and code together

## Module Communication

Modules can communicate through:
- **Shared Services**: Common utilities in main.py
- **API Calls**: Frontend modules call backend endpoints
- **Events**: Event-driven communication (future)
- **Shared State**: Vuex/Pinia stores (frontend)

## Best Practices

1. **Keep modules independent**: Minimize dependencies between modules
2. **Use consistent naming**: Follow naming conventions across modules
3. **Document APIs**: Keep API documentation up to date
4. **Version specs**: Commit spec changes with code changes
5. **Test thoroughly**: Write tests for each module
6. **Review regularly**: Review module structure during retrospectives

## References

- Backend Architecture: `sensor-backend/ARCHITECTURE.md`
- Migration Guide: `sensor-backend/MIGRATION_GUIDE.md`
- Specs Guide: `.kiro/specs/README.md`
- Project README: `README.md`
