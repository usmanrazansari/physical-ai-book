"""
Example script demonstrating the full Physical AI Book ingestion pipeline.

This script shows how all components work together to crawl, process, embed, and store
content from the Physical AI Book website.
"""
import asyncio
import sys
from typing import List, Dict
from src.crawler.url_discovery import URLDiscoverer
from src.crawler.html_fetcher import HTMLFetcher
from src.processor.text_extractor import TextExtractor
from src.processor.cleaner import ContentCleaner
from src.processor.chunker import ContentChunker
from src.embedder.cohere_client import CohereEmbedder
from src.embedder.batch_processor import BatchProcessor
from src.storage.qdrant_manager import QdrantManager
from src.storage.validator import Validator
from src.utils.config import Config
from src.utils.logger import app_logger


async def run_full_ingestion_pipeline():
    """Run the complete ingestion pipeline from crawling to vector storage."""
    config = Config()

    # Initialize all components
    url_discoverer = URLDiscoverer(config)
    html_fetcher = HTMLFetcher(config)
    text_extractor = TextExtractor(config)
    content_cleaner = ContentCleaner(config)
    content_chunker = ContentChunker(config)
    cohere_embedder = CohereEmbedder(config)
    batch_processor = BatchProcessor(config)
    qdrant_manager = QdrantManager(config)
    validator = Validator(config)

    app_logger.info("Starting full ingestion pipeline...")

    # Phase 1: URL Discovery
    app_logger.info("Phase 1: Discovering URLs...")
    discovered_urls = await url_discoverer.discover_urls(max_depth=2)
    app_logger.info(f"Discovered {len(discovered_urls)} URLs")

    # For demonstration, let's process just a few URLs
    sample_urls = list(discovered_urls)[:5]  # Process first 5 URLs
    app_logger.info(f"Processing sample of {len(sample_urls)} URLs")

    # Phase 2: Content Fetching and Extraction
    app_logger.info("Phase 2: Fetching and extracting content...")
    html_contents = await html_fetcher.fetch_multiple_html(sample_urls)

    all_chunks = []
    for url in sample_urls:
        html_content = html_contents.get(url)
        if html_content:
            # Extract text
            extraction_result = text_extractor.extract_text(html_content, url)

            # Clean content
            cleaned_content = content_cleaner.clean_content(extraction_result["text"], extraction_result["metadata"])

            # Chunk content
            chunks = content_chunker.chunk_content(cleaned_content, extraction_result["metadata"])
            all_chunks.extend(chunks)

    app_logger.info(f"Extracted and chunked content into {len(all_chunks)} chunks")

    # Phase 3: Embedding Generation
    app_logger.info("Phase 3: Generating embeddings...")
    # Extract just the text from chunks for embedding
    texts_to_embed = [chunk["text"] for chunk in all_chunks]

    # Process embeddings in batches
    embeddings = await batch_processor.process_batches(texts_to_embed, cohere_embedder)

    if embeddings is None:
        app_logger.error("Failed to generate embeddings")
        return False

    app_logger.info(f"Generated embeddings for {len(embeddings)} text chunks")

    # Validate embeddings
    for i, embedding in enumerate(embeddings):
        if not validator.validate_embedding(embedding):
            app_logger.error(f"Invalid embedding at index {i}")
            return False

    # Phase 4: Vector Storage
    app_logger.info("Phase 4: Storing vectors in Qdrant...")

    # Prepare payloads with chunk metadata
    payloads = []
    for chunk in all_chunks:
        payload = chunk["metadata"].copy()
        payload["text"] = chunk["text"]  # Include the text in the payload
        payload["chunk_id"] = chunk["chunk_id"]
        payloads.append(payload)

    # Ensure the collection exists
    await qdrant_manager.ensure_collection_exists(vector_size=len(embeddings[0]) if embeddings else 1024)

    # Store vectors
    await qdrant_manager.store_vectors(embeddings, payloads)

    # Validate storage
    stored_count = await qdrant_manager.get_vector_count()
    validation_results = validator.validate_stored_vectors(len(embeddings), stored_count)

    app_logger.info(f"Pipeline completed. Stored {stored_count} vectors in Qdrant.")
    app_logger.info(f"Validation passed: {validation_results['validation_passed']}")

    return validation_results['validation_passed']


if __name__ == "__main__":
    success = asyncio.run(run_full_ingestion_pipeline())
    if success:
        print("Ingestion pipeline completed successfully!")
        sys.exit(0)
    else:
        print("Ingestion pipeline failed!")
        sys.exit(1)