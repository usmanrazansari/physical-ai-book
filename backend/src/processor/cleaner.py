"""
Content Cleaner Module for Physical AI Book Content

This module handles cleaning and normalizing extracted text content.
"""
import re
from typing import Dict
from ..utils.logger import app_logger
from ..utils.config import Config


class ContentCleaner:
    """Class to clean and normalize extracted text content."""

    def __init__(self, config: Config):
        self.config = config

    def clean_content(self, content: str, metadata: Dict = None) -> str:
        """
        Clean and normalize text content.

        Args:
            content: Raw text content to clean
            metadata: Optional metadata associated with the content

        Returns:
            Cleaned text content
        """
        if not content:
            return ""

        # Remove extra whitespace
        content = self._normalize_whitespace(content)

        # Remove special characters and normalize
        content = self._remove_special_characters(content)

        # Remove boilerplate content specific to documentation sites
        content = self._remove_boilerplate(content)

        # Ensure content is properly formatted
        content = self._normalize_paragraphs(content)

        return content.strip()

    def _normalize_whitespace(self, content: str) -> str:
        """
        Normalize whitespace in content.

        Args:
            content: Text content to normalize

        Returns:
            Content with normalized whitespace
        """
        # Replace multiple spaces with single space
        content = re.sub(r'\s+', ' ', content)

        # Handle newlines - preserve paragraph breaks but normalize others
        content = re.sub(r'\n\s*\n', '\n\n', content)

        return content.strip()

    def _remove_special_characters(self, content: str) -> str:
        """
        Remove special characters and normalize text.

        Args:
            content: Text content to process

        Returns:
            Content with special characters removed or normalized
        """
        # Remove or replace special characters that might interfere with embeddings
        # Keep standard punctuation and basic symbols
        content = re.sub(r'[^\w\s\-\.\!\?\;\:\,\(\)\[\]\{\}\'\"\/\n]', ' ', content)

        # Normalize quotes
        content = content.replace("''", '"').replace("``", '"')

        return content

    def _remove_boilerplate(self, content: str) -> str:
        """
        Remove common boilerplate content from documentation sites.

        Args:
            content: Text content to process

        Returns:
            Content with boilerplate removed
        """
        # Common patterns found in documentation sites that aren't meaningful content
        boilerplate_patterns = [
            r'Last updated.*',  # Last updated timestamps
            r'Edit this page.*',  # Edit links
            r'Was this page helpful\?.*',  # Feedback prompts
            r'Found an issue\?.*',  # Issue reporting links
            r'\s+\d+\s+stars\s+\d+\s+forks',  # GitHub stats
            r'©\s+\d{4}.*',  # Copyright notices
            r'Did you know we.*',  # Promotional content
            r'Learn more about.*',  # Call-to-action phrases
            r'Get started with.*',  # CTA phrases
        ]

        for pattern in boilerplate_patterns:
            content = re.sub(pattern, '', content, flags=re.IGNORECASE)

        return content.strip()

    def _normalize_paragraphs(self, content: str) -> str:
        """
        Normalize paragraph breaks in content.

        Args:
            content: Text content to normalize

        Returns:
            Content with normalized paragraphs
        """
        # Ensure proper paragraph separation
        content = re.sub(r'\n\s*\n', '\n\n', content)

        # Remove extra empty lines
        lines = content.split('\n')
        normalized_lines = []
        prev_line_empty = False

        for line in lines:
            line = line.strip()
            if not line:
                if not prev_line_empty:
                    normalized_lines.append('')
                    prev_line_empty = True
            else:
                normalized_lines.append(line)
                prev_line_empty = False

        return '\n'.join(normalized_lines).strip()