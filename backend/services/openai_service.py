"""
OpenAI Service
Handles summarization using OpenAI GPT API with intelligent chunking
"""

import os
import re
from typing import List
from openai import OpenAI


class OpenAIService:
    """Service for generating summaries using OpenAI with intelligent chunking"""
    
    # Token limits per model (conservative estimates for input + output)
    MODEL_LIMITS = {
        'gpt-4o-mini': 120000,      # 128k context
        'gpt-4o': 120000,           # 128k context
        'gpt-4-turbo': 120000,      # 128k context
        'gpt-4': 7000,              # 8k context
        'gpt-3.5-turbo': 15000,     # 16k context
    }
    
    # Max tokens per chunk (leave room for prompt and response)
    CHUNK_SIZE = 12000  # ~3000 words per chunk
    
    def __init__(self):
        """Initialize OpenAI service with API key"""
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        self.context_limit = self.MODEL_LIMITS.get(self.model, 7000)
    
    def estimate_tokens(self, text: str) -> int:
        """
        Rough estimate of token count (1 token ≈ 4 characters for English)
        This is a conservative estimate; actual tokenization may differ
        """
        return len(text) // 4
    
    def chunk_text(self, text: str, max_tokens: int = None) -> List[str]:
        """
        Split text into chunks that fit within token limits.
        Tries to split on paragraph boundaries, then sentences.
        
        Args:
            text: Text to chunk
            max_tokens: Maximum tokens per chunk (defaults to CHUNK_SIZE)
        
        Returns:
            List of text chunks
        """
        if max_tokens is None:
            max_tokens = self.CHUNK_SIZE
        
        # If text is small enough, return as single chunk
        if self.estimate_tokens(text) <= max_tokens:
            return [text]
        
        chunks = []
        
        # Split by paragraphs (double newline)
        paragraphs = re.split(r'\n\s*\n', text)
        
        current_chunk = ""
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            
            # Check if adding this paragraph would exceed limit
            test_chunk = current_chunk + "\n\n" + paragraph if current_chunk else paragraph
            
            if self.estimate_tokens(test_chunk) <= max_tokens:
                current_chunk = test_chunk
            else:
                # If current chunk has content, save it
                if current_chunk:
                    chunks.append(current_chunk)
                    current_chunk = ""
                
                # If single paragraph is too large, split by sentences
                if self.estimate_tokens(paragraph) > max_tokens:
                    sentences = re.split(r'(?<=[.!?])\s+', paragraph)
                    for sentence in sentences:
                        test_chunk = current_chunk + " " + sentence if current_chunk else sentence
                        if self.estimate_tokens(test_chunk) <= max_tokens:
                            current_chunk = test_chunk
                        else:
                            if current_chunk:
                                chunks.append(current_chunk)
                            current_chunk = sentence
                else:
                    current_chunk = paragraph
        
        # Add remaining chunk
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks if chunks else [text]  # Fallback to original text
    
    def summarize_transcription(self, transcription_text: str) -> str:
        """
        Generate a summary of audio transcription with intelligent chunking.
        Uses map-reduce approach for long transcriptions:
        1. Split into chunks if needed
        2. Summarize each chunk
        3. Combine chunk summaries into final summary
        
        Args:
            transcription_text: The full transcription text
        
        Returns:
            str: The generated summary
        """
        try:
            # Estimate if we need chunking
            estimated_tokens = self.estimate_tokens(transcription_text)
            
            # If small enough, process normally
            if estimated_tokens <= self.CHUNK_SIZE:
                return self._summarize_single(transcription_text)
            
            # For large transcriptions, use map-reduce approach
            print(f"Long transcription detected (~{estimated_tokens} tokens). Using chunking...")
            
            # Step 1: Split into chunks
            chunks = self.chunk_text(transcription_text)
            print(f"Split into {len(chunks)} chunks")
            
            # Step 2: Summarize each chunk
            chunk_summaries = []
            for i, chunk in enumerate(chunks, 1):
                print(f"Processing chunk {i}/{len(chunks)}...")
                summary = self._summarize_chunk(chunk, i, len(chunks))
                chunk_summaries.append(summary)
            
            # Step 3: Combine summaries
            if len(chunk_summaries) == 1:
                return chunk_summaries[0]
            
            print("Combining chunk summaries...")
            return self._combine_summaries(chunk_summaries)
        
        except Exception as e:
            print(f"OpenAI summarization error: {str(e)}")
            raise Exception(f"Failed to generate summary: {str(e)}")
    
    def _summarize_single(self, text: str) -> str:
        """Summarize a single piece of text that fits within context"""
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

{text}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.75,
            max_tokens=1500
        )
        
        return response.choices[0].message.content.strip()
    
    def _summarize_chunk(self, chunk: str, chunk_num: int, total_chunks: int) -> str:
        """Summarize a single chunk of a larger transcription"""
        system_prompt = """You are summarizing part of a longer audio transcription. 
Focus on extracting the key information from this segment. Be comprehensive but concise.
Capture main topics, important points, decisions, action items, and notable details."""

        user_prompt = f"""This is part {chunk_num} of {total_chunks} from a longer transcription.
Please summarize the key information from this segment:

{chunk}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        
        return response.choices[0].message.content.strip()
    
    def _combine_summaries(self, summaries: List[str]) -> str:
        """Combine multiple chunk summaries into a cohesive final summary"""
        combined_text = "\n\n---\n\n".join(
            [f"**Section {i}:**\n{summary}" for i, summary in enumerate(summaries, 1)]
        )
        
        system_prompt = """You are combining multiple summaries from different parts of a long audio transcription.
Create a unified, well-structured summary that:
1. Eliminates redundancy
2. Groups related topics together
3. Maintains the same format with sections: Main Topics/Themes, Key Points, Action Items/Next Steps, Notable Details
4. Presents a cohesive narrative of the entire transcription

Be comprehensive but concise."""

        user_prompt = f"""Here are summaries from different sections of a long transcription. 
Please combine them into one cohesive, well-organized summary:

{combined_text}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.75,
            max_tokens=2000
        )
        
        return response.choices[0].message.content.strip()
    
    def extract_action_items(self, transcription_text: str) -> list:
        """
        Extract action items from transcription with chunking support
        
        Args:
            transcription_text: The full transcription text
        
        Returns:
            list: List of action items
        """
        try:
            estimated_tokens = self.estimate_tokens(transcription_text)
            
            # If small enough, process normally
            if estimated_tokens <= self.CHUNK_SIZE:
                return self._extract_action_items_single(transcription_text)
            
            # For large transcriptions, process chunks and combine
            print(f"Long transcription detected for action items. Using chunking...")
            chunks = self.chunk_text(transcription_text)
            
            all_action_items = []
            for i, chunk in enumerate(chunks, 1):
                print(f"Extracting action items from chunk {i}/{len(chunks)}...")
                items = self._extract_action_items_single(chunk)
                all_action_items.extend(items)
            
            # Deduplicate similar action items
            return self._deduplicate_action_items(all_action_items)
        
        except Exception as e:
            print(f"OpenAI action items extraction error: {str(e)}")
            return []
    
    def _extract_action_items_single(self, text: str) -> list:
        """Extract action items from a single text chunk"""
        prompt = f"""Extract all actionable tasks, to-dos, reminders, or follow-ups from the following transcription.
This could include things to research, people to contact, tasks to complete, or ideas to pursue.
Return only the action items as a bullet-point list.

Transcription:
{text}"""

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
            if item.strip() and (item.strip().startswith('-') or item.strip().startswith('•'))
        ]
        
        return action_items
    
    def _deduplicate_action_items(self, items: List[str]) -> list:
        """Remove duplicate or very similar action items"""
        if not items:
            return []
        
        # Simple deduplication by exact match and case-insensitive match
        seen = set()
        unique_items = []
        
        for item in items:
            item_lower = item.lower().strip()
            if item_lower not in seen:
                seen.add(item_lower)
                unique_items.append(item)
        
        return unique_items

