"""
Cohere Client Module for Embedding Generation

This module handles interaction with the Cohere API for generating embeddings.
"""
import asyncio
import time
from typing import List, Optional
import cohere
from ..utils.logger import app_logger
from ..utils.config import Config


class CohereEmbedder:
    """Class to handle interaction with Cohere API for generating embeddings."""

    def __init__(self, config: Config):
        self.config = config
        self.client = cohere.AsyncClient(config.cohere_api_key)
        self.last_request_time = 0
        self.min_request_interval = 60.0 / config.cohere_rpm_limit  # Respect rate limits

    async def generate_embeddings(self, texts: List[str], model: str = "embed-multilingual-v3.0") -> Optional[List[List[float]]]:
        """
        Generate embeddings for a list of texts.

        Args:
            texts: List of text strings to embed
            model: Cohere model to use for embeddings

        Returns:
            List of embedding vectors, or None if failed
        """
        if not texts:
            return []

        # Rate limiting
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            await asyncio.sleep(self.min_request_interval - time_since_last_request)

        try:
            app_logger.debug(f"Generating embeddings for {len(texts)} texts using model {model}")

            # Call Cohere API
            response = await self.client.embed(
                texts=texts,
                model=model,
                input_type="search_document"  # Optimize for search use case
            )

            embeddings = response.embeddings
            app_logger.debug(f"Successfully generated embeddings for {len(texts)} texts")

            self.last_request_time = time.time()
            return embeddings

        except Exception as e:
            app_logger.error(f"Error generating embeddings: {str(e)}")
            return None

    async def generate_single_embedding(self, text: str, model: str = "embed-multilingual-v3.0") -> Optional[List[float]]:
        """
        Generate embedding for a single text.

        Args:
            text: Text string to embed
            model: Cohere model to use for embeddings

        Returns:
            Embedding vector as a list of floats, or None if failed
        """
        embeddings = await self.generate_embeddings([text], model)
        if embeddings and len(embeddings) > 0:
            return embeddings[0]
        return None