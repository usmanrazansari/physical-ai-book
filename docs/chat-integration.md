---
sidebar_position: 999
---

# Chat Interface Integration

Learn how to integrate the RAG chatbot interface into the Physical AI Book website.

## Overview

The chat interface provides users with an AI assistant that can answer questions about the book content. The interface includes:

- A chat window with message history
- Input field for asking questions
- Text selection functionality for contextual queries
- Source attribution for AI responses

## Features

### Text Selection
Users can select text on any page and ask questions about it. The selected text will be sent as context to the AI assistant.

### Source Attribution
AI responses include links to the source material in the book, allowing users to verify information.

### Responsive Design
The chat interface works on all device sizes, with a floating widget on mobile devices.

## Integration

The chat interface is automatically added to all pages through a theme override. The widget appears as a floating button in the bottom-right corner of the screen.

## Configuration

To configure the backend URL, set the `BACKEND_URL` environment variable:

```bash
BACKEND_URL=https://your-backend-url.com
```

## API Requirements

The chat interface communicates with a FastAPI backend that must provide:

- A POST endpoint at `/ask` that accepts JSON with `query` and optional `context` fields
- Responses should include the answer and optional metadata about sources

## Customization

To customize the chat interface appearance, modify the CSS files in `src/components/ChatInterface/ChatInterface.css`.

To change the position or behavior of the chat widget, modify `src/plugins/ChatWidget.js` and `src/plugins/ChatWidget.css`.