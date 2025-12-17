import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import ChatWidget from '../../plugins/ChatWidget';

// Define the backend URL - using a default that can be overridden by environment
// In browser, process.env is not available, so we only check window object
const BACKEND_URL = typeof window !== 'undefined' && window.BACKEND_URL
  ? window.BACKEND_URL
  : 'http://localhost:8000';

export default function Layout(props) {
  return (
    <>
      <OriginalLayout {...props} />
      <ChatWidget backendUrl={BACKEND_URL} />
    </>
  );
}