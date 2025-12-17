"""
Cohere Chat Client Module for Answer Generation

This module handles interaction with the Cohere API for generating answers using chat functionality.
"""
import asyncio
import time
from typing import Optional
import cohere
from ..utils.logger import app_logger
from ..utils.config import Config


class CohereChatClient:
    """Class to handle interaction with Cohere API for generating answers using chat functionality."""

    def __init__(self, config: Config):
        self.config = config
        self.client = cohere.AsyncClient(config.cohere_api_key)
        self.last_request_time = 0
        self.min_request_interval = 60.0 / config.cohere_rpm_limit  # Respect rate limits

    async def generate_answer(self, query: str, context: str, max_tokens: int = 300) -> Optional[str]:
        """
        Generate an answer to the user's query based on the provided context.

        Args:
            query: User's question
            context: Retrieved context from Qdrant
            max_tokens: Maximum number of tokens for the response

        Returns:
            Generated answer as a string, or None if failed
        """
        if not query.strip() or not context.strip():
            return None

        # Rate limiting
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            await asyncio.sleep(self.min_request_interval - time_since_last_request)

        try:
            app_logger.debug(f"Generating answer for query: {query[:50]}...")

            # Prepare the prompt with context and query
            prompt = f"""
            Based on the following context, please answer the user's question.
            If the context doesn't contain enough information to answer the question,
            please say so and explain what information is missing.

            Context:
            {context}

            Question: {query}

            Answer:
            """

            # Call Cohere API for chat generation
            # Use current supported models (as of late 2025)
            try:
                response = await self.client.chat(
                    message=prompt,  # Using message parameter
                    model="command",  # Using the base command model which should be available
                    temperature=0.3,  # Lower temperature for more factual responses
                    max_tokens=max_tokens
                )
                answer = response.text
            except Exception as e:
                app_logger.warning(f"Chat API failed with error: {str(e)}, trying alternative approach")
                try:
                    # Try with different model name format
                    response = await self.client.chat(
                        message=prompt,
                        model="command-nightly",  # Using nightly model as fallback
                        temperature=0.3,
                        max_tokens=max_tokens
                    )
                    answer = response.text
                except Exception as e2:
                    app_logger.error(f"Both chat models failed: {str(e)}, {str(e2)}")
                    return None

            answer = answer.strip()
            app_logger.debug(f"Successfully generated answer with {len(answer)} characters")

            self.last_request_time = time.time()
            return answer

        except Exception as e:
            app_logger.error(f"Error generating answer: {str(e)}")
            return None

    async def generate_answer_with_context(self, query: str, contexts: list, max_tokens: int = 300) -> Optional[str]:
        """
        Generate an answer using multiple context chunks.

        Args:
            query: User's question
            contexts: List of context strings from Qdrant
            max_tokens: Maximum number of tokens for the response

        Returns:
            Generated answer as a string, or None if failed
        """
        if not query.strip() or not contexts:
            return None

        # Combine all contexts
        combined_context = "\n\n".join(contexts)

        return await self.generate_answer(query, combined_context, max_tokens)