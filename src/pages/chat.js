import React from 'react';
import Layout from '@theme/Layout';
import ChatInterface from '../components/ChatInterface/ChatInterface';

// Define the backend URL - using a default that can be overridden by environment
// In browser, process.env is not available, so we only check window object
const BACKEND_URL = typeof window !== 'undefined' && window.BACKEND_URL
  ? window.BACKEND_URL
  : 'http://localhost:8000';

export default function ChatPage() {
  return (
    <Layout title="Book Assistant" description="Physical AI Book Assistant">
      <div style={{ padding: '20px', maxWidth: '900px', margin: '0 auto' }}>
        <h1>Physical AI Book Assistant</h1>
        <p>Ask me anything about the Physical AI Book! Select text on the page and ask a question about it, or type your question below.</p>
        <div style={{ marginTop: '20px', border: '1px solid #ddd', borderRadius: '8px', height: '600px' }}>
          <ChatInterface backendUrl={BACKEND_URL} />
        </div>
      </div>
    </Layout>
  );
}