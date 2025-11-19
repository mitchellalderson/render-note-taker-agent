"""
AssemblyAI Service
Handles audio transcription using AssemblyAI API
"""

import os
import time
import assemblyai as aai


class AssemblyAIService:
    """Service for transcribing audio files using AssemblyAI"""
    
    def __init__(self):
        """Initialize AssemblyAI service with API key"""
        self.api_key = os.getenv('ASSEMBLYAI_API_KEY')
        if not self.api_key:
            raise ValueError("ASSEMBLYAI_API_KEY environment variable not set")
        
        aai.settings.api_key = self.api_key
        self.transcriber = aai.Transcriber()
    
    def transcribe_audio(self, audio_file_path: str, wait_for_completion: bool = True) -> dict:
        """
        Transcribe an audio file
        
        Args:
            audio_file_path: Path to the audio file
            wait_for_completion: Whether to wait for transcription to complete
        
        Returns:
            dict with keys: status ('completed', 'processing', 'error'), text, error
        """
        try:
            # Start transcription
            transcript = self.transcriber.transcribe(audio_file_path)
            
            if wait_for_completion:
                # Wait for completion
                while transcript.status not in [
                    aai.TranscriptStatus.completed,
                    aai.TranscriptStatus.error
                ]:
                    time.sleep(1)
                    transcript = self.transcriber.get_transcript(transcript.id)
                
                if transcript.status == aai.TranscriptStatus.error:
                    return {
                        'status': 'error',
                        'error': transcript.error or 'Transcription failed'
                    }
                
                return {
                    'status': 'completed',
                    'text': transcript.text
                }
            else:
                # Return immediately with processing status
                return {
                    'status': 'processing',
                    'transcript_id': transcript.id
                }
        
        except Exception as e:
            print(f"AssemblyAI transcription error: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def get_transcript(self, transcript_id: str) -> dict:
        """
        Get the status and result of a transcription
        
        Args:
            transcript_id: The transcript ID from AssemblyAI
        
        Returns:
            dict with keys: status, text, error
        """
        try:
            transcript = aai.Transcript.get_by_id(transcript_id)
            
            if transcript.status == aai.TranscriptStatus.completed:
                return {
                    'status': 'completed',
                    'text': transcript.text
                }
            elif transcript.status == aai.TranscriptStatus.error:
                return {
                    'status': 'error',
                    'error': transcript.error or 'Transcription failed'
                }
            else:
                return {
                    'status': 'processing'
                }
        
        except Exception as e:
            print(f"Error getting transcript: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }

