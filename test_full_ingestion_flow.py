#!/usr/bin/env python3
"""
Test script to simulate the full ingestion flow
"""
import os
import sys
import asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from dotenv import load_dotenv
load_dotenv()

async def test_full_ingestion_flow():
    """Test the full ingestion flow: crawl → embed → store → query."""
    try:
        from backend.src.embedder.cohere_client import CohereEmbedder
        from backend.src.storage.qdrant_manager import QdrantManager
        from backend.src.processor.text_extractor import TextExtractor
        from backend.src.processor.cleaner import ContentCleaner
        from backend.src.processor.chunker import ContentChunker
        from backend.src.utils.config import Config

        print("[OK] Successfully imported all modules for full ingestion flow")

        # Initialize configuration
        config = Config()
        print("[OK] Configuration loaded successfully")

        # Test data
        sample_content = """
        Physical AI is an emerging field that combines artificial intelligence with real-world physics.
        This interdisciplinary approach enables AI systems to understand and interact with the physical world.
        Key concepts include embodied intelligence, sensorimotor learning, and physics-informed neural networks.
        Applications range from robotics and autonomous vehicles to material science and drug discovery.
        The field represents a convergence of machine learning, physics, and engineering disciplines.
        """

        print("\nStep 1: Content Processing")
        print("-" * 30)

        # Content extraction (simulating what would come from crawling)
        text_extractor = TextExtractor(config)
        extracted_result = text_extractor.extract_text(
            f"<html><body><h1>Physical AI Concepts</h1><p>{sample_content}</p></body></html>",
            "test://physical-ai-concepts"
        )
        print(f"[OK] Content extracted: {len(extracted_result['text'])} characters")

        # Content cleaning
        content_cleaner = ContentCleaner(config)
        cleaned_content = content_cleaner.clean_content(extracted_result['text'])
        print(f"[OK] Content cleaned: {len(cleaned_content)} characters")

        # Content chunking
        content_chunker = ContentChunker(config)
        chunks = content_chunker.chunk_content(cleaned_content, extracted_result['metadata'])
        print(f"[OK] Content chunked into {len(chunks)} chunks")

        print("\nStep 2: Embedding Generation")
        print("-" * 35)

        # Generate embeddings for the chunks
        embedder = CohereEmbedder(config)

        # Extract just the text parts of the chunks for embedding
        chunk_texts = [chunk['text'] for chunk in chunks]
        embeddings = await embedder.generate_embeddings(chunk_texts)

        if embeddings and len(embeddings) == len(chunk_texts):
            print(f"[OK] Generated {len(embeddings)} embeddings successfully")
            print(f"[INFO] Embedding dimension: {len(embeddings[0]) if embeddings else 'N/A'}")
        else:
            print("[ERROR] Embedding generation failed")
            return False

        print("\nStep 3: Storage in Qdrant")
        print("-" * 25)

        # Store embeddings in Qdrant
        qdrant_manager = QdrantManager(config)

        # Ensure collection exists
        await qdrant_manager.ensure_collection_exists(vector_size=1024, distance="COSINE")
        print(f"[OK] Collection '{config.qdrant_collection_name}' ready")

        # Prepare payloads with metadata
        payloads = []
        for i, chunk in enumerate(chunks):
            payload = {
                "text": chunk['text'],
                "source_url": chunk.get('metadata', {}).get('url', 'test://source'),
                "chunk_id": f"test_chunk_{i}",
                "title": chunk.get('metadata', {}).get('title', 'Test Document'),
                "content_type": chunk.get('metadata', {}).get('content_type', 'test')
            }
            payloads.append(payload)

        # Store the vectors with integer IDs (required by Qdrant)
        ids = list(range(1, len(embeddings) + 1))  # Use integer IDs: 1, 2, 3, ...
        await qdrant_manager.store_vectors(
            vectors=embeddings,
            payloads=payloads,
            ids=ids
        )
        print(f"[OK] Stored {len(embeddings)} vectors in Qdrant")

        # Verify storage by getting count
        count = await qdrant_manager.get_vector_count()
        print(f"[INFO] Total vectors in collection: {count}")

        print("\nStep 4: Query/Retrieval Test")
        print("-" * 28)

        # Test retrieval with a query similar to the content
        query_text = "What is Physical AI and its applications?"
        query_embedding = await embedder.generate_single_embedding(query_text)

        if query_embedding:
            # Search for similar vectors
            search_results = await qdrant_manager.search_vectors(
                query_vector=query_embedding,
                limit=3  # Get top 3 results
            )

            print(f"[OK] Query search successful. Found {len(search_results)} results")
            if search_results:
                print(f"[INFO] Top result score: {search_results[0].score:.4f}")
        else:
            print("[WARNING] Query embedding generation failed, but search not tested")

        print("\n[OK] Full ingestion flow test completed successfully!")
        print("Flow: Process content → Generate embeddings → Store in Qdrant → Query retrieval")

        return True

    except ImportError as e:
        print(f"[ERROR] Import error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Error during full ingestion flow test: {e}")
        import traceback
        traceback.print_exc()
        return False

# Run the async tests
if __name__ == "__main__":
    success = asyncio.run(test_full_ingestion_flow())
    if not success:
        sys.exit(1)