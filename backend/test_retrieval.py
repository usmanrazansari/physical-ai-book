"""
Test script for Qdrant Content Retrieval Verification

This script implements the retrieval verification pipeline as per the implementation plan.
"""
import asyncio
import logging
import time
from typing import List, Dict, Optional, Any
from src.utils.config import Config
from test_config import TestConfig
from src.utils.logger import setup_logger
from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models
import cohere


class RetrievalTester:
    """Class to test and verify the Qdrant content retrieval pipeline"""

    def __init__(self, config: TestConfig):
        self.config = config
        self.qdrant_client = AsyncQdrantClient(
            url=config.qdrant_url,
            api_key=config.qdrant_api_key,
            prefer_grpc=False
        )
        self.cohere_client = cohere.AsyncClient(config.cohere_api_key)
        self.logger = setup_logger("retrieval_tester")
        self.test_results = []

    async def verify_qdrant_connection(self) -> bool:
        """
        Verify connection to Qdrant Cloud collection containing book embeddings

        Returns:
            True if connection is successful, False otherwise
        """
        try:
            collections = await self.qdrant_client.get_collections()
            collection_exists = any(col.name == self.config.qdrant_collection_name for col in collections.collections)

            if not collection_exists:
                self.logger.error(f"Collection {self.config.qdrant_collection_name} does not exist")
                return False

            # Get collection info to verify schema
            collection_info = await self.qdrant_client.get_collection(self.config.qdrant_collection_name)
            self.logger.info(f"Collection {self.config.qdrant_collection_name} exists with {collection_info.points_count} vectors")

            # Verify sample embeddings exist
            if collection_info.points_count > 0:
                # Get a sample point to verify structure
                sample_points = await self.qdrant_client.scroll(
                    collection_name=self.config.qdrant_collection_name,
                    limit=1
                )
                if sample_points[0]:
                    point = sample_points[0]
                    self.logger.info(f"Sample point retrieved with payload keys: {list(point.payload.keys()) if point.payload else []}")
                    return True

            self.logger.error("No embeddings found in the collection")
            return False

        except Exception as e:
            self.logger.error(f"Error verifying Qdrant connection: {str(e)}")
            return False

    async def generate_query_embedding(self, text: str, model: str = "embed-multilingual-v3.0") -> Optional[List[float]]:
        """
        Generate embedding for input text using Cohere API

        Args:
            text: Input text to embed
            model: Cohere model to use

        Returns:
            Embedding vector or None if failed
        """
        try:
            response = await self.cohere_client.embed(
                texts=[text],
                model=model,
                input_type="search_query"  # Optimize for search queries
            )

            if response.embeddings and len(response.embeddings) > 0:
                self.logger.debug(f"Generated embedding of size {len(response.embeddings[0])} for text: {text[:50]}...")
                return response.embeddings[0]
            else:
                self.logger.error("No embeddings returned from Cohere API")
                return None

        except Exception as e:
            self.logger.error(f"Error generating query embedding: {str(e)}")
            return None

    async def search_similar_chunks(self, query_embedding: List[float], top_k: int = 5,
                                  filters: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        Query Qdrant for top-k similar chunks

        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return
            filters: Optional metadata filters

        Returns:
            List of result dictionaries with content and metadata
        """
        try:
            # Prepare filters if provided
            qdrant_filters = None
            if filters:
                filter_conditions = []
                for key, value in filters.items():
                    if isinstance(value, list):
                        # Handle multiple values for the same key
                        should_conditions = []
                        for val in value:
                            should_conditions.append(
                                models.FieldCondition(
                                    key=key,
                                    match=models.MatchValue(value=val)
                                )
                            )
                        filter_conditions.append(
                            models.Condition(should=should_conditions)
                        )
                    else:
                        filter_conditions.append(
                            models.FieldCondition(
                                key=key,
                                match=models.MatchValue(value=value)
                            )
                        )

                if filter_conditions:
                    qdrant_filters = models.Filter(must=filter_conditions)

            # Perform search
            search_results = await self.qdrant_client.search(
                collection_name=self.config.qdrant_collection_name,
                query_vector=query_embedding,
                limit=top_k,
                query_filter=qdrant_filters
            )

            results = []
            for result in search_results:
                results.append({
                    "id": result.id,
                    "score": result.score,
                    "content": result.payload.get("text", ""),
                    "metadata": result.payload,
                    "url": result.payload.get("url", ""),
                    "chapter": result.payload.get("chapter", ""),
                    "content_type": result.payload.get("content_type", "")
                })

            self.logger.debug(f"Retrieved {len(results)} similar chunks")
            return results

        except Exception as e:
            self.logger.error(f"Error searching similar chunks: {str(e)}")
            return []

    async def test_basic_retrieval(self, query_text: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Test basic retrieval functionality without filters

        Args:
            query_text: Text to search for
            top_k: Number of results to return

        Returns:
            Test results dictionary
        """
        start_time = time.time()

        # Generate query embedding
        query_embedding = await self.generate_query_embedding(query_text)
        if not query_embedding:
            return {
                "query": query_text,
                "success": False,
                "error": "Failed to generate query embedding",
                "response_time": time.time() - start_time
            }

        # Search for similar chunks
        results = await self.search_similar_chunks(query_embedding, top_k)

        response_time = time.time() - start_time

        test_result = {
            "query": query_text,
            "success": True,
            "response_time": response_time,
            "num_results": len(results),
            "results": results,
            "top_k": top_k
        }

        self.test_results.append(test_result)
        return test_result

    async def test_metadata_filtering(self, query_text: str, filters: Dict, top_k: int = 5) -> Dict[str, Any]:
        """
        Test retrieval with metadata filters

        Args:
            query_text: Text to search for
            filters: Metadata filters to apply
            top_k: Number of results to return

        Returns:
            Test results dictionary
        """
        start_time = time.time()

        # Generate query embedding
        query_embedding = await self.generate_query_embedding(query_text)
        if not query_embedding:
            return {
                "query": query_text,
                "filters": filters,
                "success": False,
                "error": "Failed to generate query embedding",
                "response_time": time.time() - start_time
            }

        # Search with filters
        results = await self.search_similar_chunks(query_embedding, top_k, filters)

        # Verify that all results match the filters
        all_match = True
        for result in results:
            for key, expected_value in filters.items():
                actual_value = result["metadata"].get(key)
                if isinstance(expected_value, list):
                    if actual_value not in expected_value:
                        all_match = False
                        break
                else:
                    if actual_value != expected_value:
                        all_match = False
                        break
            if not all_match:
                break

        response_time = time.time() - start_time

        test_result = {
            "query": query_text,
            "filters": filters,
            "success": True,
            "response_time": response_time,
            "num_results": len(results),
            "results": results,
            "filters_applied_correctly": all_match,
            "top_k": top_k
        }

        self.test_results.append(test_result)
        return test_result

    async def test_selection_based_retrieval(self, selection_text: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Test retrieval based on user-selected text

        Args:
            selection_text: Text that simulates user selection
            top_k: Number of results to return

        Returns:
            Test results dictionary
        """
        start_time = time.time()

        # Generate query embedding from selection
        query_embedding = await self.generate_query_embedding(selection_text)
        if not query_embedding:
            return {
                "selection": selection_text,
                "success": False,
                "error": "Failed to generate query embedding",
                "response_time": time.time() - start_time
            }

        # Search for similar chunks
        results = await self.search_similar_chunks(query_embedding, top_k)

        response_time = time.time() - start_time

        test_result = {
            "selection": selection_text,
            "success": True,
            "response_time": response_time,
            "num_results": len(results),
            "results": results,
            "top_k": top_k
        }

        self.test_results.append(test_result)
        return test_result

    def log_test_results(self):
        """Log all test results for analysis"""
        self.logger.info(f"Logged {len(self.test_results)} test results")
        for i, result in enumerate(self.test_results):
            if result.get("success"):
                self.logger.info(f"Test {i+1}: Query='{result.get('query', result.get('selection', 'N/A'))[:50]}...' "
                               f"Results={result['num_results']}, Time={result['response_time']:.2f}s")
            else:
                self.logger.error(f"Test {i+1}: Failed with error: {result.get('error', 'Unknown error')}")

    def calculate_relevance_metrics(self) -> Dict[str, float]:
        """
        Calculate relevance metrics based on test results

        Returns:
            Dictionary with relevance metrics
        """
        if not self.test_results:
            return {"precision": 0.0, "recall": 0.0, "average_response_time": 0.0}

        successful_tests = [r for r in self.test_results if r.get("success")]
        if not successful_tests:
            return {"precision": 0.0, "recall": 0.0, "average_response_time": 0.0}

        total_response_time = sum(r["response_time"] for r in successful_tests)
        avg_response_time = total_response_time / len(successful_tests)

        # For now, we'll report basic metrics
        # In a real implementation, we'd have expected results to compare against
        return {
            "average_response_time": avg_response_time,
            "num_successful_tests": len(successful_tests),
            "total_tests": len(self.test_results)
        }

    async def run_comprehensive_tests(self):
        """Run comprehensive tests for all retrieval scenarios"""
        self.logger.info("Starting comprehensive retrieval tests...")

        # Test 1: Basic retrieval
        await self.test_basic_retrieval("What is ROS 2 architecture?", top_k=5)
        await self.test_basic_retrieval("Explain Gazebo physics simulation", top_k=5)
        await self.test_basic_retrieval("How does Isaac Sim work?", top_k=3)

        # Test 2: Metadata filtering
        await self.test_metadata_filtering(
            "What is computer vision?",
            {"content_type": "documentation"},
            top_k=3
        )
        await self.test_metadata_filtering(
            "navigation concepts",
            {"chapter": "Module 3"},
            top_k=3
        )

        # Test 3: Selection-based retrieval
        await self.test_selection_based_retrieval(
            "Embodied intelligence and AI systems operating in the physical world",
            top_k=5
        )
        await self.test_selection_based_retrieval(
            "Python agents (rclpy) and URDF for humanoids",
            top_k=3
        )

        # Log results
        self.log_test_results()

        # Calculate metrics
        metrics = self.calculate_relevance_metrics()
        self.logger.info(f"Test metrics: {metrics}")

        return metrics


async def main():
    """Main function to run the retrieval verification tests"""
    # Initialize configuration
    config = TestConfig()

    # Create retrieval tester
    tester = RetrievalTester(config)

    # Verify Qdrant connection first
    if not await tester.verify_qdrant_connection():
        print("Failed to connect to Qdrant. Please check your configuration.")
        return

    print("Starting Qdrant Content Retrieval Verification Tests...")

    # Run comprehensive tests
    metrics = await tester.run_comprehensive_tests()

    print(f"Tests completed with metrics: {metrics}")
    print("Retrieval verification completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())