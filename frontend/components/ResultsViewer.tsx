'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { FileText, Sparkles, AlertCircle, Copy, Check } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useState } from 'react';

interface ResultsViewerProps {
  transcription?: string;
  summary?: string;
  isTranscribing?: boolean;
  isSummarizing?: boolean;
  error?: string;
}

export function ResultsViewer({
  transcription,
  summary,
  isTranscribing = false,
  isSummarizing = false,
  error,
}: ResultsViewerProps) {
  const [copiedTranscription, setCopiedTranscription] = useState(false);
  const [copiedSummary, setCopiedSummary] = useState(false);

  const copyToClipboard = async (text: string, type: 'transcription' | 'summary') => {
    try {
      await navigator.clipboard.writeText(text);
      if (type === 'transcription') {
        setCopiedTranscription(true);
        setTimeout(() => setCopiedTranscription(false), 2000);
      } else {
        setCopiedSummary(true);
        setTimeout(() => setCopiedSummary(false), 2000);
      }
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertCircle className="h-4 w-4" />
        <AlertDescription>{error}</AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="space-y-6">
      {/* Transcription Section */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <FileText className="h-5 w-5 text-primary" />
              <CardTitle>Transcription</CardTitle>
            </div>
            {isTranscribing && (
              <Badge variant="outline" className="animate-pulse">
                Processing...
              </Badge>
            )}
            {transcription && !isTranscribing && (
              <Button
                variant="ghost"
                size="sm"
                onClick={() => copyToClipboard(transcription, 'transcription')}
              >
                {copiedTranscription ? (
                  <>
                    <Check className="h-4 w-4 mr-2" />
                    Copied!
                  </>
                ) : (
                  <>
                    <Copy className="h-4 w-4 mr-2" />
                    Copy
                  </>
                )}
              </Button>
            )}
          </div>
          <CardDescription>
            Full text transcription of your meeting audio
          </CardDescription>
        </CardHeader>
        <CardContent>
          {isTranscribing ? (
            <div className="space-y-2">
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-3/4" />
            </div>
          ) : transcription ? (
            <div className="prose prose-sm max-w-none">
              <p className="whitespace-pre-wrap text-foreground leading-relaxed">
                {transcription}
              </p>
            </div>
          ) : (
            <p className="text-muted-foreground text-sm">
              Transcription will appear here once processing is complete
            </p>
          )}
        </CardContent>
      </Card>

      {/* Summary Section */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Sparkles className="h-5 w-5 text-primary" />
              <CardTitle>AI Summary</CardTitle>
            </div>
            {isSummarizing && (
              <Badge variant="outline" className="animate-pulse">
                Generating...
              </Badge>
            )}
            {summary && !isSummarizing && (
              <Button
                variant="ghost"
                size="sm"
                onClick={() => copyToClipboard(summary, 'summary')}
              >
                {copiedSummary ? (
                  <>
                    <Check className="h-4 w-4 mr-2" />
                    Copied!
                  </>
                ) : (
                  <>
                    <Copy className="h-4 w-4 mr-2" />
                    Copy
                  </>
                )}
              </Button>
            )}
          </div>
          <CardDescription>
            Key points, decisions, and action items extracted by AI
          </CardDescription>
        </CardHeader>
        <CardContent>
          {isSummarizing ? (
            <div className="space-y-2">
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-2/3" />
            </div>
          ) : summary ? (
            <div className="prose prose-sm max-w-none">
              <p className="whitespace-pre-wrap text-foreground leading-relaxed">
                {summary}
              </p>
            </div>
          ) : (
            <p className="text-muted-foreground text-sm">
              AI-generated summary will appear here after transcription completes
            </p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

