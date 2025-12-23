import React, { useState, useEffect } from 'react';
import ErrorBoundary from '../components/ErrorBoundary';
import ChatInterface from '../components/ChatInterface/ChatInterface';
import './ChatWidget.css';

const ChatWidget = ({ backendUrl }) => {
  // If backendUrl is not provided via props, determine it based on environment
  const resolvedBackendUrl = backendUrl || (
    typeof window !== 'undefined' && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
      ? 'http://localhost:8000'
      : 'https://usmanhello-physical-ai-book.hf.space'
  );
  const [isOpen, setIsOpen] = useState(false);
  const [hasAnimated, setHasAnimated] = useState(false);

  // Add animation class after component mounts for entrance animation
  useEffect(() => {
    if (!hasAnimated) {
      setHasAnimated(true);
    }
  }, [hasAnimated]);

  return (
    <div className={`chat-widget ${isOpen ? 'open' : 'closed'} ${hasAnimated ? 'animated' : ''}`}>
      {!isOpen && (
        <button
          className="chat-widget-button"
          onClick={() => setIsOpen(true)}
          aria-label="Open chat assistant"
        >
          <span className="chat-icon">💬</span>
        </button>
      )}

      {isOpen && (
        <div className="chat-widget-container">
          <div className="chat-widget-header">
            <h3>Book Assistant</h3>
            <button
              className="chat-widget-close"
              onClick={() => setIsOpen(false)}
              aria-label="Close chat"
            >
              ×
            </button>
          </div>
          <div className="chat-widget-content">
            <ErrorBoundary>
              <ChatInterface backendUrl={resolvedBackendUrl} />
            </ErrorBoundary>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatWidget;