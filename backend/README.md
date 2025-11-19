# Note Taker Backend

Flask API for transcribing and summarizing audio notes using AssemblyAI and OpenAI.

## Setup

### Install uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Install Dependencies

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r pyproject.toml
```

### Configure Environment

```bash
cp .env.example .env
# Edit .env and add your API keys:
# - ASSEMBLYAI_API_KEY
# - OPENAI_API_KEY
```

### Run Development Server

```bash
python app.py
```

Server will start on `http://localhost:3100`

### Run Production Server

```bash
gunicorn --bind 0.0.0.0:3100 --workers 4 --timeout 120 app:app
```

## API Endpoints

- `GET /health` - Health check
- `POST /api/transcribe` - Upload audio for transcription
- `GET /api/transcription/:id` - Get transcription status
- `POST /api/summarize/:id` - Generate summary
- `GET /api/notes/:id` - Get complete notes (transcription + summary)

See main README for full API documentation.

## Project Structure

```
backend/
├── app.py                      # Main Flask application
├── pyproject.toml              # Dependencies (uv)
├── Dockerfile                  # Production container
├── .env.example                # Environment template
└── services/
    ├── assemblyai_service.py   # AssemblyAI integration
    └── openai_service.py       # OpenAI integration
```

## Technologies

- **Flask 3.0** - Web framework
- **uv** - Fast Python package manager
- **AssemblyAI** - Speech-to-text
- **OpenAI** - AI summarization
- **Gunicorn** - Production WSGI server

