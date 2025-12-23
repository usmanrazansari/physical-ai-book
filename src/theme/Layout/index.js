import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import ChatWidget from '../../plugins/ChatWidget';

// Define the backend URL with environment-based defaults
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
      // Default to a production-ready URL (can be configured in docusaurus.config.js)
      return 'https://physical-ai-book-backend.onrender.com'; // Example production backend
    }
  }

  // Fallback for SSR
  return 'http://localhost:8000';
};

const BACKEND_URL = getBackendUrl();

export default function Layout(props) {
  return (
    <>
      <OriginalLayout {...props} />
      <ChatWidget backendUrl={BACKEND_URL} />
    </>
  );
}