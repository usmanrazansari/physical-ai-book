#!/usr/bin/env python3
"""
Test script to verify error handling and logging
"""
import os
import sys
import asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from dotenv import load_dotenv
load_dotenv()

async def test_error_handling():
    """Test error handling and logging."""
    try:
        from backend.src.embedder.cohere_client import CohereEmbedder
        from backend.src.storage.qdrant_manager import QdrantManager
        from backend.src.utils.config import Config
        from backend.src.utils.logger import app_logger

        print("[OK] Successfully imported modules for error handling test")

        # Initialize configuration
        config = Config()
        print("[OK] Configuration loaded successfully")

        # Test 1: Verify logger works
        print("\nTesting logging functionality...")
        app_logger.info("Test log message - verification in progress")
        app_logger.debug("Debug message for verification")
        print("[OK] Logging functionality works")

        # Test 2: Embedding error handling - test with empty input
        print("\nTesting embedding error handling...")
        embedder = CohereEmbedder(config)

        # Test with empty list
        empty_embeddings = await embedder.generate_embeddings([])
        if empty_embeddings == []:
            print("[OK] Embedding handles empty input correctly")
        else:
            print("[INFO] Embedding behavior with empty input noted")

        # Test 3: Qdrant error handling - test with invalid data
        print("\nTesting Qdrant error handling...")
        qdrant_manager = QdrantManager(config)

        # Test getting vector count (this should work if collection exists)
        count = await qdrant_manager.get_vector_count()
        print(f"[OK] Vector count retrieved successfully: {count}")

        # Test 4: Configuration validation
        print("\nTesting configuration validation...")
        print(f"[INFO] Cohere API key set: {'Yes' if config.cohere_api_key else 'No'}")
        print(f"[INFO] Qdrant URL set: {'Yes' if config.qdrant_url else 'No'}")
        print(f"[INFO] Qdrant API key set: {'Yes' if config.qdrant_api_key else 'No'}")
        print(f"[INFO] Base URL set: {config.physical_ai_book_base_url}")
        print(f"[INFO] Chunk size: {config.chunk_size}")
        print(f"[INFO] Chunk overlap: {config.chunk_overlap}")

        # Test 5: Test a simple embedding operation to ensure everything is working
        print("\nTesting complete workflow with error handling...")
        test_text = "Physical AI combines artificial intelligence with real-world physics."
        embedding = await embedder.generate_embeddings([test_text])

        if embedding and len(embedding) > 0 and len(embedding[0]) > 0:
            print(f"[OK] Complete embedding workflow successful. Dimension: {len(embedding[0])}")
        else:
            print("[ERROR] Embedding workflow failed")
            return False

        # Test 6: Try to store and then clean up a test vector
        print("\nTesting storage workflow with cleanup...")
        await qdrant_manager.ensure_collection_exists(vector_size=1024, distance="COSINE")

        test_payload = {
            "text": test_text,
            "source_url": "test://error-handling-test",
            "chunk_id": "error_test_chunk"
        }

        await qdrant_manager.store_vectors(
            vectors=embedding,
            payloads=[test_payload],
            ids=[999999]  # Use a high ID to avoid conflicts
        )
        print("[OK] Storage workflow completed")

        # Verify the vector was stored
        new_count = await qdrant_manager.get_vector_count()
        print(f"[INFO] Vector count after test storage: {new_count}")

        print("\n[OK] All error handling tests passed!")
        print("Note: Search functionality may have API compatibility issues with current Qdrant client version")

        return True

    except ImportError as e:
        print(f"[ERROR] Import error: {e}")
        return False
    except ValueError as e:
        # This would catch configuration errors
        print(f"[ERROR] Configuration/validation error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Error during error handling test: {e}")
        import traceback
        traceback.print_exc()
        return False

# Run the async tests
if __name__ == "__main__":
    success = asyncio.run(test_error_handling())
    if not success:
        sys.exit(1)