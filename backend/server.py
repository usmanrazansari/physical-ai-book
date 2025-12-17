"""
Physical AI Book Backend Server

FastAPI server for the ingestion pipeline (crawl, process, embed, store)
Exposes endpoints for monitoring and controlling the pipeline.
"""
import asyncio
import logging
from datetime import datetime
from typing import Optional, Dict, Any
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Import pipeline modules
from src.crawler.url_discovery import URLDiscoverer
from src.crawler.html_fetcher import HTMLFetcher
from src.processor.text_extractor import TextExtractor
from src.processor.cleaner import ContentCleaner
from src.processor.chunker import ContentChunker
from src.embedder.cohere_client import CohereEmbedder
from src.embedder.batch_processor import BatchProcessor
from src.storage.qdrant_manager import QdrantManager
from src.storage.validator import Validator
from src.utils.config import Config
from src.utils.logger import app_logger


# Initialize FastAPI app
app = FastAPI(
    title="Physical AI Book Ingestion Pipeline",
    description="Backend server for the Physical AI Book content ingestion pipeline",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global state for pipeline status
class PipelineState:
    def __init__(self):
        self.is_running: bool = False
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.status: str = "idle"
        self.progress: str = "Not started"
        self.error: Optional[str] = None

pipeline_state = PipelineState()


class IngestionRequest(BaseModel):
    """Request model for ingestion endpoint"""
    max_depth: int = 2
    force_rerun: bool = False


class ServerStatus(BaseModel):
    """Response model for server status endpoint"""
    status: str
    timestamp: datetime
    uptime: Optional[float]


class PipelineStatus(BaseModel):
    """Response model for pipeline status endpoint"""
    is_running: bool
    status: str
    progress: str
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    error: Optional[str]


@app.get("/", response_model=ServerStatus)
async def root():
    """Root endpoint that returns server status"""
    try:
        uptime = None
        if pipeline_state.start_time:
            uptime = (datetime.now() - pipeline_state.start_time).total_seconds()

        return ServerStatus(
            status="operational",
            timestamp=datetime.now(),
            uptime=uptime
        )
    except Exception as e:
        app_logger.error(f"Error in root endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@app.get("/status", response_model=PipelineStatus)
async def get_pipeline_status():
    """Endpoint that returns the current status of the ingestion pipeline"""
    try:
        return PipelineStatus(
            is_running=pipeline_state.is_running,
            status=pipeline_state.status,
            progress=pipeline_state.progress,
            start_time=pipeline_state.start_time,
            end_time=pipeline_state.end_time,
            error=pipeline_state.error
        )
    except Exception as e:
        app_logger.error(f"Error in status endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Status error: {str(e)}")


async def run_ingestion_pipeline(max_depth: int = 2):
    """Background task to run the full ingestion pipeline"""
    global pipeline_state

    try:
        # Update pipeline state
        pipeline_state.is_running = True
        pipeline_state.status = "running"
        pipeline_state.progress = "Initializing pipeline"
        pipeline_state.start_time = datetime.now()
        pipeline_state.error = None

        app_logger.info("Starting ingestion pipeline")

        # Initialize configuration
        config = Config()

        # Initialize all components
        url_discoverer = URLDiscoverer(config)
        html_fetcher = HTMLFetcher(config)
        text_extractor = TextExtractor(config)
        content_cleaner = ContentCleaner(config)
        content_chunker = ContentChunker(config)
        cohere_embedder = CohereEmbedder(config)
        batch_processor = BatchProcessor(config)
        qdrant_manager = QdrantManager(config)
        validator = Validator(config)

        # Phase 1: URL Discovery
        pipeline_state.progress = "Discovering URLs"
        app_logger.info("Phase 1: Discovering URLs...")
        discovered_urls = await url_discoverer.discover_urls(max_depth=max_depth)
        app_logger.info(f"Discovered {len(discovered_urls)} URLs")

        # Phase 2: Content Fetching and Processing
        pipeline_state.progress = "Fetching and processing content"
        app_logger.info("Phase 2: Fetching and processing content...")
        all_chunks = []

        html_contents = await html_fetcher.fetch_multiple_html(list(discovered_urls)[:10])  # Limit for testing

        for url, html_content in html_contents.items():
            if html_content:
                # Extract text
                extraction_result = text_extractor.extract_text(html_content, url)

                # Clean content
                cleaned_content = content_cleaner.clean_content(extraction_result["text"], extraction_result["metadata"])

                # Chunk content
                chunks = content_chunker.chunk_content(cleaned_content, extraction_result["metadata"])
                all_chunks.extend(chunks)

        app_logger.info(f"Processed {len(all_chunks)} content chunks")

        # Phase 3: Embedding Generation
        pipeline_state.progress = "Generating embeddings"
        app_logger.info("Phase 3: Generating embeddings...")
        # Extract just the text from chunks for embedding
        texts_to_embed = [chunk["text"] for chunk in all_chunks]

        # Process embeddings in batches
        embeddings = await batch_processor.process_batches(texts_to_embed, cohere_embedder)

        if embeddings is None:
            raise Exception("Failed to generate embeddings")

        app_logger.info(f"Generated embeddings for {len(embeddings)} text chunks")

        # Phase 4: Vector Storage
        pipeline_state.progress = "Storing vectors"
        app_logger.info("Phase 4: Storing vectors in Qdrant...")

        # Prepare payloads with chunk metadata
        payloads = []
        for chunk in all_chunks:
            payload = chunk["metadata"].copy()
            payload["text"] = chunk["text"]  # Include the text in the payload
            payload["chunk_id"] = chunk["chunk_id"]
            payloads.append(payload)

        # Ensure the collection exists
        await qdrant_manager.ensure_collection_exists(vector_size=len(embeddings[0]) if embeddings else 1024)

        # Store vectors
        await qdrant_manager.store_vectors(embeddings, payloads)

        # Validate storage
        stored_count = await qdrant_manager.get_vector_count()
        validation_results = validator.validate_stored_vectors(len(embeddings), stored_count)

        app_logger.info(f"Stored {stored_count} vectors in Qdrant.")
        app_logger.info(f"Validation passed: {validation_results['validation_passed']}")

        # Update state on success
        pipeline_state.status = "completed"
        pipeline_state.progress = f"Completed successfully. Stored {stored_count} vectors."
        pipeline_state.end_time = datetime.now()

        app_logger.info("Ingestion pipeline completed successfully")

    except Exception as e:
        app_logger.error(f"Error in ingestion pipeline: {str(e)}")
        pipeline_state.status = "failed"
        pipeline_state.progress = f"Failed with error: {str(e)}"
        pipeline_state.error = str(e)
        pipeline_state.end_time = datetime.now()

    finally:
        pipeline_state.is_running = False


@app.post("/ingest")
async def trigger_ingestion(background_tasks: BackgroundTasks, request: IngestionRequest = None):
    """Endpoint to trigger the full ingestion pipeline"""
    if request is None:
        request = IngestionRequest()

    if pipeline_state.is_running:
        raise HTTPException(status_code=409, detail="Pipeline is already running")

    try:
        # Run the ingestion pipeline in the background
        background_tasks.add_task(run_ingestion_pipeline, request.max_depth)

        return {
            "message": "Ingestion pipeline started successfully",
            "max_depth": request.max_depth,
            "force_rerun": request.force_rerun
        }
    except Exception as e:
        app_logger.error(f"Error triggering ingestion: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ingestion trigger error: {str(e)}")


# Additional utility endpoints
@app.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now()}


if __name__ == "__main__":
    # Run the server with uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)