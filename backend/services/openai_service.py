"""
OpenAI Service
Handles summarization using OpenAI GPT API
"""

import os
from openai import OpenAI


class OpenAIService:
    """Service for generating summaries using OpenAI"""
    
    def __init__(self):
        """Initialize OpenAI service with API key"""
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
    
    def summarize_transcription(self, transcription_text: str) -> str:
        """
        Generate a summary of audio transcription
        
        Args:
            transcription_text: The full transcription text
        
        Returns:
            str: The generated summary
        """
        try:
            # Create the prompt
            system_prompt = """You are an expert at summarizing audio notes and transcriptions. 
Your task is to create clear, concise summaries that capture the essential information from any type of audio content.

Analyze the content and provide a structured summary with these sections (adapt based on content type):

**Main Topics/Themes:** 
Brief overview of the primary subjects covered

**Key Points:** 
Important information, facts, insights, or ideas mentioned

**Action Items/Next Steps:** 
Any tasks, to-dos, reminders, or follow-ups identified (if applicable)

**Notable Details:**
Specific examples, quotes, references, or important details worth highlighting

Adapt your summary to the content type - whether it's a meeting, lecture, voice memo, brainstorming session, interview, or general notes. Keep it well-organized, easy to scan, and actionable."""

            user_prompt = f"""Please analyze and summarize the following audio transcription:

{transcription_text}"""

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.75,
                max_tokens=1500
            )
            
            summary = response.choices[0].message.content.strip()
            return summary
        
        except Exception as e:
            print(f"OpenAI summarization error: {str(e)}")
            raise Exception(f"Failed to generate summary: {str(e)}")
    
    def extract_action_items(self, transcription_text: str) -> list:
        """
        Extract action items from transcription
        
        Args:
            transcription_text: The full transcription text
        
        Returns:
            list: List of action items
        """
        try:
            prompt = f"""Extract all actionable tasks, to-dos, reminders, or follow-ups from the following transcription.
This could include things to research, people to contact, tasks to complete, or ideas to pursue.
Return only the action items as a bullet-point list.

Transcription:
{transcription_text}"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=750
            )
            
            action_items_text = response.choices[0].message.content.strip()
            # Split into list
            action_items = [
                item.strip('- ').strip()
                for item in action_items_text.split('\n')
                if item.strip() and item.strip().startswith('-')
            ]
            
            return action_items
        
        except Exception as e:
            print(f"OpenAI action items extraction error: {str(e)}")
            return []

