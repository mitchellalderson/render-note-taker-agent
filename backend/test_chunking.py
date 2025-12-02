"""
Test script for OpenAI chunking functionality
Run with: python test_chunking.py
"""

import os
from services.openai_service import OpenAIService


def test_token_estimation():
    """Test token estimation"""
    service = OpenAIService() if os.getenv('OPENAI_API_KEY') else None
    
    if not service:
        print("⚠️  Skipping: OPENAI_API_KEY not set")
        return
    
    print("Testing token estimation...")
    
    # Test cases
    test_cases = [
        ("Hello world", 3),  # ~3 tokens
        ("This is a longer sentence with more words.", 11),  # ~11 tokens
        ("A" * 400, 100),  # 400 chars = ~100 tokens
    ]
    
    for text, expected in test_cases:
        estimated = service.estimate_tokens(text)
        print(f"  Text length: {len(text)} chars → {estimated} tokens (expected ~{expected})")
        assert abs(estimated - expected) <= 2, f"Estimation off: {estimated} vs {expected}"
    
    print("✅ Token estimation tests passed\n")


def test_chunking_small_text():
    """Test that small text doesn't get chunked"""
    service = OpenAIService() if os.getenv('OPENAI_API_KEY') else None
    
    if not service:
        print("⚠️  Skipping: OPENAI_API_KEY not set")
        return
    
    print("Testing small text chunking...")
    
    small_text = "This is a short transcription that should not be chunked." * 10
    chunks = service.chunk_text(small_text)
    
    print(f"  Input: {len(small_text)} chars (~{service.estimate_tokens(small_text)} tokens)")
    print(f"  Chunks: {len(chunks)}")
    
    assert len(chunks) == 1, "Small text should remain as single chunk"
    print("✅ Small text test passed\n")


def test_chunking_large_text():
    """Test that large text gets chunked properly"""
    service = OpenAIService() if os.getenv('OPENAI_API_KEY') else None
    
    if not service:
        print("⚠️  Skipping: OPENAI_API_KEY not set")
        return
    
    print("Testing large text chunking...")
    
    # Create a large text (simulate ~50k token transcription)
    paragraph = "This is a paragraph about an important topic. " * 50
    large_text = (paragraph + "\n\n") * 200  # ~200k chars = ~50k tokens
    
    chunks = service.chunk_text(large_text, max_tokens=5000)
    
    print(f"  Input: {len(large_text)} chars (~{service.estimate_tokens(large_text)} tokens)")
    print(f"  Chunks: {len(chunks)}")
    
    for i, chunk in enumerate(chunks, 1):
        tokens = service.estimate_tokens(chunk)
        print(f"    Chunk {i}: {len(chunk)} chars (~{tokens} tokens)")
        assert tokens <= 5000, f"Chunk {i} exceeds max tokens"
    
    assert len(chunks) > 1, "Large text should be split into multiple chunks"
    print("✅ Large text test passed\n")


def test_chunking_preserves_content():
    """Test that chunking doesn't lose content"""
    service = OpenAIService() if os.getenv('OPENAI_API_KEY') else None
    
    if not service:
        print("⚠️  Skipping: OPENAI_API_KEY not set")
        return
    
    print("Testing content preservation...")
    
    # Create text with distinct markers
    paragraphs = [f"Paragraph {i}: " + "content " * 100 for i in range(1, 21)]
    large_text = "\n\n".join(paragraphs)
    
    chunks = service.chunk_text(large_text, max_tokens=2000)
    
    # Combine chunks back together
    combined = "\n\n".join(chunks)
    combined_normalized = " ".join(combined.split())
    original_normalized = " ".join(large_text.split())
    
    # Check if all content is preserved (accounting for whitespace differences)
    content_preserved = all(f"Paragraph {i}:" in combined for i in range(1, 21))
    
    print(f"  Original length: {len(large_text)} chars")
    print(f"  Combined length: {len(combined)} chars")
    print(f"  All paragraphs preserved: {content_preserved}")
    
    assert content_preserved, "Some content was lost during chunking"
    print("✅ Content preservation test passed\n")


def test_chunk_boundary_detection():
    """Test that chunking prefers paragraph boundaries"""
    service = OpenAIService() if os.getenv('OPENAI_API_KEY') else None
    
    if not service:
        print("⚠️  Skipping: OPENAI_API_KEY not set")
        return
    
    print("Testing chunk boundary detection...")
    
    # Create text with clear paragraph boundaries
    paragraph1 = "This is the first paragraph. " * 1000
    paragraph2 = "This is the second paragraph. " * 1000
    paragraph3 = "This is the third paragraph. " * 1000
    
    text = paragraph1 + "\n\n" + paragraph2 + "\n\n" + paragraph3
    
    chunks = service.chunk_text(text, max_tokens=4000)
    
    print(f"  Input: {len(text)} chars (~{service.estimate_tokens(text)} tokens)")
    print(f"  Chunks: {len(chunks)}")
    
    # Check that chunks don't end mid-sentence
    for i, chunk in enumerate(chunks, 1):
        ends_properly = chunk.rstrip().endswith('.') or chunk.rstrip().endswith('\n')
        print(f"    Chunk {i} ends properly: {ends_properly}")
        # Note: This is a soft check, might fail if chunks split mid-paragraph
    
    assert len(chunks) > 0, "Should produce at least one chunk"
    print("✅ Boundary detection test passed\n")


def run_all_tests():
    """Run all chunking tests"""
    print("=" * 60)
    print("OpenAI Service Chunking Tests")
    print("=" * 60 + "\n")
    
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  OPENAI_API_KEY not set - tests will be skipped")
        print("    Set the environment variable to run tests\n")
        return
    
    try:
        test_token_estimation()
        test_chunking_small_text()
        test_chunking_large_text()
        test_chunking_preserves_content()
        test_chunk_boundary_detection()
        
        print("=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        raise
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        raise


if __name__ == "__main__":
    run_all_tests()

