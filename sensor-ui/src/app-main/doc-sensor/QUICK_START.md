# Doc Sensor - Quick Start Guide

## 🚀 Getting Started

### 1. Start the Backend
```bash
cd sensor-backend
python -m uvicorn main:app --reload
```

Backend will run at: `http://localhost:8000`
API docs available at: `http://localhost:8000/docs`

### 2. Start the Frontend
```bash
cd sensor-ui
pnpm install  # if first time
pnpm dev
```

Frontend will run at: `http://localhost:9000` (or the port shown in terminal)

### 3. Access the Application

Navigate to: **`http://localhost:9000/doc-sensor/upload`**

## 📋 Features

### Upload & Analyze CV
1. Click "Upload & Analyze CV" tab
2. Select a PDF file (max 10MB)
3. Click "Analyze CV"
4. View extracted information:
   - Basic info (name, email, phone, location, social links)
   - Work experience
   - Skills
   - Education

### CV Library
1. Click "CV Library" tab
2. View all uploaded CVs
3. Click expand icon to see full analysis
4. Click delete icon to remove CV

## 🧪 Testing

### Create a Test CV

Create a simple PDF with these sections:

```
John Doe
john.doe@email.com | +1-234-567-8900 | San Francisco, CA
https://linkedin.com/in/johndoe | https://github.com/johndoe

WORK EXPERIENCE

Senior Software Engineer
Tech Company Inc.
2020 - Present
Developed web applications using React and Node.js

Software Engineer
Startup Co.
2018 - 2020
Built REST APIs and microservices

SKILLS

Python, JavaScript, React, Node.js, Docker, AWS, PostgreSQL

EDUCATION

Bachelor of Science in Computer Science
University of California
2018
```

### Test the Upload
1. Save the above as a PDF
2. Upload it via the interface
3. Verify all sections are extracted correctly

## 🔧 Configuration

### Change Backend URL

If your backend runs on a different port, update in both components:

**cv-upload.vue:**
```typescript
const API_BASE_URL = 'http://localhost:8000'
```

**cv-list.vue:**
```typescript
const API_BASE_URL = 'http://localhost:8000'
```

## 📁 Project Structure

```
sensor-ui/src/app-main/doc-sensor/
├── index.vue              # Main container
├── cv-upload.vue          # Upload interface
├── cv-list.vue            # Library interface
├── route-config.ts        # Routes
├── README.md              # Documentation
├── IMPLEMENTATION.md      # Implementation details
└── QUICK_START.md         # This file
```

## 🐛 Troubleshooting

### Backend not responding
```bash
# Check if backend is running
curl http://localhost:8000/docs

# Restart backend
cd sensor-backend
python -m uvicorn main:app --reload
```

### Frontend not loading
```bash
# Clear cache and restart
cd sensor-ui
rm -rf node_modules/.vite
pnpm dev
```

### File upload fails
- Ensure file is PDF format
- Check file size < 10MB
- Verify backend has PyPDF2 installed:
  ```bash
  cd sensor-backend
  pip install PyPDF2
  ```

### No data extracted
- Check PDF has text (not image-based)
- Verify CV has standard sections
- Check backend logs for errors

## 📚 API Endpoints

### Upload and Analyze
```bash
POST /doc-sensor/analyze-cv
Content-Type: multipart/form-data
Body: file (PDF)
```

### List CVs
```bash
GET /doc-sensor/cvs
```

### Get CV Details
```bash
GET /doc-sensor/cv/{cv_id}
```

### Delete CV
```bash
DELETE /doc-sensor/cv/{cv_id}
```

## 🎯 Next Steps

1. **Test with real CVs** - Upload various CV formats
2. **Refine extraction** - Improve parsing accuracy
3. **Add features** - Search, export, skill matching
4. **Production setup** - Database, auth, file storage

## 📖 More Documentation

- **README.md** - Component documentation
- **IMPLEMENTATION.md** - Implementation details
- **Backend docs** - `sensor-backend/doc-sensor/README.md`
- **Specs** - `.kiro/specs/doc-sensor/`

## 💡 Tips

- Use browser DevTools Network tab to debug API calls
- Check backend terminal for error logs
- Test with simple CVs first before complex ones
- The parser works best with standard CV formats

## ✅ Success Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 9000
- [ ] Can access /doc-sensor/upload
- [ ] Can upload a PDF file
- [ ] Analysis results display correctly
- [ ] Can view CV library
- [ ] Can delete CVs

---

**Need help?** Check the other documentation files or backend logs for more details.
