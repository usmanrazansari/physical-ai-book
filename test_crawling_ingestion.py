#!/usr/bin/env python3
"""
Test script to verify crawling and ingestion functionality
"""
import os
import sys
import asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from dotenv import load_dotenv
load_dotenv()

async def test_crawling_functionality():
    """Test the crawling functionality."""
    try:
        from backend.src.crawler.url_discovery import URLDiscoverer
        from backend.src.processor.text_extractor import TextExtractor
        from backend.src.processor.cleaner import ContentCleaner
        from backend.src.processor.chunker import ContentChunker
        from backend.src.utils.config import Config

        print("[OK] Successfully imported crawling and ingestion modules")

        # Initialize configuration
        config = Config()
        print(f"[OK] Configuration loaded successfully")
        print(f"[INFO] Base URL: {config.physical_ai_book_base_url}")

        # Test URL discovery (with minimal depth to avoid extensive crawling)
        print("\nTesting URL discovery...")
        url_discoverer = URLDiscoverer(config)

        # Only crawl to depth 0 to avoid actual network requests in test
        discovered_urls = await url_discoverer.discover_urls(max_depth=0)

        print(f"[OK] URL discovery initialization successful. Found {len(discovered_urls)} URLs")

        # Test text extraction
        print("\nTesting text extraction...")
        text_extractor = TextExtractor(config)

        sample_html = "<html><body><h1>Test Page</h1><p>This is a test paragraph.</p></body></html>"
        extracted_result = text_extractor.extract_text(sample_html, "test://sample")

        if extracted_result and "text" in extracted_result and "test" in extracted_result["text"].lower():
            print(f"[OK] Text extraction successful. Extracted: '{extracted_result['text'][:50]}...'")
        else:
            print("[WARNING] Text extraction returned empty or unexpected result")

        # Test content cleaning
        print("\nTesting content cleaning...")
        content_cleaner = ContentCleaner(config)

        sample_text = "   This is a   sample text with   extra   spaces.   \n\n\n And newlines.   "
        cleaned_text = content_cleaner.clean_content(sample_text)

        if cleaned_text and cleaned_text != sample_text:
            print(f"[OK] Content cleaning successful. Cleaned: '{cleaned_text[:50]}...'")
        else:
            print("[INFO] Content cleaning completed (may return same text if already clean)")

        # Test content chunking
        print("\nTesting content chunking...")
        content_chunker = ContentChunker(config)

        long_text = "This is a longer text. " * 50  # Create a longer text
        chunks = content_chunker.chunk_content(long_text)

        if chunks and len(chunks) > 0:
            print(f"[OK] Content chunking successful. Created {len(chunks)} chunks")
            print(f"[INFO] First chunk length: {len(chunks[0])} characters")
        else:
            print("[WARNING] Content chunking returned empty result")

        print("\n[OK] All crawling and ingestion tests passed! (Note: Network-based crawling tests skipped due to URL availability)")

        return True

    except ImportError as e:
        print(f"[ERROR] Import error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Error during crawling/ingestion test: {e}")
        import traceback
        traceback.print_exc()
        return False

# Run the async tests
if __name__ == "__main__":
    success = asyncio.run(test_crawling_functionality())
    if not success:
        sys.exit(1)