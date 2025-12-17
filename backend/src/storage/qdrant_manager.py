"""
Qdrant Manager Module for Vector Storage

This module handles interaction with Qdrant Cloud for storing and retrieving embeddings.
"""
import asyncio
import time
from typing import List, Dict, Optional
from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
from ..utils.logger import app_logger
from ..utils.config import Config


class QdrantManager:
    """Class to handle interaction with Qdrant Cloud for vector storage."""

    def __init__(self, config: Config):
        self.config = config
        self.client = AsyncQdrantClient(
            url=config.qdrant_url,
            api_key=config.qdrant_api_key,
            prefer_grpc=False  # Using HTTP for better compatibility
        )
        self.last_request_time = 0
        self.min_request_interval = 60.0 / config.qdrant_rpm_limit  # Respect rate limits

    async def ensure_collection_exists(self, vector_size: int = 1024, distance: str = "Cosine"):
        """
        Ensure the collection exists with the specified configuration.

        Args:
            vector_size: Size of the embedding vectors
            distance: Distance metric for similarity search
        """
        # Check if collection exists
        try:
            collections = await self.client.get_collections()
            collection_exists = any(col.name == self.config.qdrant_collection_name for col in collections.collections)

            if not collection_exists:
                # Create collection
                await self.client.create_collection(
                    collection_name=self.config.qdrant_collection_name,
                    vectors_config=models.VectorParams(
                        size=vector_size,
                        distance=models.Distance[distance]
                    ),
                    # Set up for Qdrant Cloud Free Tier limitations
                    optimizers_config=models.OptimizersConfigDiff(
                        memmap_threshold=20000,  # Use memory mapping for larger collections
                        indexing_threshold=20000,  # Start indexing when collection reaches this size
                    )
                )
                app_logger.info(f"Created collection: {self.config.qdrant_collection_name}")
            else:
                app_logger.info(f"Collection already exists: {self.config.qdrant_collection_name}")
        except Exception as e:
            app_logger.error(f"Error ensuring collection exists: {str(e)}")
            raise

    async def store_vectors(self, vectors: List[List[float]], payloads: List[Dict], ids: List[str] = None):
        """
        Store vectors with their payloads in Qdrant.

        Args:
            vectors: List of embedding vectors to store
            payloads: List of metadata payloads corresponding to each vector
            ids: Optional list of IDs for the vectors (if not provided, will be auto-generated)
        """
        if not vectors or len(vectors) != len(payloads):
            raise ValueError("Vectors and payloads must have the same length and not be empty")

        # Rate limiting
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            await asyncio.sleep(self.min_request_interval - time_since_last_request)

        try:
            # Generate IDs if not provided
            if ids is None:
                ids = [f"doc_{i}" for i in range(len(vectors))]

            # Prepare points for upsert
            points = [
                models.PointStruct(
                    id=idx,
                    vector=vector,
                    payload=payload
                )
                for idx, vector, payload in zip(ids, vectors, payloads)
            ]

            # Upsert points to Qdrant
            await self.client.upsert(
                collection_name=self.config.qdrant_collection_name,
                points=points
            )

            app_logger.info(f"Successfully stored {len(vectors)} vectors in Qdrant")

            self.last_request_time = time.time()
        except Exception as e:
            app_logger.error(f"Error storing vectors in Qdrant: {str(e)}")
            raise

    async def search_vectors(self, query_vector: List[float], limit: int = 10, filters: Dict = None):
        """
        Search for similar vectors in Qdrant.

        Args:
            query_vector: Query embedding vector
            limit: Number of results to return
            filters: Optional filters for metadata search

        Returns:
            List of search results with scores and payloads
        """
        # Rate limiting
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            await asyncio.sleep(self.min_request_interval - time_since_last_request)

        try:
            # Prepare filters if provided
            qdrant_filters = None
            if filters:
                filter_conditions = []
                for key, value in filters.items():
                    filter_conditions.append(
                        models.FieldCondition(
                            key=key,
                            match=models.MatchValue(value=value)
                        )
                    )
                if filter_conditions:
                    qdrant_filters = models.Filter(must=filter_conditions)

            # Perform search using query_points method
            query_response = await self.client.query_points(
                collection_name=self.config.qdrant_collection_name,
                query=query_vector,
                limit=limit,
                query_filter=qdrant_filters
            )

            # Extract results from QueryResponse object
            search_results = query_response.points
            app_logger.debug(f"Search returned {len(search_results)} results")

            self.last_request_time = time.time()
            return search_results
        except Exception as e:
            app_logger.error(f"Error searching vectors in Qdrant: {str(e)}")
            raise

    async def get_vector_count(self) -> int:
        """
        Get the total number of vectors stored in the collection.

        Returns:
            Total count of vectors in the collection
        """
        try:
            collection_info = await self.client.get_collection(self.config.qdrant_collection_name)
            return collection_info.points_count
        except Exception as e:
            app_logger.error(f"Error getting vector count: {str(e)}")
            return 0