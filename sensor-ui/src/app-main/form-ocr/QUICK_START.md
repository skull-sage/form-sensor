# Form OCR Frontend - Quick Start Guide

Get started with the Form OCR frontend in 5 minutes.

## Prerequisites

1. **Backend running** at http://localhost:8000
   ```bash
   cd sensor-backend
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   python main.py
   ```
2. **Frontend dependencies installed**

## Installation

```bash
cd sensor-ui
npm install
```

## Start Development Server

```bash
npm run dev
```

Access at: http://localhost:9000

## Quick Usage

### 1. Navigate to Form OCR

Open your browser and go to:
```
http://localhost:9000/form-ocr/upload
```

### 2. Upload a Form

1. Click "Select PDF file" or drag-and-drop a PDF
2. (Optional) Configure OCR options:
   - Select language
   - Enable/disable perspective correction
   - Enable/disable segment detection
   - Adjust confidence threshold
3. Click "Process Form"

### 3. View Results

After processing, you'll see:
- Original vs corrected images
- Detected form fields (label-value pairs)
- All text regions with confidence scores
- Processing metadata

### 4. View Form Library

Navigate to the library:
```
http://localhost:9000/form-ocr/list
```

Features:
- View all processed forms
- Expand to see details
- View images in full-screen
- Delete forms

## Routes

| Route | Component | Description |
|-------|-----------|-------------|
| `/form-ocr/upload` | form-upload.vue | Upload and process forms |
| `/form-ocr/list` | form-list.vue | View form library |

## Components Overview

### form-upload.vue
Upload and process scanned forms with OCR.

**Features:**
- PDF file upload (max 20MB)
- OCR options configuration
- Real-time processing
- Results visualization

### form-list.vue
Manage and view processed forms.

**Features:**
- Form list with status
- Expandable details
- Image viewer
- Delete functionality

## Configuration

### API Base URL

Update in component files if backend is on different host:

```typescript
// form-upload.vue and form-list.vue
const API_BASE_URL = 'http://localhost:8000'
```

### Language Options

Available languages:
- English (en)
- Chinese (ch)
- French (fr)
- German (german)
- Korean (korean)
- Japanese (japan)

## Common Tasks

### Upload and Process a Form

```typescript
// 1. Select file
const file = document.querySelector('input[type="file"]').files[0]

// 2. Create form data
const formData = new FormData()
formData.append('file', file)
formData.append('language', 'en')
formData.append('enable_segment_detection', 'true')

// 3. Submit
const response = await fetch('http://localhost:8000/form-ocr/process-form', {
  method: 'POST',
  body: formData
})

const result = await response.json()
console.log('Form ID:', result.form_id)
```

### View Form Details

```typescript
const formId = 'your-form-id'
const response = await fetch(`http://localhost:8000/form-ocr/form/${formId}`)
const details = await response.json()
console.log('Form details:', details)
```

### Delete a Form

```typescript
const formId = 'your-form-id'
const response = await fetch(`http://localhost:8000/form-ocr/form/${formId}`, {
  method: 'DELETE'
})
const result = await response.json()
console.log(result.message)
```

## Troubleshooting

### Issue: Routes not working
**Solution**: Ensure you've registered the routes in `routes.ts`

### Issue: API calls failing
**Solution**:
1. Check backend is running at http://localhost:8000
   ```bash
   cd sensor-backend
   source venv/bin/activate
   python main.py
   ```
2. Check CORS is enabled in backend
3. Check browser console for errors

### Issue: Images not displaying
**Solution**:
1. Check base64 data is valid
2. Check browser console for errors
3. Try refreshing the page

### Issue: File upload fails
**Solution**:
1. Ensure file is PDF format
2. Check file size is under 20MB
3. Check backend logs for errors

## Development Tips

### Hot Reload
Changes to Vue files will hot-reload automatically.

### Vue DevTools
Install Vue DevTools browser extension for debugging:
- Chrome: https://chrome.google.com/webstore
- Firefox: https://addons.mozilla.org/firefox

### API Testing
Use browser DevTools Network tab to inspect API calls.

### Component Props
Use Vue DevTools to inspect component props and state.

## Next Steps

1. **Test the upload flow** with sample PDFs
2. **Explore OCR options** to see how they affect results
3. **View the form library** to manage processed forms
4. **Check the documentation** for advanced features

## Related Documentation

- Component README: `README.md`
- Implementation Guide: `IMPLEMENTATION.md`
- Backend API: `sensor-backend/form-ocr/README.md`
- Backend Testing: `sensor-backend/form-ocr/TESTING.md`

## Support

For issues or questions:
1. Check the documentation
2. Review backend logs
3. Check browser console
4. Review API responses

## Quick Reference

### Keyboard Shortcuts
- `Ctrl/Cmd + Click` - Open link in new tab
- `Esc` - Close dialogs
- `Tab` - Navigate between fields

### Status Colors
- 🟢 Green - High confidence (≥80%)
- 🟡 Yellow - Medium confidence (60-79%)
- 🔴 Red - Low confidence (<60%)

### File Limits
- Max file size: 20MB
- Supported format: PDF only
- Pages: Unlimited

---

**Happy Form Processing! 📄✨**
