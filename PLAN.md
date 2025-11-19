# Note Taker AI - Project Plan

## Overview
A note-taking app that allows users to record audio, transcribe it using AssemblyAI, and summarize it using OpenAI. This is an example application for the Render AI Agent example library.

## Tech Stack

### Backend
- **Framework:** Python with Flask API
- **Package Manager:** uv (modern Python package manager)
- **Speech-to-Text:** AssemblyAI
- **Summarization:** OpenAI GPT
- **Dependencies:**
  - Flask
  - Flask-CORS
  - AssemblyAI Python SDK
  - OpenAI Python SDK
  - python-dotenv

### Frontend
- **Framework:** Next.js 14+ (App Router)
- **Language:** TypeScript
- **UI Components:** shadcn/ui
- **Styling:** Tailwind CSS
- **Key Libraries:**
  - React hooks for audio recording
  - Fetch/Axios for API calls

### Deployment
- **Local Development:** Docker Compose
- **Production:** Render (using blueprint file)

---

## Architecture

### Backend API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/transcribe` | Upload audio file for transcription |
| GET | `/api/transcription/:id` | Get transcription status/result |
| POST | `/api/summarize/:id` | Generate summary from transcription |
| GET | `/api/notes/:id` | Get complete meeting notes (transcription + summary) |

### Frontend Pages/Components

```
app/
├── page.tsx                    # Home page with recorder
├── components/
│   ├── AudioRecorder.tsx       # Audio recording interface
│   ├── FileUploader.tsx        # Drag-and-drop upload
│   ├── TranscriptionViewer.tsx # Display transcription
│   ├── SummaryViewer.tsx       # Display AI summary
│   └── LoadingState.tsx        # Loading skeletons
└── lib/
    └── api.ts                  # API client functions
```

---

## Implementation Checklist

### Phase 1: Backend Setup
- [ ] Initialize Python project with `uv`
- [ ] Create `pyproject.toml` with dependencies
- [ ] Setup Flask application structure
- [ ] Configure CORS for frontend communication
- [ ] Add environment variable management (.env)
- [ ] Create backend Dockerfile

### Phase 2: Backend Features
- [ ] Implement audio file upload endpoint
- [ ] Integrate AssemblyAI SDK for transcription
  - [ ] Handle file upload to AssemblyAI
  - [ ] Poll for transcription completion
  - [ ] Store transcription results
- [ ] Integrate OpenAI SDK for summarization
  - [ ] Create prompt template for meeting notes
  - [ ] Generate summary from transcription
- [ ] Add error handling and validation
- [ ] Implement basic in-memory storage (or file-based)

### Phase 3: Frontend Setup
- [ ] Initialize Next.js project with TypeScript
- [ ] Configure Tailwind CSS
- [ ] Install and configure shadcn/ui
  - [ ] Add Button component
  - [ ] Add Card component
  - [ ] Add Badge component
  - [ ] Add Progress component
  - [ ] Add Textarea component
  - [ ] Add Alert component
- [ ] Create frontend Dockerfile
- [ ] Setup API client utility

### Phase 4: Frontend Features
- [ ] Build AudioRecorder component
  - [ ] Use MediaRecorder API
  - [ ] Add start/stop/pause controls
  - [ ] Show recording timer
  - [ ] Display waveform visualization (optional)
- [ ] Build FileUploader component
  - [ ] Drag-and-drop interface
  - [ ] File type validation (WAV, MP3, M4A)
  - [ ] File size validation
- [ ] Create TranscriptionViewer
  - [ ] Display transcription text
  - [ ] Show timestamp/speaker info if available
- [ ] Create SummaryViewer
  - [ ] Display formatted summary
  - [ ] Add copy-to-clipboard functionality
- [ ] Implement loading states and error handling
- [ ] Add responsive design

### Phase 5: Local Development
- [ ] Create `docker-compose.yml`
  - [ ] Backend service (port 5000)
  - [ ] Frontend service (port 3000)
  - [ ] Shared network configuration
  - [ ] Volume mounts for hot-reloading
  - [ ] Environment variable configuration
- [ ] Create `.env.example` files
- [ ] Test full workflow locally

### Phase 6: Production Deployment
- [ ] Create `render.yaml` blueprint
  - [ ] Web service for Flask backend
  - [ ] Static site or web service for Next.js
  - [ ] Environment variable definitions
  - [ ] Build commands
  - [ ] Health check endpoints
- [ ] Configure production environment variables
- [ ] Test deployment on Render

### Phase 7: Documentation
- [ ] Create comprehensive README.md
  - [ ] Project description
  - [ ] Prerequisites
  - [ ] Local setup instructions
  - [ ] API documentation
  - [ ] Deployment guide
  - [ ] Environment variables reference
- [ ] Add code comments and docstrings
- [ ] Create API examples/screenshots

---

## Key Implementation Details

### Audio Recording
- Use Web Audio API's `MediaRecorder` interface
- Support multiple audio formats (WAV, MP3, M4A)
- Handle browser permissions gracefully
- Add visual feedback during recording

### AssemblyAI Integration
- Upload audio file to AssemblyAI
- Use polling or webhooks for transcription status
- Handle transcription errors and retries
- Optional: Support speaker diarization

### OpenAI Summarization
- Use GPT-4 or GPT-3.5-turbo for summarization
- Craft effective prompt:
  ```
  Summarize the following meeting transcription. 
  Include key discussion points, decisions made, and action items.
  
  Transcription:
  {transcription_text}
  ```
- Handle token limits for long transcriptions

### Error Handling
- Frontend: Display user-friendly error messages
- Backend: Log errors and return appropriate HTTP status codes
- Handle API rate limits and quota issues
- Validate file types and sizes

### Security Considerations
- Validate uploaded file types
- Set maximum file size limits
- Sanitize user inputs
- Use environment variables for API keys
- Add rate limiting (optional for demo)

---

## Development Workflow

### Local Development Commands

**Backend (with uv):**
```bash
cd backend
uv venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
uv pip install -r pyproject.toml
flask run
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Docker Compose:**
```bash
docker-compose up --build
```

### Environment Variables

**Backend (.env):**
```
ASSEMBLYAI_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
FLASK_ENV=development
FLASK_APP=app.py
```

**Frontend (.env.local):**
```
NEXT_PUBLIC_API_URL=http://localhost:5000
```

---

## Success Criteria

- [ ] User can record audio in browser
- [ ] User can upload audio files (multiple formats)
- [ ] Audio is transcribed accurately using AssemblyAI
- [ ] Transcription is summarized with key points using OpenAI
- [ ] Results are displayed in clean, readable format
- [ ] App runs locally via Docker Compose
- [ ] App deploys successfully to Render
- [ ] Comprehensive documentation is provided

---

## Future Enhancements (Optional)
- Real-time transcription during recording
- Speaker identification and labeling
- Export notes to PDF/Markdown
- Save meeting notes to database
- User authentication
- Meeting history/archive
- Multi-language support
- Transcription editing interface

---

## File Structure

```
render-meeting-notes-agent/
├── backend/
│   ├── app.py                  # Flask application
│   ├── pyproject.toml          # uv dependencies
│   ├── .env.example
│   ├── Dockerfile
│   └── services/
│       ├── assemblyai_service.py
│       └── openai_service.py
├── frontend/
│   ├── app/
│   │   ├── page.tsx
│   │   ├── layout.tsx
│   │   └── components/
│   ├── lib/
│   ├── public/
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── next.config.js
│   ├── .env.local.example
│   └── Dockerfile
├── docker-compose.yml
├── render.yaml
├── PLAN.md
└── README.md
```

---

## Timeline Estimate

- **Phase 1-2 (Backend):** 2-3 hours
- **Phase 3-4 (Frontend):** 3-4 hours
- **Phase 5 (Local Dev):** 1 hour
- **Phase 6 (Deployment):** 1-2 hours
- **Phase 7 (Documentation):** 1 hour

**Total:** 8-11 hours

---

## Notes

- This is a demo/example application for the Render AI Agent library
- Focus on clean, readable code that serves as a good example
- Prioritize functionality over advanced features
- Ensure good error handling and user feedback
- Make deployment process as simple as possible

