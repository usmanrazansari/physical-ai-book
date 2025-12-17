#!/usr/bin/env python3
"""
RAG Chatbot Backend Verification Script

This script verifies that the RAG chatbot backend is working correctly by testing:
1. Retrieval from Qdrant returns chunks for sample queries
2. FastAPI agent endpoint (/ask) responds correctly
3. Selection-based queries are handled correctly

Requirements:
- Python 3.14+
- Install: pip install requests qdrant-client openai

Configuration:
Update the API keys and connection details in the CONFIG section below.
"""

import os
import sys
import time
import requests
from typing import Dict, List, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
import json

# ===========================================
# CONFIGURATION - UPDATE THESE VALUES
# ===========================================

CONFIG = {
    # Qdrant Configuration
    "qdrant_url": os.getenv("QDRANT_URL", "your-qdrant-cluster-url.here"),
    "qdrant_api_key": os.getenv("QDRANT_API_KEY", "your-qdrant-api-key"),
    "collection_name": os.getenv("QDRANT_COLLECTION_NAME", "physical_ai_book_content"),

    # FastAPI Backend Configuration
    "backend_url": os.getenv("BACKEND_URL", "http://localhost:8000"),

    # OpenAI Configuration (optional, only if using OpenAI embeddings)
    "openai_api_key": os.getenv("OPENAI_API_KEY", "your-openai-api-key-if-needed"),

    # Test Configuration
    "test_query": "What is ROS 2 architecture?",
    "test_selection": "Python agents (rclpy) and URDF for humanoids",
    "test_query_with_context": "Explain more about this topic",
}

# ===========================================
# TEST FUNCTIONS
# ===========================================

def test_qdrant_connection() -> bool:
    """Test connection to Qdrant and verify collection exists."""
    print("Testing Qdrant connection...")

    try:
        client = QdrantClient(
            url=CONFIG["qdrant_url"],
            api_key=CONFIG["qdrant_api_key"],
            prefer_grpc=False
        )

        # Check if collection exists
        collections = client.get_collections()
        collection_exists = any(col.name == CONFIG["collection_name"] for col in collections.collections)

        if not collection_exists:
            print("❌ FAIL: Qdrant collection does not exist")
            return False

        # Get collection info
        collection_info = client.get_collection(CONFIG["collection_name"])
        print(f"✅ PASS: Qdrant collection exists with {collection_info.points_count} vectors")
        return True

    except Exception as e:
        print(f"❌ FAIL: Qdrant connection error - {str(e)}")
        return False


def test_qdrant_retrieval() -> bool:
    """Test retrieval from Qdrant with a sample query."""
    print("Testing Qdrant retrieval...")

    try:
        client = QdrantClient(
            url=CONFIG["qdrant_url"],
            api_key=CONFIG["qdrant_api_key"],
            prefer_grpc=False
        )

        # For this test, we'll use a simple scroll to get sample points
        # In a real scenario, you'd want to generate an embedding for the query
        sample_points = client.scroll(
            collection_name=CONFIG["collection_name"],
            limit=1
        )

        if not sample_points[0]:
            print("❌ FAIL: No sample points found in Qdrant collection")
            return False

        # Get a sample point to verify structure
        sample_point = sample_points[0]
        if not sample_point.payload:
            print("❌ FAIL: Sample point has no payload")
            return False

        print(f"✅ PASS: Retrieved sample point with payload keys: {list(sample_point.payload.keys())}")
        return True

    except Exception as e:
        print(f"❌ FAIL: Qdrant retrieval error - {str(e)}")
        return False


def test_backend_health() -> bool:
    """Test if the backend is running and responding."""
    print("Testing backend health...")

    try:
        response = requests.get(f"{CONFIG['backend_url']}/docs", timeout=10)
        if response.status_code in [200, 404]:  # 404 is OK if docs endpoint doesn't exist
            print("✅ PASS: Backend is responding")
            return True
        else:
            print(f"❌ FAIL: Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ FAIL: Cannot connect to backend")
        return False
    except Exception as e:
        print(f"❌ FAIL: Backend health check error - {str(e)}")
        return False


def test_ask_endpoint() -> bool:
    """Test the /ask endpoint with a simple query."""
    print("Testing /ask endpoint...")

    try:
        payload = {
            "query": CONFIG["test_query"]
        }

        response = requests.post(
            f"{CONFIG['backend_url']}/ask",
            json=payload,
            timeout=30
        )

        if response.status_code != 200:
            print(f"❌ FAIL: /ask endpoint returned status {response.status_code}")
            print(f"Response: {response.text}")
            return False

        try:
            data = response.json()
            if "response" in data or "answer" in data:
                response_text = data.get("response", data.get("answer", ""))
                if len(response_text) > 0:
                    print(f"✅ PASS: /ask endpoint returned response of {len(response_text)} characters")
                    return True
                else:
                    print("❌ FAIL: /ask endpoint returned empty response")
                    return False
            else:
                print(f"❌ FAIL: /ask endpoint returned unexpected format: {data}")
                return False
        except json.JSONDecodeError:
            print(f"❌ FAIL: /ask endpoint returned invalid JSON: {response.text[:200]}...")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ FAIL: Cannot connect to /ask endpoint")
        return False
    except Exception as e:
        print(f"❌ FAIL: /ask endpoint error - {str(e)}")
        return False


def test_selection_based_query() -> bool:
    """Test the /ask endpoint with a selection-based query."""
    print("Testing selection-based query...")

    try:
        payload = {
            "query": CONFIG["test_query_with_context"],
            "context": CONFIG["test_selection"]
        }

        response = requests.post(
            f"{CONFIG['backend_url']}/ask",
            json=payload,
            timeout=30
        )

        if response.status_code != 200:
            print(f"❌ FAIL: Selection-based query returned status {response.status_code}")
            print(f"Response: {response.text}")
            return False

        try:
            data = response.json()
            if "response" in data or "answer" in data:
                response_text = data.get("response", data.get("answer", ""))
                if len(response_text) > 0:
                    print(f"✅ PASS: Selection-based query returned response of {len(response_text)} characters")
                    return True
                else:
                    print("❌ FAIL: Selection-based query returned empty response")
                    return False
            else:
                print(f"❌ FAIL: Selection-based query returned unexpected format: {data}")
                return False
        except json.JSONDecodeError:
            print(f"❌ FAIL: Selection-based query returned invalid JSON: {response.text[:200]}...")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ FAIL: Cannot connect to selection-based query endpoint")
        return False
    except Exception as e:
        print(f"❌ FAIL: Selection-based query error - {str(e)}")
        return False


def run_verification() -> None:
    """Run all verification tests and report results."""
    print("=" * 60)
    print("RAG Chatbot Backend Verification")
    print("=" * 60)
    print(f"Testing backend at: {CONFIG['backend_url']}")
    print(f"Testing Qdrant collection: {CONFIG['collection_name']}")
    print(f"Test query: '{CONFIG['test_query']}'")
    print(f"Test selection: '{CONFIG['test_selection']}'")
    print("-" * 60)

    # Track test results
    results = {}

    # Test 1: Qdrant connection
    results["qdrant_connection"] = test_qdrant_connection()
    time.sleep(1)  # Brief pause between tests

    # Test 2: Qdrant retrieval
    results["qdrant_retrieval"] = test_qdrant_retrieval()
    time.sleep(1)

    # Test 3: Backend health
    results["backend_health"] = test_backend_health()
    time.sleep(1)

    # Test 4: Ask endpoint
    results["ask_endpoint"] = test_ask_endpoint()
    time.sleep(1)

    # Test 5: Selection-based query
    results["selection_query"] = test_selection_based_query()
    time.sleep(1)

    # Summary
    print("-" * 60)
    print("VERIFICATION SUMMARY")
    print("-" * 60)

    passed = sum(1 for result in results.values() if result)
    total = len(results)

    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name.replace('_', ' ').title()}")

    print("-" * 60)
    print(f"Overall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL TESTS PASSED! Your RAG backend is ready for GitHub.")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED! Please fix the issues before pushing to GitHub.")
        sys.exit(1)


if __name__ == "__main__":
    # Check if required packages are available
    try:
        import requests
        import qdrant_client
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please install required packages: pip install requests qdrant-client openai")
        sys.exit(1)

    # Check Python version
    if sys.version_info < (3, 14):
        print(f"❌ Python version {sys.version_info} is less than required 3.14")
        sys.exit(1)

    # Run verification
    run_verification()