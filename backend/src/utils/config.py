"""
Configuration Management Module

This module handles loading and managing application configuration and environment variables.
"""
import os
from typing import Optional
from dotenv import load_dotenv


class Config:
    """Configuration class to manage application settings and environment variables."""

    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Cohere API Configuration
        self.cohere_api_key = self._get_required_env_var("COHERE_API_KEY")

        # Qdrant Cloud Configuration
        self.qdrant_url = self._get_required_env_var("QDRANT_URL")
        self.qdrant_api_key = self._get_required_env_var("QDRANT_API_KEY")
        self.qdrant_collection_name = os.getenv("QDRANT_COLLECTION_NAME", "physical_ai_book_content")

        # Website Configuration
        self.physical_ai_book_base_url = self._get_required_env_var("PHYSICAL_AI_BOOK_BASE_URL")

        # Processing Configuration
        self.chunk_size = int(os.getenv("CHUNK_SIZE", "512"))
        self.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "64"))
        self.max_concurrent_requests = int(os.getenv("MAX_CONCURRENT_REQUESTS", "5"))

        # Rate Limiting Configuration
        self.cohere_rpm_limit = int(os.getenv("COHERE_RPM_LIMIT", "100"))
        self.qdrant_rpm_limit = int(os.getenv("QDRANT_RPM_LIMIT", "1000"))

        # Validation
        self._validate_config()

    def _get_required_env_var(self, var_name: str) -> str:
        """Get a required environment variable or raise an exception if not found."""
        value = os.getenv(var_name)
        if not value:
            raise ValueError(f"Required environment variable {var_name} is not set")
        return value

    def _validate_config(self):
        """Validate configuration values."""
        if self.chunk_size <= 0:
            raise ValueError("CHUNK_SIZE must be greater than 0")
        if self.chunk_overlap < 0:
            raise ValueError("CHUNK_OVERLAP must be greater than or equal to 0")
        if self.max_concurrent_requests <= 0:
            raise ValueError("MAX_CONCURRENT_REQUESTS must be greater than 0")
        if self.cohere_rpm_limit <= 0:
            raise ValueError("COHERE_RPM_LIMIT must be greater than 0")
        if self.qdrant_rpm_limit <= 0:
            raise ValueError("QDRANT_RPM_LIMIT must be greater than 0")