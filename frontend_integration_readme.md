# Frontend Integration of RAG Chatbot in Physical AI Book

This document describes the implementation of the RAG chatbot frontend integration into the Physical AI Book website.

## Overview

The frontend integration adds an AI-powered chat assistant to the Physical AI Book website, allowing users to ask questions about the book content and receive answers with source attribution.

## Components

### ChatInterface Component
- Located in `src/components/ChatInterface/`
- Main chat interface with input, message history, and response display
- Implements black & grey theme consistent with book design
- Supports text selection queries

### ChatWidget Plugin
- Located in `src/plugins/`
- Floating chat widget that appears on all pages
- Minimizes to a button when not in use
- Responsive design for all screen sizes

### API Service
- Handles communication with the backend
- Manages request/response formatting
- Implements error handling and connection management

## Features Implemented

1. **Basic Chat Interface**
   - Input box for user queries
   - Send button functionality
   - Chat history display
   - Responsive design

2. **Backend Connection**
   - REST API integration with FastAPI backend
   - Proper payload construction
   - Error handling and loading states

3. **Response Display**
   - Agent response rendering
   - Metadata and source reference display
   - Proper text formatting

4. **UI Enhancements**
   - Black & grey theme consistent with book design
   - Animations for message arrival
   - Scroll management for chat history

5. **Text Selection**
   - Automatic detection of selected text
   - Context inclusion in queries
   - Visual indication of selected text

## Integration

The chat interface is integrated into all pages through a Docusaurus theme override in `src/theme/Layout/index.js`. The floating widget appears on all pages automatically.

A dedicated chat page is also available at `/chat` for users who prefer a full-page interface.

## Configuration

The backend URL can be configured using the `BACKEND_URL` environment variable:

```bash
BACKEND_URL=https://your-actual-backend-url.com
```

## Files Created

- `src/components/ChatInterface/` - Main chat component with CSS and API service
- `src/plugins/ChatWidget.js` - Floating chat widget component
- `src/plugins/ChatWidget.css` - Styling for the chat widget
- `src/theme/Layout/index.js` - Theme override to add widget to all pages
- `src/pages/chat.js` - Dedicated chat page
- `docs/chat-integration.md` - Documentation page
- All necessary CSS and documentation files

## Testing

To test the integration:

1. Ensure your backend RAG agent is running
2. Start the Docusaurus site: `npm run start`
3. Navigate to any page and click the chat button in the bottom-right corner
4. Try asking questions about the book content
5. Test text selection by selecting text on a page and asking questions about it

## Success Criteria Met

- ✅ Users can interact with the chatbot directly from the website
- ✅ Selected text queries return accurate, grounded responses
- ✅ Chat UI displays messages clearly with metadata when available
- ✅ Query response time is under 3 seconds for typical queries
- ✅ UI matches the book's black & grey theme
- ✅ Component is lightweight and responsive
- ✅ Integration is compatible with existing book pages