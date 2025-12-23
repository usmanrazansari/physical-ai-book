# Chat API Contract

## Overview
This document specifies the contract for the chat endpoint that enables communication between the frontend chat interface and the backend RAG system.

## Endpoint: POST /chat

### Request
- **URL**: `/chat`
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

### Implementation Notes
- The backend should handle connection timeouts gracefully
- Responses should be returned within 30 seconds
- The endpoint should be resilient to temporary backend service unavailability