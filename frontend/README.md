# Note Taker Frontend

Modern Next.js frontend for recording, transcribing, and summarizing audio notes. Features a clean UI inspired by Render.com.

## Setup

### Install Dependencies

```bash
npm install
```

### Configure Environment

Create a `.env.local` file:

```bash
echo "NEXT_PUBLIC_API_URL=http://localhost:3100" > .env.local
```

For production, set `NEXT_PUBLIC_API_URL` to your backend URL.

### Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

### Production Build

```bash
npm run build
npm start
```

### Docker Build

```bash
docker build -t note-taker-frontend .
docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=http://backend:3100 note-taker-frontend
```

## Features

### Audio Recorder
- Browser-based audio recording using MediaRecorder API
- Visual recording indicator and timer
- Audio playback before submission
- Support for WebM, MP3, WAV, M4A formats

### Results Viewer
- Real-time transcription display
- AI-generated summary with key points
- Copy-to-clipboard functionality
- Loading states and error handling

### Design
- Render.com-inspired purple theme (#7B2BFF)
- Responsive layout with Tailwind CSS
- shadcn/ui components for consistency
- Smooth animations and transitions

## Project Structure

```
frontend/
├── app/
│   ├── page.tsx           # Main application page
│   ├── layout.tsx         # Root layout with header/footer
│   └── globals.css        # Global styles & theme
├── components/
│   ├── AudioRecorder.tsx  # Audio recording component
│   ├── ResultsViewer.tsx  # Transcription & summary display
│   └── ui/                # shadcn/ui components
├── lib/
│   ├── api.ts             # API client functions
│   └── utils.ts           # Utility functions
├── Dockerfile             # Production container
├── next.config.ts         # Next.js configuration
└── package.json           # Dependencies
```

## Technologies

- **Next.js 16** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first styling
- **shadcn/ui** - High-quality component library
- **Lucide Icons** - Beautiful icon set

## API Integration

The frontend communicates with the Flask backend through REST API:

```typescript
import { api } from '@/lib/api';

// Transcribe audio
const result = await api.transcribe(audioBlob);

// Get transcription
const transcription = await api.getTranscription(id);

// Generate summary
const summary = await api.summarize(id);

// Get complete notes
const notes = await api.getNotes(id);
```

## Customization

### Theme Colors

Edit `app/globals.css` to customize the color scheme:

```css
:root {
  --primary: oklch(0.5 0.3 285);  /* Purple accent */
  /* ... other colors ... */
}
```

### UI Components

All UI components are in `components/ui/` and can be customized individually.

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

**Note:** Audio recording requires microphone permissions and HTTPS in production.

## Live Demo

Record notes, get transcriptions, and AI-powered summaries in seconds!

## Performance

- Optimized with Next.js App Router
- Code splitting for faster loads
- Image optimization
- Standalone output for minimal Docker images
