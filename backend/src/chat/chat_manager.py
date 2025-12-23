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

    async def get_answer(self, query: str, max_results: int = 5):
        """
        Generate an answer to the user's query using RAG.

        Args:
            query: User's question
            max_results: Maximum number of results to retrieve from Qdrant

        Returns:
            Dictionary with response, sources, and metadata
        """
        if not query.strip():
            return {
                "response": "Please ask a question about the Physical AI book content.",
                "sources": [],
                "metadata": {}
            }

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
                return {
                    "response": "Sorry, I couldn't process your query. Please try again.",
                    "sources": [],
                    "metadata": {}
                }

            # Search for relevant content in Qdrant
            search_results = await self.qdrant_manager.search_vectors(
                query_vector=query_embedding,
                limit=max_results
            )

            if not search_results:
                app_logger.warning("No relevant content found for query")
                return {
                    "response": "I couldn't find relevant information in the book content to answer your question.",
                    "sources": [],
                    "metadata": {}
                }

            # Prepare context from search results
            context_parts = []
            sources = []
            for result in search_results:
                if result.payload:
                    # Try to get content from 'text' field first (as stored in test), then 'content'
                    content = result.payload.get('text') or result.payload.get('content')
                    if content:
                        context_parts.append(content)

                    # Collect source information
                    source_info = {
                        "title": result.payload.get('title', 'Unknown Source'),
                        "url": result.payload.get('url', ''),
                        "page": result.payload.get('page', ''),
                        "score": result.score if hasattr(result, 'score') else None
                    }
                    sources.append(source_info)

            if not context_parts:
                app_logger.warning("Search results returned no content")
                return {
                    "response": "I found some related information but couldn't extract relevant content to answer your question.",
                    "sources": sources,
                    "metadata": {}
                }

            # Use Cohere's chat functionality to generate a proper answer based on context
            answer = await self.cohere_chat_client.generate_answer_with_context(
                query=query,
                contexts=context_parts[:max_results]
            )

            if answer:
                app_logger.info("Successfully generated response for query")
                return {
                    "response": answer,
                    "sources": sources,
                    "metadata": {"retrieved_chunks": len(context_parts)}
                }
            else:
                # Fallback to simple response if Cohere fails
                app_logger.warning("Cohere chat generation failed, using fallback")
                context = "\n\n".join(context_parts[:max_results])
                response = f"Based on the book content:\n\n{context[:500]}..."
                if len(context) > 500:
                    response += "\n\n(Additional context was retrieved but truncated for brevity.)"
                return {
                    "response": response,
                    "sources": sources,
                    "metadata": {"retrieved_chunks": len(context_parts)}
                }

        except Exception as e:
            app_logger.error(f"Error processing chat query: {str(e)}")
            return {
                "response": "Sorry, I encountered an error while processing your query. Please try again.",
                "sources": [],
                "metadata": {}
            }

    async def get_answer_with_context(self, query: str, provided_context: str, max_results: int = 5):
        """
        Generate an answer to the user's query using both RAG and provided context.

        Args:
            query: User's question
            provided_context: Additional context provided by the frontend
            max_results: Maximum number of results to retrieve from Qdrant

        Returns:
            Dictionary with response, sources, and metadata
        """
        if not query.strip():
            return {
                "response": "Please ask a question about the Physical AI book content.",
                "sources": [],
                "metadata": {}
            }

        # Rate limiting
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            await asyncio.sleep(self.min_request_interval - time_since_last_request)

        try:
            app_logger.info(f"Processing chat query with context: {query[:50]}...")

            # Search for relevant content in Qdrant
            query_embedding = await self.cohere_embedder.generate_single_embedding(query)
            if not query_embedding:
                app_logger.error("Failed to generate embedding for query")
                return {
                    "response": "Sorry, I couldn't process your query. Please try again.",
                    "sources": [],
                    "metadata": {}
                }

            search_results = await self.qdrant_manager.search_vectors(
                query_vector=query_embedding,
                limit=max_results
            )

            # Prepare context from search results
            context_parts = []
            sources = []
            for result in search_results:
                if result.payload:
                    # Try to get content from 'text' field first (as stored in test), then 'content'
                    content = result.payload.get('text') or result.payload.get('content')
                    if content:
                        context_parts.append(content)

                    # Collect source information
                    source_info = {
                        "title": result.payload.get('title', 'Unknown Source'),
                        "url": result.payload.get('url', ''),
                        "page": result.payload.get('page', ''),
                        "score": result.score if hasattr(result, 'score') else None
                    }
                    sources.append(source_info)

            # Combine provided context with retrieved context
            combined_contexts = [provided_context] + context_parts[:max_results]

            # Use Cohere's chat functionality to generate a proper answer based on all contexts
            answer = await self.cohere_chat_client.generate_answer_with_context(
                query=query,
                contexts=combined_contexts
            )

            if answer:
                app_logger.info("Successfully generated response for query with provided context")
                return {
                    "response": answer,
                    "sources": sources,
                    "metadata": {"retrieved_chunks": len(context_parts), "provided_context_used": True}
                }
            else:
                # Fallback to simple response if Cohere fails
                app_logger.warning("Cohere chat generation failed, using fallback")
                all_context = "\n\n".join(combined_contexts)
                response = f"Based on the provided context and book content:\n\n{all_context[:500]}..."
                if len(all_context) > 500:
                    response += "\n\n(Additional context was retrieved but truncated for brevity.)"
                return {
                    "response": response,
                    "sources": sources,
                    "metadata": {"retrieved_chunks": len(context_parts), "provided_context_used": True}
                }

        except Exception as e:
            app_logger.error(f"Error processing chat query with context: {str(e)}")
            return {
                "response": "Sorry, I encountered an error while processing your query. Please try again.",
                "sources": [],
                "metadata": {}
            }

