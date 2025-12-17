# Specification: Physical AI Book Website Content Ingestion System

## 1. Overview

### 1.1 Purpose
This specification defines a system for ingesting content from the Physical AI Book website (Docusaurus-based), generating semantic embeddings using Cohere, and storing the vectorized content in Qdrant Cloud for retrieval-augmented generation (RAG) applications.

### 1.2 Scope
- Crawling the Physical AI Book website to extract content
- Processing and cleaning extracted content
- Chunking content with relevant metadata
- Generating embeddings using Cohere's embedding models
- Storing vectors in Qdrant Cloud Free Tier
- Providing search capabilities over the content

### 1.3 Success Criteria
- All website pages crawled and content extracted
- Clean, well-structured text chunks with metadata preserved
- Embeddings generated successfully with high quality
- Vectors stored efficiently in Qdrant Cloud
- Search functionality working properly
- System operates within Qdrant Cloud Free Tier limits

## 2. Functional Requirements

### 2.1 Content Crawling
- **REQ-CRAWL-001**: System shall crawl all pages of the Physical AI Book website
- **REQ-CRAWL-002**: System shall respect robots.txt and crawl delays
- **REQ-CRAWL-003**: System shall handle dynamic content and client-side rendering
- **REQ-CRAWL-004**: System shall identify and prioritize content-rich pages over navigation pages
- **REQ-CRAWL-005**: System shall track and report crawl statistics (pages processed, errors, etc.)

### 2.2 Content Extraction and Cleaning
- **REQ-EXTRACT-001**: System shall extract main content from HTML, excluding navigation and boilerplate
- **REQ-EXTRACT-002**: System shall preserve document hierarchy and structural elements
- **REQ-EXTRACT-003**: System shall clean content by removing HTML tags while preserving meaningful formatting
- **REQ-EXTRACT-004**: System shall extract and preserve metadata (title, headings, document structure)
- **REQ-EXTRACT-005**: System shall handle different content formats (text, code blocks, lists, tables)

### 2.3 Content Chunking
- **REQ-CHUNK-001**: System shall split content into semantically coherent chunks
- **REQ-CHUNK-002**: System shall maintain context between chunks (overlap when necessary)
- **REQ-CHUNK-003**: System shall preserve document hierarchy in chunk metadata
- **REQ-CHUNK-004**: System shall respect paragraph and section boundaries when chunking
- **REQ-CHUNK-005**: System shall store chunk-specific metadata (URL, heading, page context)

### 2.4 Embedding Generation
- **REQ-EMBED-001**: System shall generate embeddings using Cohere's embedding model
- **REQ-EMBED-002**: System shall handle rate limiting and API quotas appropriately
- **REQ-EMBED-003**: System shall cache embeddings to avoid redundant API calls
- **REQ-EMBED-004**: System shall handle embedding errors gracefully with retry logic
- **REQ-EMBED-005**: System shall support batch processing for efficiency

### 2.5 Vector Storage
- **REQ-STORAGE-001**: System shall store vectors in Qdrant Cloud
- **REQ-STORAGE-002**: System shall create appropriate collection schema with metadata fields
- **REQ-STORAGE-003**: System shall index vectors for efficient similarity search
- **REQ-STORAGE-004**: System shall handle storage limits of Qdrant Cloud Free Tier
- **REQ-STORAGE-005**: System shall maintain data integrity during storage operations

### 2.6 Search Functionality
- **REQ-SEARCH-001**: System shall provide semantic search over stored content
- **REQ-SEARCH-002**: System shall return relevant results with confidence scores
- **REQ-SEARCH-003**: System shall support filtering by metadata (document type, section, etc.)
- **REQ-SEARCH-004**: System shall return original content context with results
- **REQ-SEARCH-005**: System shall support configurable result count and relevance threshold

## 3. Technical Requirements

### 3.1 Performance Requirements
- **PERF-001**: Content extraction should process 100 pages within 10 minutes
- **PERF-002**: Embedding generation should process 1000 chunks within 30 minutes
- **PERF-003**: Search response time should be under 500ms for 95% of queries
- **PERF-004**: System should handle concurrent requests without degradation

### 3.2 Scalability Requirements
- **SCALE-001**: System should handle up to 10,000 content chunks within Qdrant Free Tier limits
- **SCALE-002**: System should support incremental updates as content changes
- **SCALE-003**: System should handle content growth of 20% monthly

### 3.3 Security Requirements
- **SEC-001**: API keys and credentials must be securely stored (environment variables)
- **SEC-002**: No sensitive data should be stored in plain text
- **SEC-003**: Connection to Qdrant Cloud must use encrypted channels
- **SEC-004**: System should validate all inputs to prevent injection attacks

### 3.4 Reliability Requirements
- **RELIABLE-001**: System should have 99% uptime for search functionality
- **RELIABLE-002**: Failed operations should have appropriate retry mechanisms
- **RELIABLE-003**: System should maintain consistent state during partial failures
- **RELIABLE-004**: Backup and recovery procedures should be documented

## 4. Architecture Components

### 4.1 Web Crawler
- Discovers and extracts content from the Physical AI Book website
- Handles navigation structure and follows internal links
- Respects rate limits and robots.txt policies
- Extracts content while preserving document hierarchy

### 4.2 Content Processor
- Cleans and structures extracted content
- Removes boilerplate HTML while preserving semantic meaning
- Identifies and preserves important metadata (headings, sections, etc.)

### 4.3 Content Chunker
- Splits content into appropriately sized chunks
- Maintains context between related content
- Adds metadata to each chunk (source URL, document structure, etc.)

### 4.4 Embedding Generator
- Uses Cohere API to generate semantic embeddings
- Implements caching to minimize API calls
- Handles rate limiting and error conditions
- Batch processes embeddings for efficiency

### 4.5 Vector Storage Manager
- Manages storage of vectors in Qdrant Cloud
- Creates and manages collections with appropriate schema
- Implements indexing for efficient search
- Monitors and enforces storage limits

### 4.6 Search Interface
- Provides semantic search over stored content
- Accepts natural language queries
- Returns relevant results with confidence scores
- Supports metadata filtering and result customization

## 5. Data Model

### 5.1 Content Chunk Schema
```
{
  "id": "unique_chunk_identifier",
  "vector": [float_vector],  // Cohere embedding vector
  "payload": {
    "content": "cleaned_content_text",
    "url": "original_page_url",
    "title": "page_title",
    "heading": "section_heading_if_applicable",
    "hierarchy": ["level1", "level2", "level3"],  // Document hierarchy
    "chunk_index": integer,  // Position of chunk in document
    "total_chunks": integer,  // Total chunks in document
    "metadata": {
      "word_count": integer,
      "language": "en",
      "created_at": "timestamp",
      "updated_at": "timestamp"
    }
  }
}
```

### 5.2 Metadata Fields
- **URL**: Original source URL of the content
- **Title**: Page title from HTML head or Docusaurus metadata
- **Heading**: Specific heading associated with this chunk
- **Hierarchy**: Document structure path (e.g., ["Module 1", "Chapter 2"])
- **Content Type**: Type of content (text, code, list, etc.)

## 6. Implementation Constraints

### 6.1 Qdrant Cloud Free Tier Limitations
- Maximum 100K vectors
- Maximum 2GB storage
- Limited to 1 collection
- Rate limits apply

### 6.2 Cohere API Limits
- Rate limits depending on account type
- Monthly token usage limits
- Need to implement proper error handling and retries

### 6.3 Docusaurus Site Structure
- Static site generation with predictable URL patterns
- Content organized in modules and chapters
- Rich Markdown content with special formatting

## 7. Acceptance Criteria

### 7.1 Crawling Verification
- [ ] All pages from the Physical AI Book website successfully crawled
- [ ] Content extraction accuracy rate > 95%
- [ ] Proper handling of navigation and content elements

### 7.2 Processing Verification
- [ ] Content cleaned and structured appropriately
- [ ] Metadata preserved and accessible
- [ ] Chunks created with appropriate size and context

### 7.3 Embedding Verification
- [ ] All chunks successfully embedded using Cohere
- [ ] Embeddings stored without corruption
- [ ] Proper handling of API rate limits and errors

### 7.4 Storage Verification
- [ ] Vectors stored in Qdrant Cloud collection
- [ ] Collection schema properly configured
- [ ] Storage limits respected

### 7.5 Search Verification
- [ ] Semantic search returns relevant results
- [ ] Response times meet performance requirements
- [ ] Metadata filtering works correctly

## 8. Risk Assessment

### 8.1 High-Risk Items
- **API Quotas**: Cohere and Qdrant rate limits could impact processing speed
- **Storage Limits**: Qdrant Cloud Free Tier may not accommodate all content
- **Content Changes**: Website updates could break crawling logic

### 8.2 Mitigation Strategies
- Implement robust error handling and retry logic
- Design system to work within tier limitations
- Create monitoring for API usage and storage consumption
- Plan for graceful degradation when limits reached

## 9. Success Metrics

### 9.1 Performance Metrics
- Crawl completion time
- Embedding generation throughput
- Search query response time
- Accuracy of search results

### 9.2 Quality Metrics
- Content extraction accuracy
- Chunk coherence and context preservation
- Embedding quality and relevance
- User satisfaction with search results

## 10. Dependencies

### 10.1 External Services
- Cohere API for embeddings
- Qdrant Cloud for vector storage
- Physical AI Book website (source)

### 10.2 Libraries and Frameworks
- Web scraping library (BeautifulSoup, Scrapy, or Playwright)
- Cohere Python SDK
- Qdrant Python client
- Configuration management library

### 10.3 Infrastructure
- Environment variables for API keys
- Network connectivity to external services
- Sufficient compute resources for processing