# Qdrant Content Retrieval Verification System

This system tests and validates the retrieval pipeline using stored embeddings in Qdrant to support a future RAG chatbot for the Physical AI Book.

## Overview

The retrieval verification system implements the complete pipeline for testing Qdrant-based content retrieval as outlined in the implementation plan. It includes:

- Connection verification to Qdrant Cloud
- Query embedding generation using Cohere
- Similarity search with metadata filtering
- Selection-based retrieval simulation
- Comprehensive verification and logging

## Setup

1. Ensure you have the backend environment set up from the ingestion system
2. Install required dependencies:
   ```bash
   cd backend
   source .venv/Scripts/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configure your environment variables in a `.env` file:
   ```bash
   cp .env.example .env
   # Edit .env with your Qdrant and Cohere credentials
   ```

## Configuration

The system uses the same configuration as the ingestion system but with additional test-specific settings:

- `TEST_TOP_K`: Number of results to retrieve (default: 5)
- `TEST_QUERY_TIMEOUT`: Query timeout in seconds (default: 30)
- `MIN_RELEVANCE_SCORE`: Minimum score for relevance (default: 0.3)
- `MAX_RESPONSE_TIME`: Maximum allowed response time (default: 2.0)

## Usage

Run the verification system:

```bash
python retrieval_verification.py
```

This will execute all verification tests and generate a report.

## Test Components

### 1. Basic Retrieval Tests
- Tests similarity search with various query types
- Validates embedding generation and matching
- Measures response times and result relevance

### 2. Metadata Filtering Tests
- Tests filtering by chapter, URL, content type, etc.
- Verifies filter application accuracy
- Tests complex filter combinations

### 3. Selection-Based Retrieval Tests
- Simulates user text selection scenarios
- Validates context matching between selection and results
- Tests different selection lengths

### 4. Verification Tests
- Connection verification to Qdrant
- Metadata accuracy validation
- Reproducibility testing
- Performance metrics collection

## Output

The system generates:
- Console output with test results and metrics
- A JSON report file (`verification_report.json`) with detailed results
- Log entries for debugging and analysis

## Success Criteria

The verification system checks for:
- At least 85% retrieval accuracy for top-k results
- 100% metadata accuracy for source attribution
- Query response time under 2 seconds for 95% of queries
- System reproducibility with consistent results across identical queries

## Integration with Existing System

This verification system integrates with the existing Physical AI Book ingestion pipeline:
- Uses the same Qdrant collection and Cohere API
- Compatible with the embedding format and metadata structure
- Extends the existing configuration system