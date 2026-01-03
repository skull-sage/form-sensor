# Doc Sensor Frontend Implementation

## Quick Start

### Access the Application
1. Start backend: `cd sensor-backend && python -m uvicorn main:app --reload`
2. Start frontend: `cd sensor-ui && pnpm dev`
3. Navigate to: `http://localhost:9000/doc-sensor/upload`

### Routes
- `/doc-sensor/upload` - Upload and analyze CVs
- `/doc-sensor/list` - View CV library

## File Structure

```
sensor-ui/src/app-main/doc-sensor/
├── index.vue              # Main container with tabs
├── cv-upload.vue          # Upload and analysis interface
├── cv-list.vue            # CV library and management
├── route-config.ts        # Route configuration
├── README.md              # Component documentation
└── IMPLEMENTATION.md      # This file
```

## Components Overview

### index.vue
- Container component with header and tab navigation
- Uses `activity-container` and `a-page` layout components
- Indigo color scheme for consistency

### cv-upload.vue
**Features:**
- PDF file upload with validation
- Single-step upload and analysis
- Display analysis results:
  - Basic info (name, email, phone, location, social links)
  - Work experience (timeline view)
  - Skills (chips)
  - Education (list)
- Actions: Upload another, View library

**API Call:**
```typescript
POST /doc-sensor/analyze-cv
Content-Type: multipart/form-data
Body: { file: File }
```

### cv-list.vue
**Features:**
- List all uploaded CVs
- Expandable cards with full analysis
- Delete CV with confirmation
- Refresh list
- Empty state and loading states

**API Calls:**
```typescript
GET /doc-sensor/cvs              # List all CVs
GET /doc-sensor/cv/:id           # Get CV details
DELETE /doc-sensor/cv/:id        # Delete CV
```

## Styling

### Color Scheme
- **Primary**: Indigo (header, buttons, accents)
- **Skills**: Teal chips
- **Status**: Green (analyzed), Grey (not analyzed)
- **Background**: Grey-1

### Components Used
- `q-card` - Content containers
- `q-chip` - Skills display
- `q-timeline` - Work experience
- `q-list` - Education
- `q-file` - File upload
- `q-btn` - Actions
- `q-dialog` - Confirmations

## API Configuration

Update `API_BASE_URL` if backend runs on different port:

```typescript
// In cv-upload.vue and cv-list.vue
const API_BASE_URL = 'http://localhost:8000'
```

## Testing Checklist

- [ ] Upload a valid PDF CV
- [ ] Verify analysis results display correctly
- [ ] Check all sections (basic info, experience, skills, education)
- [ ] Test file validation (non-PDF, large file)
- [ ] View CV library
- [ ] Expand CV details
- [ ] Delete CV
- [ ] Upload another CV after analysis
- [ ] Test empty state (no CVs)
- [ ] Test error handling (backend down)

## Known Limitations

1. **In-memory storage** - CVs are lost on backend restart
2. **No authentication** - Anyone can access all CVs
3. **Basic extraction** - Regex-based parsing may miss complex formats
4. **No PDF preview** - Cannot view original PDF in browser
5. **No editing** - Cannot edit extracted data

## Future Enhancements

### Short-term
- [ ] Add loading spinner during analysis
- [ ] Show upload progress
- [ ] Add CV search/filter
- [ ] Export CV data (JSON/CSV)
- [ ] Improve error messages

### Long-term
- [ ] PDF preview in browser
- [ ] Edit extracted data
- [ ] Batch upload
- [ ] Skill matching against job requirements
- [ ] CV scoring and ranking
- [ ] Tags and categories
- [ ] Compare CVs side-by-side
- [ ] Advanced NLP for better extraction

## Troubleshooting

### Backend not responding
- Check backend is running: `http://localhost:8000/docs`
- Verify CORS is enabled in backend
- Check browser console for errors

### File upload fails
- Verify file is PDF format
- Check file size < 10MB
- Ensure backend has PyPDF2 installed

### Analysis returns empty data
- Check PDF has extractable text (not image-based)
- Verify CV has standard sections (Experience, Skills, Education)
- Check backend logs for extraction errors

### Routes not working
- Verify route is registered in `src/router/routes.ts`
- Check route-config.ts exports correctly
- Clear browser cache and reload

## Development Tips

1. **Hot reload**: Frontend auto-reloads on file changes
2. **Backend logs**: Watch terminal for API errors
3. **Browser DevTools**: Check Network tab for API calls
4. **Vue DevTools**: Inspect component state and props
5. **Test data**: Create sample CVs with clear sections for testing

## Related Files

- Backend: `sensor-backend/doc-sensor/`
- Specs: `.kiro/specs/doc-sensor/`
- Routes: `sensor-ui/src/router/routes.ts`
- Main app: `sensor-ui/src/app-main/index.vue`
