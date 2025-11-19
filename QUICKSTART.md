# 🚀 Quickstart Guide

Get Note Taker AI running locally in under 5 minutes using Docker Compose!

## Prerequisites

- **Docker Desktop** installed ([Download here](https://www.docker.com/products/docker-desktop))
- **AssemblyAI API key** ([Get free key here](https://www.assemblyai.com/))
- **OpenAI API key** ([Get one here](https://platform.openai.com/api-keys))

That's it! Docker handles everything else (Python, Flask, Node.js, etc.)

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd render-meeting-notes-agent
```

### 2. Create Environment File

Create a file named `.env` in the root directory:

```bash
# Copy this template and fill in your API keys
cat > .env << 'EOF'
# Required: Your AssemblyAI API key
ASSEMBLYAI_API_KEY=your-assemblyai-key-here

# Required: Your OpenAI API key
OPENAI_API_KEY=sk-your-openai-key-here

# Optional: OpenAI model (defaults to gpt-4o-mini)
OPENAI_MODEL=gpt-4o-mini

# Optional: Port configuration
BACKEND_PORT=3100
FRONTEND_PORT=3000
EOF
```

**Important:** Replace the placeholder values with your real API keys!

### 3. Start Everything

```bash
docker compose up -d
```

This single command will:
- ✅ Build and start the Flask backend API
- ✅ Build and start the Next.js frontend
- ✅ Connect both services together

**First-time setup takes 2-3 minutes** to build Docker images. Subsequent starts are instant!

### 4. Open the App

Once the containers are running, open your browser to:

**http://localhost:3000**

You should see the Note Taker AI interface with a microphone button ready to record!

## 🎉 You're Done!

That's it! You now have a fully functional AI note-taking app with:
- Browser-based audio recording
- AssemblyAI transcription
- OpenAI-powered summarization
- Beautiful, modern UI

## How to Use

1. **Click the microphone button** to start recording
2. **Speak** your notes, meeting content, or ideas
3. **Click the square button** to stop recording
4. **Click "Transcribe & Summarize"** to process the audio
5. **View results** - get accurate transcription and AI-generated summary with key insights

## Useful Commands

### View logs
```bash
# All services
docker compose logs -f

# Just backend
docker compose logs -f backend

# Just frontend
docker compose logs -f frontend
```

### Stop everything
```bash
docker compose down
```

### Restart everything
```bash
docker compose restart
```

### Rebuild after code changes
```bash
docker compose up -d --build
```

## What's Running?

| Service | Port | Purpose |
|---------|------|---------|
| Frontend | http://localhost:3000 | Next.js chat UI with audio recorder |
| Backend API | http://localhost:3100 | Flask API with AssemblyAI & OpenAI |

## Verify It's Working

### 1. Check all services are running:
```bash
docker compose ps
```

You should see both services with status "Up".

### 2. Check backend health:
```bash
curl http://localhost:3100/health
```

Should return:
```json
{
  "status": "healthy",
  "service": "note-taker-backend"
}
```

### 3. Test in browser:
- Open http://localhost:3000
- You should see the Note Taker AI interface
- Click the microphone icon - you should see it turn red when recording

## Troubleshooting

### Port already in use?

If you see errors about ports 3000 or 3100 already being used:

```bash
# Find what's using the ports
lsof -i :3000
lsof -i :3100

# Change ports in .env file
BACKEND_PORT=8080
FRONTEND_PORT=8000

# Then restart
docker compose down && docker compose up -d
```

### API Key Errors?

1. Verify your API keys are correct in `.env`
2. **AssemblyAI**: Check your account at https://www.assemblyai.com/app
3. **OpenAI**: Check your account has credits at https://platform.openai.com/account/billing
4. Make sure you didn't include quotes around the API keys

### Microphone not working?

- **Browser permission**: Allow microphone access when prompted
- **HTTPS required**: Production deployments need HTTPS for microphone access
- **Browser compatibility**: Use Chrome, Firefox, or Safari (Edge may have issues)

### Frontend can't reach backend?

Check the backend URL configuration:
```bash
# For local development, frontend expects backend at http://localhost:3100
# If you changed BACKEND_PORT, update docker-compose.yml accordingly
```

### Fresh start?

To completely reset everything and start from scratch:

```bash
# WARNING: This deletes all data!
docker compose down -v
docker compose up -d --build
```

## Cost Considerations

### API Usage

- **AssemblyAI**: ~$0.05 per audio hour (~$0.001 per minute)
- **OpenAI summarization**: ~$0.01-0.05 per summary (depends on length)

**Example costs:**
- 5-minute meeting: ~$0.01-0.06 total
- 30-minute meeting: ~$0.03-0.10 total
- 1-hour meeting: ~$0.06-0.15 total

**Tip:** Start with short recordings to test before processing longer meetings.

## What's Next?

### Customize the Prompt

Edit `backend/services/openai_service.py` to change how summaries are generated.

### Add Features

- Export summaries to PDF
- Email summaries automatically
- Integrate with calendar
- Add speaker diarization (AssemblyAI feature)

### Deploy to Production

See the main [README.md](./README.md) for deployment options:
- **Render.com**: One-click deployment (recommended)
- **Any Docker host**: Use the included Dockerfiles
- **Vercel + Render**: Deploy frontend to Vercel, backend to Render

## Need Help?

- **Backend API**: See `backend/README.md`
- **Frontend Details**: See `frontend/README.md`
- **Main Documentation**: See [README.md](./README.md)
- **Project Plan**: See [PLAN.md](./PLAN.md)

## Common Questions

**Q: Can I use a different transcription service?**
A: Currently only AssemblyAI is supported. Adding support for Whisper or other services would require code changes in `backend/services/`.

**Q: Can I use a different LLM provider?**
A: Yes! You can modify `backend/services/openai_service.py` to use Anthropic, Cohere, or other providers.

**Q: How long can my recordings be?**
A: There's no hard limit, but longer recordings take more time to transcribe and cost more. Most meetings under 2 hours work well.

**Q: Are my recordings stored?**
A: Audio files are temporarily stored in `backend/uploads/` and can be automatically cleaned up. See `backend/app.py` for cleanup configuration.

**Q: Is my API key secure?**
A: API keys are only stored in your local `.env` file and used by the backend container. Never commit this file to Git!

**Q: How do I update the code?**
A: Pull the latest changes and rebuild:
```bash
git pull
docker compose up -d --build
```

---

**That's it!** You now have a production-ready AI note-taking app running locally. Start recording and get instant transcriptions! 🎙️

