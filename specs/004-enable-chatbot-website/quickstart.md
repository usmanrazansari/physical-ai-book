# Quickstart: Enable Fully Functional Chatbot on Website

## Overview
This guide explains how to verify and configure the existing chatbot implementation on the Physical AI Book website.

## Implementation Steps

### 1. Backend Setup
- Ensure environment variables are set:
  - COHERE_API_KEY: Your Cohere API key
  - QDRANT_API_KEY: Your Qdrant API key
  - QDRANT_URL: Your Qdrant cluster URL
- Run the ingestion pipeline to populate Qdrant with book content:
  ```bash
  cd backend
  python main.py --mode full
  ```
- Start the backend server:
  ```bash
  uvicorn main:app --reload --host 0.0.0.0 --port 8000
  ```

### 2. Frontend Configuration
- Verify that the backend URL is properly configured in the frontend
- Check that the chat interface is properly integrated into the website layout
- Ensure error handling and connection status indicators are working

### 3. Testing the Integration
- Test the /chat endpoint directly with sample queries
- Verify that the frontend chat interface successfully communicates with the backend
- Test various query types to ensure responses are relevant to the book content
- Verify that error handling works properly when services are unavailable

## Running the Implementation

### Prerequisites
- Python 3.11+ for backend
- Node.js 18+ for frontend
- Docusaurus development environment
- Access to Cohere API and Qdrant vector database

### Setup
1. Navigate to the project root
2. Set up environment variables in a .env file
3. Install backend dependencies: `pip install -r requirements.txt`
4. Install frontend dependencies: `npm install`

### Starting the Services
1. Start the backend: `cd backend && uvicorn main:app --reload`
2. In a new terminal, start the frontend: `npm start`
3. The chat interface should be available on the website

## Testing the Chatbot
1. Submit sample queries about the book content
2. Verify that responses are relevant and pulled from the ingested content
3. Test error conditions to ensure graceful degradation
4. Verify that existing website functionality is not affected