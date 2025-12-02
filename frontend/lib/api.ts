function getApiBaseUrl(): string {
  const apiHost = process.env.NEXT_PUBLIC_API_HOST;
  if (apiHost) {
    // If it's just a service name (no dots), append .onrender.com
    const fullHost = apiHost.includes(".")
      ? apiHost
      : `${apiHost}.onrender.com`;
    return `https://${fullHost}`;
  }
  // Fall back to full URL (for local development)
  return process.env.NEXT_PUBLIC_API_URL || "http://localhost:3100";
}

const API_BASE_URL = getApiBaseUrl();

export interface TranscriptionResponse {
  id: string;
  status: 'processing' | 'completed' | 'error';
  text?: string;
  error?: string;
}

export interface SummaryResponse {
  summary: string;
}

export interface NotesResponse {
  id: string;
  transcription: string;
  summary: string;
  createdAt: string;
}

export const api = {
  /**
   * Upload audio file for transcription
   */
  async transcribe(audioBlob: Blob): Promise<TranscriptionResponse> {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.webm');

    const response = await fetch(`${API_BASE_URL}/api/transcribe`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Transcription failed: ${response.statusText}`);
    }

    return response.json();
  },

  /**
   * Get transcription status and result
   */
  async getTranscription(id: string): Promise<TranscriptionResponse> {
    const response = await fetch(`${API_BASE_URL}/api/transcription/${id}`);

    if (!response.ok) {
      throw new Error(`Failed to get transcription: ${response.statusText}`);
    }

    return response.json();
  },

  /**
   * Generate summary from transcription
   */
  async summarize(id: string): Promise<SummaryResponse> {
    const response = await fetch(`${API_BASE_URL}/api/summarize/${id}`, {
      method: 'POST',
    });

    if (!response.ok) {
      throw new Error(`Summarization failed: ${response.statusText}`);
    }

    return response.json();
  },

  /**
   * Get complete meeting notes (transcription + summary)
   */
  async getNotes(id: string): Promise<NotesResponse> {
    const response = await fetch(`${API_BASE_URL}/api/notes/${id}`);

    if (!response.ok) {
      throw new Error(`Failed to get notes: ${response.statusText}`);
    }

    return response.json();
  },
};

