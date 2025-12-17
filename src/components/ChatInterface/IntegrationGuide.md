# Integration Guide: Chat Interface for Physical AI Book

This guide explains how to integrate the RAG chatbot interface into the Physical AI Book Docusaurus site.

## Integration Options

### Option 1: Sidebar Integration (Recommended)

1. Create a new page that includes the chat interface:

```jsx
// src/pages/chat.jsx
import React from 'react';
import Layout from '@theme/Layout';
import ChatInterface from '../components/ChatInterface/ChatInterface';

export default function ChatPage() {
  return (
    <Layout title="Book Assistant" description="Physical AI Book Assistant">
      <div style={{ padding: '20px', maxWidth: '900px', margin: '0 auto' }}>
        <h1>Physical AI Book Assistant</h1>
        <ChatInterface backendUrl={process.env.BACKEND_URL || 'http://localhost:8000'} />
      </div>
    </Layout>
  );
}
```

2. Add the page to your sidebar in `sidebars.js`:

```js
module.exports = {
  docs: [
    // ... your existing docs
    {
      type: 'category',
      label: 'Tools',
      items: [
        'chat',  // Add this line to reference the chat page
      ],
    },
  ],
};
```

### Option 2: Floating Chat Widget

1. Add the chat interface as a floating widget in your main layout by modifying the Docusaurus theme:

Create a new component `src/components/FloatingChat.jsx`:

```jsx
import React, { useState } from 'react';
import ChatInterface from './ChatInterface/ChatInterface';
import './FloatingChat.css';

const FloatingChat = ({ backendUrl }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      {!isOpen && (
        <button
          className="floating-chat-button"
          onClick={() => setIsOpen(true)}
        >
          💬
        </button>
      )}

      {isOpen && (
        <div className="floating-chat-container">
          <div className="floating-chat-header">
            <span>Book Assistant</span>
            <button
              className="close-button"
              onClick={() => setIsOpen(false)}
            >
              ×
            </button>
          </div>
          <div className="floating-chat-body">
            <ChatInterface backendUrl={backendUrl} />
          </div>
        </div>
      )}
    </>
  );
};

export default FloatingChat;
```

2. Add the widget to your main layout by creating a theme override in `src/theme/Layout/index.js`:

```jsx
import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import FloatingChat from '@site/src/components/FloatingChat';

export default function Layout(props) {
  return (
    <>
      <OriginalLayout {...props} />
      <FloatingChat backendUrl={process.env.BACKEND_URL || 'http://localhost:8000'} />
    </>
  );
}
```

## Environment Configuration

Add the backend URL to your Docusaurus configuration by adding it to your `.env` file:

```env
BACKEND_URL=https://your-actual-backend-url.com
```

## Styling Notes

The chat interface uses a black and grey theme that should match the book's design. The component is responsive and will adapt to different screen sizes.

## Backend API Requirements

The chat interface expects the following API endpoint:
- POST `/ask` - Accepts a JSON payload with `query` and optional `context` fields
- The backend should return a JSON response with at least an `answer` or `response` field

## Testing

To test the integration:

1. Make sure your backend is running and accessible
2. Start your Docusaurus site: `npm run start`
3. Navigate to the page where you've integrated the chat component
4. Try asking questions to ensure the backend communication is working
5. Test text selection functionality by selecting text on the page and asking questions about it