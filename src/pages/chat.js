import React from 'react';
import Layout from '@theme/Layout';
import ChatInterface from '../components/ChatInterface/ChatInterface';

// Define the backend URL - using a default that can be overridden by environment
// In browser, process.env is not available, so we check window object and URL parameters
const getBackendUrl = () => {
  // Check for URL parameter override first
  if (typeof window !== 'undefined') {
    const urlParams = new URLSearchParams(window.location.search);
    const backendParam = urlParams.get('backend');
    if (backendParam) {
      return backendParam;
    }

    // Check for window variable
    if (window.BACKEND_URL) {
      return window.BACKEND_URL;
    }

    // Check for environment-specific configuration
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      return 'http://localhost:8000';
    } else {
      // Use the working Hugging Face Space backend for production
      return 'https://usmanhello-physical-ai-book.hf.space';
    }
  }

  // Fallback for SSR
  return 'http://localhost:8000';
};

const BACKEND_URL = getBackendUrl();

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