'use client';

import { useState } from 'react';
import { AudioRecorder } from '@/components/AudioRecorder';
import { ResultsViewer } from '@/components/ResultsViewer';
import { api } from '@/lib/api';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { AlertCircle } from 'lucide-react';

export default function Home() {
  const [transcription, setTranscription] = useState<string>('');
  const [summary, setSummary] = useState<string>('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [isTranscribing, setIsTranscribing] = useState(false);
  const [isSummarizing, setIsSummarizing] = useState(false);
  const [error, setError] = useState<string>('');

  const handleRecordingComplete = async (audioBlob: Blob) => {
    setIsProcessing(true);
    setIsTranscribing(true);
    setError('');
    setTranscription('');
    setSummary('');

    try {
      // Step 1: Transcribe the audio
      const transcribeResponse = await api.transcribe(audioBlob);
      
      if (transcribeResponse.status === 'error') {
        throw new Error(transcribeResponse.error || 'Transcription failed');
      }

      // Poll for transcription completion if needed
      let finalTranscription = transcribeResponse;
      if (transcribeResponse.status === 'processing') {
        // Poll every 2 seconds until complete
        while (finalTranscription.status === 'processing') {
          await new Promise(resolve => setTimeout(resolve, 2000));
          finalTranscription = await api.getTranscription(transcribeResponse.id);
        }
      }

      if (finalTranscription.status === 'error') {
        throw new Error(finalTranscription.error || 'Transcription failed');
      }

      setTranscription(finalTranscription.text || '');
      setIsTranscribing(false);

      // Step 2: Generate summary
      setIsSummarizing(true);
      const summaryResponse = await api.summarize(transcribeResponse.id);
      setSummary(summaryResponse.summary);
      setIsSummarizing(false);
    } catch (err) {
      console.error('Processing error:', err);
      setError(err instanceof Error ? err.message : 'An error occurred during processing');
      setIsTranscribing(false);
      setIsSummarizing(false);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-8">
      {/* Hero Section */}
      <div className="text-center space-y-4 py-8">
        <h2 className="text-4xl font-bold tracking-tight">
          Transform audio into insights
        </h2>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Record your notes and get instant AI-powered transcriptions and summaries.
          Never miss an important detail again.
        </p>
      </div>

      {/* Error Alert */}
      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Audio Recorder */}
      <div className="grid gap-8 lg:grid-cols-1">
        <AudioRecorder
          onRecordingComplete={handleRecordingComplete}
          isProcessing={isProcessing}
        />
      </div>

      {/* Results */}
      {(isTranscribing || isSummarizing || transcription || summary) && (
        <ResultsViewer
          transcription={transcription}
          summary={summary}
          isTranscribing={isTranscribing}
          isSummarizing={isSummarizing}
        />
      )}

      {/* Features */}
      {!isProcessing && !transcription && (
        <div className="grid gap-6 md:grid-cols-3 py-8">
          <div className="space-y-2 text-center">
            <div className="mx-auto h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={1.5}
                stroke="currentColor"
                className="w-6 h-6 text-primary"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M12 18.75a6 6 0 006-6v-1.5m-6 7.5a6 6 0 01-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 01-3-3V4.5a3 3 0 116 0v8.25a3 3 0 01-3 3z"
                />
              </svg>
            </div>
            <h3 className="font-semibold">Easy Recording</h3>
            <p className="text-sm text-muted-foreground">
              One-click recording directly in your browser. No downloads required.
            </p>
          </div>

          <div className="space-y-2 text-center">
            <div className="mx-auto h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={1.5}
                stroke="currentColor"
                className="w-6 h-6 text-primary"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z"
                />
              </svg>
            </div>
            <h3 className="font-semibold">Lightning Fast</h3>
            <p className="text-sm text-muted-foreground">
              Powered by AssemblyAI for accurate, real-time transcription.
            </p>
          </div>

          <div className="space-y-2 text-center">
            <div className="mx-auto h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={1.5}
                stroke="currentColor"
                className="w-6 h-6 text-primary"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 22l-.394-1.433a2.25 2.25 0 00-1.423-1.423L13.5 19l1.183-.394a2.25 2.25 0 001.423-1.423L16.5 16l.394 1.183a2.25 2.25 0 001.423 1.423L19.5 19l-1.183.394a2.25 2.25 0 00-1.423 1.423z"
                />
              </svg>
            </div>
            <h3 className="font-semibold">AI Summaries</h3>
            <p className="text-sm text-muted-foreground">
              Get key insights, decisions, and action items with OpenAI.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
