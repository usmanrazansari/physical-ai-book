# Website API Contract

## Overview
This document specifies the contract for the Physical AI Book website, including the chat service integration and website functionality.

## Chat Service Endpoint: POST /chat

### Request
- **URL**: `/chat` (relative to backend URL)
- **Method**: POST
- **Content-Type**: `application/json`

#### Request Body
```json
{
  "query": "string, the user's question",
  "context": "string, optional context from selected text (optional)"
}
```

#### Example Request
```json
{
  "query": "What is the main concept of Physical AI?",
  "context": "Physical AI combines robotics, machine learning, and physics..."
}
```

### Response
#### Success Response (200 OK)
```json
{
  "answer": "string, the response from the RAG system"
}
```

#### Error Response (500 Internal Server Error)
```json
{
  "answer": "Sorry, I encountered an error while processing your query. Please try again."
}
```

## Health Check Endpoint: GET /health

### Request
- **URL**: `/health` (relative to backend URL)
- **Method**: GET

### Response
#### Success Response (200 OK)
```json
{
  "status": "healthy",
  "service": "Physical AI Book Ingestion Backend"
}
```

#### Error Response (500 Internal Server Error)
```json
{
  "status": "unhealthy"
}
```

## Implementation Notes
- The website should gracefully handle cases where the chat service is unavailable
- Backend URL should be configurable for different environments
- The website should provide appropriate feedback when services are not accessible