"""
Validator Module for Vector Storage

This module handles validation of stored vectors and data integrity checks.
"""
from typing import List, Dict
from ..utils.logger import app_logger
from ..utils.config import Config


class Validator:
    """Class to handle validation of stored vectors and data integrity checks."""

    def __init__(self, config: Config):
        self.config = config

    def validate_embedding(self, embedding: List[float], expected_dimension: int = None) -> bool:
        """
        Validate an embedding vector.

        Args:
            embedding: Embedding vector to validate
            expected_dimension: Expected dimension of the embedding (optional)

        Returns:
            True if embedding is valid, False otherwise
        """
        if not embedding:
            app_logger.warning("Invalid embedding: empty")
            return False

        if not isinstance(embedding, list):
            app_logger.warning("Invalid embedding: not a list")
            return False

        if expected_dimension and len(embedding) != expected_dimension:
            app_logger.warning(f"Invalid embedding: expected dimension {expected_dimension}, got {len(embedding)}")
            return False

        # Check if all elements are numbers
        for i, value in enumerate(embedding):
            if not isinstance(value, (int, float)):
                app_logger.warning(f"Invalid embedding: element at index {i} is not a number")
                return False

        return True

    def validate_payload(self, payload: Dict) -> bool:
        """
        Validate a payload dictionary.

        Args:
            payload: Payload dictionary to validate

        Returns:
            True if payload is valid, False otherwise
        """
        if not payload or not isinstance(payload, dict):
            app_logger.warning("Invalid payload: not a dictionary or empty")
            return False

        # Check for required fields (at minimum, we need some content identification)
        if "url" not in payload and "text" not in payload:
            app_logger.warning("Invalid payload: missing required fields (url or text)")
            return False

        return True

    def validate_stored_vectors(self, expected_count: int, actual_count: int) -> Dict:
        """
        Validate that the expected number of vectors were stored.

        Args:
            expected_count: Number of vectors that were expected to be stored
            actual_count: Actual number of vectors stored

        Returns:
            Dictionary with validation results
        """
        results = {
            "expected_count": expected_count,
            "actual_count": actual_count,
            "count_match": expected_count == actual_count,
            "validation_passed": True,
            "issues": []
        }

        if expected_count != actual_count:
            results["validation_passed"] = False
            results["issues"].append(f"Expected {expected_count} vectors, but found {actual_count}")

        if actual_count < 0:
            results["validation_passed"] = False
            results["issues"].append("Negative vector count reported")

        if results["validation_passed"]:
            app_logger.info(f"Vector storage validation passed: {actual_count} vectors stored as expected")
        else:
            app_logger.warning(f"Vector storage validation failed: {', '.join(results['issues'])}")

        return results