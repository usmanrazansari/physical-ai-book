#!/usr/bin/env python3
"""
Test script to verify embeddings and Qdrant integration
"""
import os
import sys
import asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from dotenv import load_dotenv
load_dotenv()

async def run_tests():
    """Run all tests in a single async context to avoid event loop issues."""
    try:
        from backend.src.embedder.cohere_client import CohereEmbedder
        from backend.src.storage.qdrant_manager import QdrantManager
        from backend.src.utils.config import Config

        print("[OK] Successfully imported CohereEmbedder and QdrantManager")

        # Initialize configuration
        config = Config()
        print("[OK] Configuration loaded successfully")

        # Test Cohere embedding
        print("\nTesting Cohere embedding...")
        embedder = CohereEmbedder(config)

        test_text = "This is a test sentence for embedding."
        embedding = await embedder.generate_embeddings([test_text])

        if embedding and len(embedding) > 0:
            print(f"[OK] Cohere embedding successful. Embedding dimension: {len(embedding[0])}")
        else:
            print("[ERROR] Cohere embedding failed")
            return False

        # Test Qdrant connection
        print("\nTesting Qdrant connection...")
        qdrant_manager = QdrantManager(config)

        # First ensure the collection exists
        await qdrant_manager.ensure_collection_exists(vector_size=1024, distance="COSINE")
        print(f"[OK] Qdrant collection '{config.qdrant_collection_name}' verified/created successfully")

        # Test storing a sample vector
        test_vector = embedding[0]  # Use the embedding we just created
        test_payload = {
            "text": test_text,
            "source_url": "test://verification",
            "chunk_id": "test_chunk_1"
        }

        # Store the vector with integer IDs (Qdrant requirement)
        await qdrant_manager.store_vectors(
            vectors=[test_vector],
            payloads=[test_payload],
            ids=[1]  # Use integer ID as required by Qdrant
        )

        print("[OK] Sample vector stored successfully in Qdrant")

        # Get the vector count to verify it was stored
        count = await qdrant_manager.get_vector_count()
        print(f"[OK] Vector count after storing: {count}")

        print("\n[OK] All embeddings and Qdrant integration tests passed!")
        return True

    except Exception as e:
        print(f"[ERROR] Error during embedding/Qdrant test: {e}")
        return False

# Run the async tests
if __name__ == "__main__":
    success = asyncio.run(run_tests())
    if not success:
        sys.exit(1)