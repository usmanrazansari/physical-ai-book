"""
Chat Manager Module for RAG-based Chatbot

This module handles chat functionality using retrieval-augmented generation with Qdrant and Cohere.
"""
import asyncio
import time
from typing import List, Dict, Optional
from ..utils.logger import app_logger
from ..utils.config import Config
from ..embedder.cohere_client import CohereEmbedder
from ..storage.qdrant_manager import QdrantManager
from .cohere_chat_client import CohereChatClient


class ChatManager:
    """Class to handle chat functionality using RAG (Retrieval-Augmented Generation)."""

    def __init__(self, config: Config):
        self.config = config
        self.cohere_embedder = CohereEmbedder(config)
        self.cohere_chat_client = CohereChatClient(config)
        self.qdrant_manager = QdrantManager(config)
        self.last_request_time = 0
        self.min_request_interval = 0.1  # Minimum interval between requests

    async def get_answer(self, query: str, max_results: int = 5) -> str:
        """
        Generate an answer to the user's query using RAG.

        Args:
            query: User's question
            max_results: Maximum number of results to retrieve from Qdrant

        Returns:
            Generated answer based on retrieved context
        """
        if not query.strip():
            return "Please ask a question about the Physical AI book content."

        # Rate limiting
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            await asyncio.sleep(self.min_request_interval - time_since_last_request)

        try:
            app_logger.info(f"Processing chat query: {query[:50]}...")

            # Generate embedding for the query
            query_embedding = await self.cohere_embedder.generate_single_embedding(query)
            if not query_embedding:
                app_logger.error("Failed to generate embedding for query")
                return "Sorry, I couldn't process your query. Please try again."

            # Search for relevant content in Qdrant
            search_results = await self.qdrant_manager.search_vectors(
                query_vector=query_embedding,
                limit=max_results
            )

            if not search_results:
                app_logger.warning("No relevant content found for query")
                return "I couldn't find relevant information in the book content to answer your question."

            # Prepare context from search results
            context_parts = []
            for result in search_results:
                if result.payload:
                    # Try to get content from 'text' field first (as stored in test), then 'content'
                    content = result.payload.get('text') or result.payload.get('content')
                    if content:
                        context_parts.append(content)

            if not context_parts:
                app_logger.warning("Search results returned no content")
                return "I found some related information but couldn't extract relevant content to answer your question."

            # Use Cohere's chat functionality to generate a proper answer based on context
            answer = await self.cohere_chat_client.generate_answer_with_context(
                query=query,
                contexts=context_parts[:max_results]
            )

            if answer:
                app_logger.info("Successfully generated response for query")
                return answer
            else:
                # Fallback to simple response if Cohere fails
                app_logger.warning("Cohere chat generation failed, using fallback")
                context = "\n\n".join(context_parts[:max_results])
                response = f"Based on the book content:\n\n{context[:500]}..."
                if len(context) > 500:
                    response += "\n\n(Additional context was retrieved but truncated for brevity.)"
                return response

        except Exception as e:
            app_logger.error(f"Error processing chat query: {str(e)}")
            return "Sorry, I encountered an error while processing your query. Please try again."

