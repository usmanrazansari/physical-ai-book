"""
HTML Fetcher Module for Physical AI Book Website

This module handles fetching HTML content from discovered URLs.
"""
import asyncio
import time
from typing import Dict, Optional
from playwright.async_api import async_playwright
from ..utils.logger import app_logger
from ..utils.config import Config


class HTMLFetcher:
    """Class to fetch HTML content from URLs with proper error handling and rate limiting."""

    def __init__(self, config: Config):
        self.config = config
        self.last_request_time = 0
        self.min_request_interval = 1.0 / (self.config.max_concurrent_requests * 0.8)  # Respect rate limits

    async def fetch_html(self, url: str) -> Optional[str]:
        """
        Fetch HTML content from a URL.

        Args:
            url: URL to fetch

        Returns:
            HTML content as string, or None if failed
        """
        # Rate limiting
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            await asyncio.sleep(self.min_request_interval - time_since_last_request)

        app_logger.debug(f"Fetching HTML from: {url}")

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()

                # Set a reasonable timeout
                page.set_default_timeout(30000)

                # Navigate to the page
                response = await page.goto(url, wait_until="domcontentloaded")

                if response and response.status == 200:
                    # Get the HTML content
                    html_content = await page.content()
                    app_logger.debug(f"Successfully fetched HTML from {url} ({len(html_content)} characters)")

                    await browser.close()
                    self.last_request_time = time.time()
                    return html_content
                else:
                    app_logger.warning(f"Failed to fetch {url}, status code: {response.status if response else 'N/A'}")
                    await browser.close()
                    return None

        except Exception as e:
            app_logger.warning(f"Error fetching HTML from {url}: {str(e)}")
            return None

    async def fetch_multiple_html(self, urls: list, max_concurrent: int = 5) -> Dict[str, Optional[str]]:
        """
        Fetch HTML content from multiple URLs with controlled concurrency.

        Args:
            urls: List of URLs to fetch
            max_concurrent: Maximum number of concurrent requests

        Returns:
            Dictionary mapping URLs to their HTML content (or None if failed)
        """
        semaphore = asyncio.Semaphore(max_concurrent)

        async def fetch_with_semaphore(url):
            async with semaphore:
                return await self.fetch_html(url)

        # Create tasks for all URLs
        tasks = [fetch_with_semaphore(url) for url in urls]

        # Execute tasks with concurrency control
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Map results back to URLs
        html_contents = {}
        for i, url in enumerate(urls):
            if isinstance(results[i], Exception):
                app_logger.error(f"Exception occurred while fetching {url}: {results[i]}")
                html_contents[url] = None
            else:
                html_contents[url] = results[i]

        return html_contents