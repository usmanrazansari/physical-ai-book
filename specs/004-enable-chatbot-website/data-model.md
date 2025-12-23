# Data Model: Enable Fully Functional Chatbot on Website

## Key Entities

### Chat Query
- **Name**: ChatQuery
- **Description**: User input sent to the backend for processing
- **Attributes**:
  - query: String (the user's question)
  - timestamp: DateTime (when the query was submitted)
  - context: String (optional context from selected text)

### Chat Response
- **Name**: ChatResponse
- **Description**: System output generated based on book collection and user query
- **Attributes**:
  - answer: String (the response to the user's query)
  - sources: Array (references to the book content that informed the response)
  - timestamp: DateTime (when the response was generated)

### Chat Session
- **Name**: ChatSession
- **Description**: User's interaction context with the chatbot during their visit
- **Attributes**:
  - sessionId: String (unique identifier for the session)
  - messages: Array (the conversation history)
  - startTime: DateTime (when the session started)
  - isActive: Boolean (whether the session is currently active)

### Backend Endpoint
- **Name**: BackendEndpoint
- **Description**: The /chat API endpoint that processes queries using ChatManager
- **Attributes**:
  - endpoint: String (the API endpoint URL)
  - method: String (HTTP method, e.g., POST)
  - requestFormat: Object (expected request structure)
  - responseFormat: Object (expected response structure)

### Frontend Interface
- **Name**: FrontendInterface
- **Description**: The UI component that allows users to interact with the chatbot
- **Attributes**:
  - inputField: String (the text input element)
  - sendButton: String (the button to submit queries)
  - chatWindow: String (the display area for conversation)
  - statusIndicator: String (shows connection status)

## Relationships
- ChatSession contains multiple ChatQuery and ChatResponse instances
- BackendEndpoint processes ChatQuery and generates ChatResponse
- FrontendInterface displays ChatSession conversation history
- ChatResponse includes sources that reference the book content in Qdrant

## State Transitions
- ChatSession: inactive → active (when user starts chatting)
- ChatSession: active → inactive (when session ends)
- BackendEndpoint: ready → processing (when handling a query)
- BackendEndpoint: processing → ready (when response is generated)
- FrontendInterface: idle → loading (when waiting for response)
- FrontendInterface: loading → response (when response is received)