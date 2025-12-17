"""
URL Discovery Module for Physical AI Book Website

This module handles the discovery of all pages on the Physical AI Book website.
"""
import asyncio
import re
from urllib.parse import urljoin, urlparse
from typing import Set, List
from playwright.async_api import async_playwright
from ..utils.logger import app_logger
from ..utils.config import Config


class URLDiscoverer:
    """Class to discover and collect all URLs from the Physical AI Book website."""

    def __init__(self, config: Config):
        self.config = config
        self.visited_urls: Set[str] = set()
        self.discovered_urls: Set[str] = set()
        self.base_domain = urlparse(config.physical_ai_book_base_url).netloc

    async def discover_urls(self, max_depth: int = 3) -> Set[str]:
        """
        Discover all URLs on the Physical AI Book website up to a specified depth.

        Args:
            max_depth: Maximum depth to crawl (default: 3)

        Returns:
            Set of discovered URLs
        """
        app_logger.info(f"Starting URL discovery for {self.config.physical_ai_book_base_url} with max depth {max_depth}")

        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            try:
                # Start with the base URL
                await self._crawl_page(self.config.physical_ai_book_base_url, page, 0, max_depth)
            finally:
                await browser.close()

        app_logger.info(f"URL discovery completed. Found {len(self.discovered_urls)} unique URLs")
        return self.discovered_urls

    async def _crawl_page(self, url: str, page, current_depth: int, max_depth: int):
        """
        Crawl a single page and extract URLs.

        Args:
            url: URL to crawl
            page: Playwright page object
            current_depth: Current depth in the crawl
            max_depth: Maximum allowed depth
        """
        if current_depth > max_depth:
            return

        if url in self.visited_urls:
            return

        app_logger.debug(f"Crawling page: {url} at depth {current_depth}")

        try:
            # Navigate to the page
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)

            # Mark as visited
            self.visited_urls.add(url)

            # Extract URLs from the page
            page_urls = await self._extract_urls_from_page(page, url)

            # Add new URLs to discovered set
            for new_url in page_urls:
                if self._is_valid_url(new_url) and new_url not in self.discovered_urls:
                    self.discovered_urls.add(new_url)
                    app_logger.debug(f"Discovered URL: {new_url}")

                    # Recursively crawl if within depth limits
                    if current_depth < max_depth:
                        await self._crawl_page(new_url, page, current_depth + 1, max_depth)

        except Exception as e:
            app_logger.warning(f"Error crawling {url}: {str(e)}")

    async def _extract_urls_from_page(self, page, current_url: str) -> Set[str]:
        """
        Extract all URLs from the current page.

        Args:
            page: Playwright page object
            current_url: Current page URL for relative URL resolution

        Returns:
            Set of URLs found on the page
        """
        # Get all links from the page
        links = await page.query_selector_all('a')
        urls = set()

        for link in links:
            try:
                href = await link.get_attribute('href')
                if href:
                    # Resolve relative URLs
                    absolute_url = urljoin(current_url, href)

                    # Only include URLs from the same domain
                    if self._is_same_domain(absolute_url):
                        # Normalize the URL by removing fragments
                        normalized_url = absolute_url.split('#')[0]
                        urls.add(normalized_url)
            except Exception as e:
                app_logger.debug(f"Error extracting URL from link: {str(e)}")

        return urls

    def _is_same_domain(self, url: str) -> bool:
        """
        Check if the URL is from the same domain as the base URL.

        Args:
            url: URL to check

        Returns:
            True if URL is from the same domain, False otherwise
        """
        try:
            parsed_url = urlparse(url)
            return parsed_url.netloc == self.base_domain
        except Exception:
            return False

    def _is_valid_url(self, url: str) -> bool:
        """
        Check if the URL is valid for crawling.

        Args:
            url: URL to validate

        Returns:
            True if URL is valid, False otherwise
        """
        # Basic validation: must be HTTP/HTTPS and from the same domain
        if not url.startswith(('http://', 'https://')):
            return False

        if not self._is_same_domain(url):
            return False

        # Exclude certain file types that are not content pages
        excluded_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.zip', '.exe', '.doc', '.docx']
        if any(url.lower().endswith(ext) for ext in excluded_extensions):
            return False

        # Exclude URLs that look like admin/login pages
        excluded_patterns = [r'/admin', r'/login', r'/logout', r'/auth', r'/dashboard']
        if any(re.search(pattern, url, re.IGNORECASE) for pattern in excluded_patterns):
            return False

        return True