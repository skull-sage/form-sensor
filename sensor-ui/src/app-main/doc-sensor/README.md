# Doc Sensor Frontend Module

Frontend components for CV/Resume analysis and management.

## Components

### 1. `index.vue`
Main container component with navigation tabs.

**Features:**
- Header with "CV Analysis" title
- Tab navigation between Upload and Library views
- Consistent layout with other modules

### 2. `cv-upload.vue`
CV upload and analysis interface.

**Features:**
- PDF file upload with drag-and-drop support
- File validation (PDF only, max 10MB)
- Real-time CV analysis
- Display of analysis results:
  - Basic information (name, email, phone, location, social links)
  - Work experience timeline
  - Skills as chips
  - Education qualifications
- Actions to upload another CV or view library

**API Endpoint:**
- `POST /doc-sensor/analyze-cv` - Upload and analyze CV

### 3. `cv-list.vue`
CV library and management interface.

**Features:**
- List of all uploaded CVs
- CV metadata display (filename, upload date, analysis status)
- Expandable CV details with full analysis
- Delete CV functionality
- Refresh list
- Navigate to upload page

**API Endpoints:**
- `GET /doc-sensor/cvs` - Get list of all CVs
- `GET /doc-sensor/cv/:id` - Get CV details
- `DELETE /doc-sensor/cv/:id` - Delete CV

## Routes

- `/doc-sensor` - Main container
  - `/upload` - Upload and analyze CV
  - `/list` - CV library

## Usage

### Navigate to CV Analysis
```typescript
// In template
<q-btn :to="{name: 'doc-sensor.upload'}" label="Upload CV" />
<q-btn :to="{name: 'doc-sensor.list'}" label="View CVs" />

// In script
import { useRouter } from 'vue-router'
const router = useRouter()
router.push({ name: 'doc-sensor.upload' })
```

### API Configuration
Update the `API_BASE_URL` constant in each component if your backend runs on a different port:

```typescript
const API_BASE_URL = 'http://localhost:8000'
```

## Styling

Components use Quasar's built-in components and styling:
- Cards for content containers
- Chips for skills display
- Timeline for work experience
- Lists for education
- Icons from Material Design

Color scheme:
- Primary: Indigo (header and accents)
- Skills: Teal chips
- Status: Green (analyzed), Grey (not analyzed)

## Development

### Testing the Frontend

1. Start the backend server:
```bash
cd sensor-backend
python -m uvicorn main:app --reload
```

2. Start the frontend dev server:
```bash
cd sensor-ui
npm run dev
# or
pnpm dev
```

3. Navigate to `/doc-sensor/upload` to test CV upload
4. Navigate to `/doc-sensor/list` to view uploaded CVs

### Sample CV for Testing

Create a simple PDF CV with:
- Name and contact info at the top
- Work Experience section
- Skills section
- Education section

The parser will extract structured data from these sections.

## Future Enhancements

- [ ] Advanced search and filtering in CV library
- [ ] Export CV data to JSON/CSV
- [ ] Compare multiple CVs side-by-side
- [ ] Skill matching against job requirements
- [ ] CV scoring and ranking
- [ ] Batch CV upload
- [ ] PDF preview in browser
- [ ] Edit extracted data
- [ ] Tags and categories for CVs
