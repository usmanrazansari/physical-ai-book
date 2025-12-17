"""
Batch Processor Module for Embedding Generation

This module handles batching text chunks for efficient embedding generation.
"""
import asyncio
from typing import List, Dict, Optional
from ..utils.logger import app_logger
from ..utils.config import Config


class BatchProcessor:
    """Class to handle batching of text chunks for efficient embedding generation."""

    def __init__(self, config: Config):
        self.config = config

    def create_batches(self, texts: List[str], max_batch_size: int = 96) -> List[List[str]]:
        """
        Create batches of texts for embedding generation.

        Args:
            texts: List of text strings to batch
            max_batch_size: Maximum size of each batch (Cohere's limit is 96)

        Returns:
            List of text batches
        """
        if not texts:
            return []

        # Ensure batch size doesn't exceed Cohere's limit
        effective_batch_size = min(max_batch_size, 96)

        batches = []
        for i in range(0, len(texts), effective_batch_size):
            batch = texts[i:i + effective_batch_size]
            batches.append(batch)

        app_logger.debug(f"Created {len(batches)} batches from {len(texts)} texts (batch size: {effective_batch_size})")
        return batches

    async def process_batches(self, texts: List[str], embedder, max_batch_size: int = 96) -> Optional[List[List[float]]]:
        """
        Process batches of texts through the embedder with concurrency control.

        Args:
            texts: List of text strings to embed
            embedder: Embedder instance (e.g., CohereEmbedder)
            max_batch_size: Maximum size of each batch

        Returns:
            List of embedding vectors, or None if failed
        """
        if not texts:
            return []

        # Create batches
        batches = self.create_batches(texts, max_batch_size)
        all_embeddings = []

        # Process batches with concurrency control
        semaphore = asyncio.Semaphore(self.config.max_concurrent_requests)

        async def process_batch(batch):
            async with semaphore:
                return await embedder.generate_embeddings(batch)

        # Process all batches concurrently
        batch_results = await asyncio.gather(*[process_batch(batch) for batch in batches], return_exceptions=True)

        # Collect results
        for i, result in enumerate(batch_results):
            if isinstance(result, Exception):
                app_logger.error(f"Error processing batch {i}: {result}")
                return None
            elif result is not None:
                all_embeddings.extend(result)
            else:
                app_logger.warning(f"Batch {i} returned None embeddings")
                return None

        app_logger.info(f"Successfully processed {len(texts)} texts in {len(batches)} batches")
        return all_embeddings