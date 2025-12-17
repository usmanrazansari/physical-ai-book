"""
Text Extractor Module for Physical AI Book Content

This module handles extracting meaningful text content from HTML pages.
"""
from typing import Dict, List, Tuple
from bs4 import BeautifulSoup
from ..utils.logger import app_logger
from ..utils.config import Config


class TextExtractor:
    """Class to extract meaningful text content from HTML pages."""

    def __init__(self, config: Config):
        self.config = config

    def extract_text(self, html_content: str, url: str = "") -> Dict:
        """
        Extract text content from HTML with metadata.

        Args:
            html_content: HTML content to extract text from
            url: Source URL for metadata

        Returns:
            Dictionary containing extracted text and metadata
        """
        soup = BeautifulSoup(html_content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Extract title
        title_tag = soup.find('title')
        title = title_tag.get_text().strip() if title_tag else ""

        # Extract main content - focus on content areas typical in Docusaurus sites
        main_content = self._extract_main_content(soup)

        # Extract headings hierarchy
        headings = self._extract_headings(soup)

        # Get text content
        text_content = main_content.get_text(separator=' ', strip=True)

        # Extract metadata
        metadata = {
            "url": url,
            "title": title,
            "headings": headings,
            "word_count": len(text_content.split()),
            "content_type": self._determine_content_type(url, soup)
        }

        return {
            "text": text_content,
            "metadata": metadata,
            "html_structure": str(main_content)
        }

    def _extract_main_content(self, soup) -> BeautifulSoup:
        """
        Extract the main content area from the HTML.

        Args:
            soup: BeautifulSoup object

        Returns:
            BeautifulSoup object containing main content
        """
        # Try common selectors for Docusaurus and similar documentation sites
        selectors_to_try = [
            '[role="main"]',
            '.main-wrapper',
            '.container',
            '.main-content',
            '.content',
            '.docs-content',
            '.theme-doc-markdown',
            'main',
            '.article',
            '.post-content',
            'body'
        ]

        for selector in selectors_to_try:
            content = soup.select_one(selector)
            if content:
                return content

        # If no specific selector matches, return the body
        body = soup.find('body')
        return body if body else soup

    def _extract_headings(self, soup) -> List[Dict]:
        """
        Extract heading hierarchy from the HTML.

        Args:
            soup: BeautifulSoup object

        Returns:
            List of heading dictionaries with level and text
        """
        headings = []
        for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            headings.append({
                "level": int(heading.name[1]),
                "text": heading.get_text().strip()
            })
        return headings

    def _determine_content_type(self, url: str, soup) -> str:
        """
        Determine the content type based on URL and HTML structure.

        Args:
            url: Source URL
            soup: BeautifulSoup object

        Returns:
            Content type string
        """
        # Check for common patterns in the URL
        if '/docs/' in url:
            return 'documentation'
        elif '/blog/' in url or '/posts/' in url:
            return 'blog'
        elif '/api/' in url:
            return 'api_reference'
        elif '/tutorial/' in url:
            return 'tutorial'
        else:
            # Check for common elements in the HTML
            if soup.find('article'):
                return 'article'
            elif soup.find('div', class_=lambda x: x and 'doc' in x.lower()):
                return 'documentation'
            else:
                return 'general'