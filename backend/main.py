"""
Main Entry Point for Physical AI Book Content Ingestion System

This script orchestrates the entire ingestion pipeline from crawling to vector storage.
"""
import argparse
import sys
import os
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_import_paths():
    """Setup import paths for different execution contexts."""
    # Get the directory of this file (backend directory)
    current_file_dir = os.path.dirname(os.path.abspath(__file__))

    # Add backend directory to the beginning of path if not already there
    if current_file_dir not in sys.path:
        sys.path.insert(0, current_file_dir)

    # Also check if we need to add the parent directory to handle different contexts
    parent_dir = os.path.dirname(current_file_dir)  # This gets the parent directory
    if parent_dir not in sys.path:
        sys.path.append(parent_dir)

# Setup import paths
setup_import_paths()

# Import the modules after setting up paths
from src.crawler.url_discovery import URLDiscoverer
from src.crawler.html_fetcher import HTMLFetcher
from src.processor.text_extractor import TextExtractor
from src.processor.cleaner import ContentCleaner
from src.processor.chunker import ContentChunker
from src.embedder.cohere_client import CohereEmbedder
from src.embedder.batch_processor import BatchProcessor
from src.storage.qdrant_manager import QdrantManager
from src.storage.validator import Validator
from src.chat.chat_manager import ChatManager
from src.utils.config import Config
from src.utils.logger import app_logger

# Create FastAPI app instance
app = FastAPI(
    title="Physical AI Book Content Ingestion API",
    description="API for the Physical AI Book Content Ingestion System",
    version="1.0.0"
)

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://usmanrazansari.github.io",
        "https://usmanrazansari.github.io/",
        "https://*.github.io",
        "https://*.hf.space",  # Allow Hugging Face Spaces
        "https://usmanhello-physical-ai-book.hf.space",  # Specific Hugging Face Space
        "http://localhost:3000",  # Local development
        "http://localhost:8000",  # Local backend
        "http://127.0.0.1:8000",  # Local backend alternative
        "*",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
    allow_headers=["*"],
    max_age=86400,  # Cache preflight requests for 24 hours
)


@app.get("/status")
async def status():
    """Sample endpoint returning system status."""
    return {"status": "ok"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Physical AI Book Ingestion Backend"}


@app.get("/config")
async def config_check():
    """Configuration check endpoint."""
    required_vars = [
        "QDRANT_API_KEY",
        "QDRANT_URL",
        "COHERE_API_KEY"
    ]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    return {
        "status": "ok" if not missing_vars else "missing_config",
        "missing_variables": missing_vars,
        "all_variables_present": len(missing_vars) == 0
    }


from fastapi import Request
import json

@app.post("/chat")
async def chat(request: Request):
    """Chat endpoint that accepts user queries and returns responses based on book content."""
    try:
        # Get JSON data from request
        data = await request.json()
        query = data.get('query', '')
        context = data.get('context', None)  # Additional context from selected text

        config = Config()
        chat_manager = ChatManager(config)

        # Pass context to the chat manager if available
        if context:
            response = await chat_manager.get_answer_with_context(query, context)
        else:
            response = await chat_manager.get_answer(query)

        return response
    except Exception as e:
        app_logger.error(f"Error in chat endpoint: {str(e)}")
        return {
            "response": "Sorry, I encountered an error while processing your query. Please try again.",
            "sources": [],
            "metadata": {}
        }


def main():
    parser = argparse.ArgumentParser(description='Physical AI Book Content Ingestion System')
    parser.add_argument('--mode', choices=['crawl', 'process', 'embed', 'store', 'full'],
                        default='full', help='Execution mode for the ingestion pipeline')
    args = parser.parse_args()

    try:
        # Initialize configuration
        config = Config()
        app_logger.info(f"Starting Physical AI Book Content Ingestion System in {args.mode} mode")

        if args.mode in ['full', 'crawl']:
            app_logger.info("Starting URL discovery...")
            url_discoverer = URLDiscoverer(config)
            discovered_urls = asyncio.run(url_discoverer.discover_urls(max_depth=2))
            app_logger.info(f"Discovered {len(discovered_urls)} URLs")

        if args.mode in ['full', 'process']:
            app_logger.info("Starting content processing...")
            # Example of how content processing would work
            # This would typically be done after crawling in a full implementation
            html_fetcher = HTMLFetcher(config)
            text_extractor = TextExtractor(config)
            content_cleaner = ContentCleaner(config)
            content_chunker = ContentChunker(config)

            # In a real implementation, we would process the discovered URLs
            # For now, we'll just show the structure
            app_logger.info("Content processing components initialized")

        if args.mode in ['full', 'embed']:
            app_logger.info("Starting embedding generation...")
            cohere_embedder = CohereEmbedder(config)
            batch_processor = BatchProcessor(config)
            app_logger.info("Embedding generation components initialized")

        if args.mode in ['full', 'store']:
            app_logger.info("Starting vector storage...")
            qdrant_manager = QdrantManager(config)
            validator = Validator(config)
            app_logger.info("Vector storage components initialized")

        app_logger.info("Physical AI Book Content Ingestion System completed successfully")

    except ValueError as e:
        app_logger.error(f"Configuration error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        app_logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()