# Note Taker AI 🎙️

An AI-powered note-taking application that transcribes and summarizes audio recordings using AssemblyAI and OpenAI. Built as an example application for the Render AI Agent example library.

## 🚀 New? Start Here!

**Want to run this locally in 5 minutes?** → **[QUICKSTART.md](./QUICKSTART.md)**

The quickstart guide walks you through getting everything running with Docker Compose in just a few commands!

---

## Table of Contents

- [Deploy to Render](#-deploy-to-render)
- [Features](#-features)
- [Repository Structure](#-repository-structure)
- [Quick Start with Docker](#-quick-start-with-docker)
- [Docker Commands](#-docker-commands)
- [Troubleshooting](#-troubleshooting)
- [Additional Documentation](#-additional-documentation)
- [Contributing](#-contributing)
- [License](#-license)

## 🚀 Deploy to Render

This project is pre-configured for one-click deployment to [Render](https://render.com/) using the included `render.yaml` blueprint.

**What you get:**
- ✅ Next.js frontend with browser-based audio recording
- ✅ Flask backend with AssemblyAI and OpenAI integration
- ✅ Separate frontend and backend services
- ✅ Auto-scaling and health checks
- ✅ Environment variable management

**Deployment steps:**

1. **Fork this repository to your GitHub account**

2. **Create a new Blueprint Instance on Render:**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Blueprint Instance"
   - Connect your forked repository
   - Select branch (usually `main`)

3. **Configure environment variables:**
   - Render will auto-detect `render.yaml`
   - You'll be prompted to enter:
     - `ASSEMBLYAI_API_KEY` ([Get one here](https://www.assemblyai.com/))
     - `OPENAI_API_KEY` ([Get one here](https://platform.openai.com/))
   - Optional: `OPENAI_MODEL` (defaults to `gpt-4o-mini`)

4. **Deploy:**
   - Click "Apply" to create all services
   - Render will:
     - Build and deploy Flask backend
     - Build and deploy Next.js frontend
     - Link services together

5. **Configure the Frontend API URL:**
   - After deployment, copy your backend URL (e.g., `https://note-taker-backend.onrender.com`)
   - Go to your frontend service in the Render Dashboard
   - Navigate to "Environment" tab
   - Set `NEXT_PUBLIC_API_URL` to your backend URL
   - The frontend will automatically redeploy with the correct API endpoint

6. **Access your deployed app:**
   - Frontend: `https://your-app-name-frontend.onrender.com`
   - Backend API: `https://your-app-name-backend.onrender.com`

**Cost Estimate (Render Free Tier):**
- 2 Web Services (frontend + backend): Free
- AssemblyAI API: Pay-per-use (~$0.05 per audio hour)
- OpenAI API: Pay-per-use (~$0.01-0.05 per summary)
- Total: ~$0/month recurring (free tier) + usage-based API costs

## ✨ Features

- 🎤 **Browser-based audio recording** - Record directly in your browser, no downloads needed
- ⚡ **Lightning-fast transcription** - Powered by AssemblyAI for accurate speech-to-text
- 🤖 **AI-powered summaries** - Get key insights, important points, and action items with OpenAI
- 🎨 **Beautiful UI** - Inspired by Render.com's clean, modern design
- 🐳 **Docker-ready** - Easy deployment with Docker Compose
- ☁️ **Render-optimized** - Deploy to production with a single blueprint file

## 📁 Repository Structure

```
.
├── backend/               # Flask + Python API (transcription + summarization)
│   ├── app.py             # Flask application
│   ├── pyproject.toml     # uv dependencies
│   ├── services/          # AssemblyAI and OpenAI integrations
│   │   ├── assemblyai_service.py
│   │   └── openai_service.py
│   ├── Dockerfile         # Backend container
│   └── ...
├── frontend/              # Next.js app (audio recorder + results viewer)
│   ├── app/
│   │   ├── page.tsx       # Main page
│   │   ├── layout.tsx     # App layout
│   │   └── globals.css    # Global styles
│   ├── components/
│   │   ├── AudioRecorder.tsx  # Audio recording component
│   │   └── ResultsViewer.tsx  # Results display
│   ├── lib/
│   │   └── api.ts         # API client
│   ├── Dockerfile         # Nginx-served production build
│   └── next.config.ts     # Next.js configuration
├── docker-compose.yml     # Full-stack local development
├── render.yaml            # Production deployment configuration (Render.com)
├── QUICKSTART.md          # Quick start guide
└── README.md
```

## 🚀 Quick Start with Docker

**For detailed step-by-step instructions, see [QUICKSTART.md](./QUICKSTART.md)**

**TL;DR:**

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd render-meeting-notes-agent

# 2. Create .env file with your API keys
cat > .env << 'EOF'
ASSEMBLYAI_API_KEY=your-key-here
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o-mini
BACKEND_PORT=3100
FRONTEND_PORT=3000
EOF

# 3. Start everything
docker compose up -d

# 4. Open http://localhost:3000
```

This starts:
- ✅ Flask backend API (port 3100)
- ✅ Next.js frontend UI (port 3000)
- ✅ Browser-based audio recording ready to use

## 📦 Docker Commands

**Start all services:**
```bash
docker compose up -d
```

**Stop all services:**
```bash
docker compose down
```

**View logs:**
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend
```

**Rebuild after code changes:**
```bash
docker compose up -d --build
```

## 🐛 Troubleshooting

**1. Docker port conflicts:**
```bash
# Check what's using the port
lsof -i :3100  # or :3000

# Change ports in .env file or docker-compose.yml
```

**2. Backend connection errors:**
```bash
# Ensure backend is running
docker compose ps

# Check backend logs
docker compose logs backend
```

**3. AssemblyAI API errors:**
- Verify your API key is valid at https://www.assemblyai.com/
- Check your AssemblyAI account has credits
- Ensure API key is properly set in `.env` or environment variables

**4. OpenAI API errors:**
- Verify your API key is valid at https://platform.openai.com/api-keys
- Check your OpenAI account has credits
- Ensure correct model name in configuration (e.g., `gpt-4o-mini`)

**5. Frontend can't reach backend:**
- For local dev: Frontend should connect to `http://localhost:3100`
- For Docker: Check `NEXT_PUBLIC_API_URL` in `docker-compose.yml` build args
- For Render: Services are auto-linked via `render.yaml`

**Getting more help:**
1. Check service logs: `docker compose logs <service-name>`
2. Verify all environment variables are set correctly
3. Ensure Docker containers are healthy: `docker compose ps`
4. See detailed troubleshooting in `backend/README.md`

## 📚 Additional Documentation

- **[QUICKSTART.md](./QUICKSTART.md)** - 🚀 Get started in 5 minutes with Docker Compose
- `backend/README.md` - Backend API documentation
- `frontend/README.md` - Frontend component documentation

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT

