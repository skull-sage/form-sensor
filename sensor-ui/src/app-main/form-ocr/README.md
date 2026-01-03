# Form OCR Frontend Module

Vue.js/Quasar frontend components for the Form OCR module.

## Components

### index.vue
Main layout component with tab navigation between Upload and Library views.

### form-upload.vue
Form upload and processing component with:
- PDF file upload (max 20MB)
- OCR options configuration
  - Language selection (English, Chinese, French, German, Korean, Japanese)
  - Perspective correction toggle
  - Form segment detection toggle
  - GPU acceleration toggle
  - Confidence threshold slider
- Real-time processing with progress indicator
- Results display with:
  - Original vs corrected image comparison
  - Detected form fields (label-value pairs)
  - All text regions with confidence scores
  - Processing metadata

### form-list.vue
Form library and management component with:
- List of all processed forms
- Form details expansion
- Processing status indicators
- Page summaries
- Form fields display
- Image viewer dialog (original vs corrected)
- Delete functionality
- Refresh capability

## Routes

- `/form-ocr/upload` - Upload and process forms
- `/form-ocr/list` - View form library

## API Integration

Connects to backend endpoints:
- `POST /form-ocr/process-form` - Upload and process form
- `GET /form-ocr/forms` - List all forms
- `GET /form-ocr/form/:id` - Get form details
- `GET /form-ocr/form/:id/images` - Get form images
- `DELETE /form-ocr/form/:id` - Delete form

## Features

### Upload & Process
- Drag-and-drop file upload
- File validation (PDF only, max 20MB)
- Configurable OCR options
- Real-time processing feedback
- Side-by-side image comparison
- Structured form field extraction
- Confidence score visualization

### Form Library
- Searchable form list
- Status indicators (completed, processing, failed)
- Expandable details view
- Image viewer with page navigation
- Bulk operations support
- Delete with confirmation

## Usage

### Basic Upload
```vue
<template>
  <form-upload />
</template>
```

### View Library
```vue
<template>
  <form-list />
</template>
```

### Navigation
```typescript
// Navigate to upload
router.push({ name: 'form-ocr.upload' })

// Navigate to library
router.push({ name: 'form-ocr.list' })
```

## Configuration

### API Base URL
Update in component files:
```typescript
const API_BASE_URL = 'http://localhost:8000'
```

### Language Options
Configured in `form-upload.vue`:
```typescript
const languageOptions = [
  { label: 'English', value: 'en' },
  { label: 'Chinese', value: 'ch' },
  // ... more languages
]
```

## Styling

Components use Quasar's built-in styling with custom enhancements:
- Deep purple theme for headers
- Confidence-based color coding (green/yellow/red)
- Smooth transitions and animations
- Responsive layout (mobile-friendly)
- Card-based design

## Error Handling

All API calls include comprehensive error handling:
- Network errors
- HTTP errors (400, 413, 422, 404, 500)
- Validation errors
- User-friendly error messages via Quasar Notify

## Performance

- Lazy loading of form details
- Image loading with spinners
- Optimized re-renders
- Efficient list updates
- Base64 image caching

## Accessibility

- Semantic HTML structure
- ARIA labels on interactive elements
- Keyboard navigation support
- Screen reader friendly
- High contrast color schemes

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Development

### Local Development
```bash
cd sensor-ui
npm install
npm run dev
```

### Build for Production
```bash
npm run build
```

## Testing

### Manual Testing Checklist
- [ ] Upload PDF file
- [ ] Configure OCR options
- [ ] Process form successfully
- [ ] View results (images, fields, text regions)
- [ ] Navigate to form library
- [ ] Expand form details
- [ ] View images in dialog
- [ ] Delete form
- [ ] Test error scenarios (invalid file, large file, etc.)

## Future Enhancements

- [ ] Batch upload support
- [ ] Export results (JSON, CSV, Excel)
- [ ] Form template management
- [ ] Advanced search and filtering
- [ ] Form comparison view
- [ ] Annotation tools
- [ ] Print functionality
- [ ] Share/collaborate features

## Dependencies

- Vue 3
- Quasar Framework
- Vue Router
- TypeScript

## Related Documentation

- Backend API: `sensor-backend/form-ocr/README.md`
- Testing Guide: `sensor-backend/form-ocr/TESTING.md`
- Quick Start: `sensor-backend/form-ocr/QUICK_START.md`
