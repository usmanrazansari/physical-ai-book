# RAG Chatbot Backend Verification Script

This script verifies that your RAG chatbot backend is working correctly before pushing to GitHub.

## Purpose

The script performs the following checks:
1. Verifies connection to Qdrant and checks that the collection exists
2. Tests retrieval from Qdrant with sample queries
3. Checks that the FastAPI backend is responding
4. Tests the `/ask` endpoint with a simple query
5. Tests selection-based queries with context

## Requirements

- Python 3.14 or higher
- Required packages: `requests`, `qdrant-client`, `openai`

## Installation

```bash
pip install requests qdrant-client openai
```

## Configuration

Before running the script, you need to configure your API keys and connection details. You can do this in two ways:

### Option 1: Environment Variables
Set the following environment variables:

```bash
export QDRANT_URL="your-qdrant-cluster-url"
export QDRANT_API_KEY="your-qdrant-api-key"
export QDRANT_COLLECTION_NAME="your-collection-name"
export BACKEND_URL="http://localhost:8000"  # or your backend URL
export OPENAI_API_KEY="your-openai-api-key-if-needed"  # optional
```

### Option 2: Update the Script
Edit the `CONFIG` dictionary in the script to include your actual values:

```python
CONFIG = {
    # Qdrant Configuration
    "qdrant_url": "your-qdrant-cluster-url.here",
    "qdrant_api_key": "your-qdrant-api-key",
    "collection_name": "your-collection-name",

    # FastAPI Backend Configuration
    "backend_url": "http://localhost:8000",

    # OpenAI Configuration (optional)
    "openai_api_key": "your-openai-api-key-if-needed",

    # Test Configuration
    "test_query": "What is ROS 2 architecture?",
    "test_selection": "Python agents (rclpy) and URDF for humanoids",
    "test_query_with_context": "Explain more about this topic",
}
```

## Usage

Run the script from the command line:

```bash
python verify_rag_backend.py
```

The script will run through all verification tests and provide a clear pass/fail report for each test, followed by an overall summary.

## Expected Output

When all tests pass, you'll see output like:

```
============================================================
RAG Chatbot Backend Verification
============================================================
Testing backend at: http://localhost:8000
Testing Qdrant collection: physical_ai_book_content
Test query: 'What is ROS 2 architecture?'
Test selection: 'Python agents (rclpy) and URDF for humanoids'
------------------------------------------------------------
Testing Qdrant connection...
✅ PASS: Qdrant collection exists with 1234 vectors
Testing Qdrant retrieval...
✅ PASS: Retrieved sample point with payload keys: ['text', 'url', 'chapter', 'content_type']
Testing backend health...
✅ PASS: Backend is responding
Testing /ask endpoint...
✅ PASS: /ask endpoint returned response of 245 characters
Testing selection-based query...
✅ PASS: Selection-based query returned response of 189 characters
------------------------------------------------------------
VERIFICATION SUMMARY
------------------------------------------------------------
✅ PASS: Qdrant Connection
✅ PASS: Qdrant Retrieval
✅ PASS: Backend Health
✅ PASS: Ask Endpoint
✅ PASS: Selection Query
------------------------------------------------------------
Overall: 5/5 tests passed
🎉 ALL TESTS PASSED! Your RAG backend is ready for GitHub.
```

## Troubleshooting

- If Qdrant tests fail, verify your URL, API key, and collection name
- If backend tests fail, ensure your FastAPI server is running
- If selection-based queries fail, verify that your backend supports the context parameter
- Check that your environment variables are properly set if using that method