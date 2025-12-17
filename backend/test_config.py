"""
Test Configuration for Qdrant Content Retrieval Verification

This module extends the base configuration for testing purposes.
"""
from src.utils.config import Config


class TestConfig(Config):
    """Test configuration extending the base Config class with additional test-specific settings"""

    def __init__(self):
        super().__init__()

        # Test-specific configurations
        self.test_top_k = int(self._get_env_var_with_default("TEST_TOP_K", "5"))
        self.test_query_timeout = int(self._get_env_var_with_default("TEST_QUERY_TIMEOUT", "30"))
        self.test_log_level = self._get_env_var_with_default("TEST_LOG_LEVEL", "INFO")

        # Verification thresholds
        self.min_relevance_score = float(self._get_env_var_with_default("MIN_RELEVANCE_SCORE", "0.3"))
        self.max_response_time = float(self._get_env_var_with_default("MAX_RESPONSE_TIME", "2.0"))

        # Test data configurations
        self.test_queries_file = self._get_env_var_with_default("TEST_QUERIES_FILE", "test_queries.txt")

    def _get_env_var_with_default(self, var_name: str, default_value: str) -> str:
        """Get an environment variable with a default value"""
        import os
        return os.getenv(var_name, default_value)