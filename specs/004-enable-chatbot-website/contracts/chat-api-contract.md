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
  "query": "string, the user's question about the book content"
}
```

#### Example Request
```json
{
  "query": "What are the main concepts of Physical AI?"
}
```

### Response
#### Success Response (200 OK)
```json
{
  "answer": "string, the response generated from the book content"
}
```

#### Example Success Response
```json
{
  "answer": "Physical AI combines robotics, machine learning, and physics to create intelligent systems that operate in the real world..."
}
```

#### Error Response (500 Internal Server Error)
```json
{
  "answer": "Sorry, I encountered an error while processing your query. Please try again."
}
```

### Implementation Notes
- The endpoint should use the existing ChatManager with the ingested books Qdrant collection
- Responses should be generated using retrieval-augmented generation (RAG) from the book content
- The endpoint should log errors without disrupting other operations
- Response time should be within 10 seconds for 95% of queries