import React, { useState, useRef, useEffect } from 'react';
import './ChatInterface.css';
import { getApiService } from './ApiService';
import ConnectionStatusManager from './ConnectionStatusManager';
import { CONNECTION_STATUS, ERROR_MESSAGES } from './constants';

const ChatInterface = ({ backendUrl = 'http://localhost:8000' }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const [connectionStatus, setConnectionStatus] = useState(CONNECTION_STATUS.CONNECTED);
  const [retryCount, setRetryCount] = useState(0);
  const [preservedInput, setPreservedInput] = useState(''); // To preserve user input during failures
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  // Initialize API service with retry configuration
  const apiService = getApiService(backendUrl);

  // Initialize connection status manager
  const connectionManager = useRef(null);

  useEffect(() => {
    // Initialize connection status manager
    connectionManager.current = new ConnectionStatusManager((newStatus) => {
      setConnectionStatus(newStatus);
    });

    // Check initial connection status
    const checkInitialConnection = async () => {
      try {
        // Try the health check but don't fail if it doesn't exist or takes too long
        // Some backends might not have a /health endpoint
        const isConnected = await apiService.checkHealth();
        // Don't immediately mark as disconnected on initial check failure
        // as mobile networks might be slower to respond
        if (!isConnected) {
          console.log('Initial connection check failed, but keeping status as connected for mobile tolerance');
          // Keep current status instead of changing to disconnected immediately
        }
      } catch (error) {
        // The health endpoint might not exist or be accessible
        // This is OK - we'll proceed assuming the backend is available
        console.log('Health check failed or not available, proceeding with connection');
        // Keep current status instead of changing to disconnected immediately
      }
    };

    checkInitialConnection();

    // Cleanup function
    return () => {
      apiService.cancelCurrentOperation();
    };
  }, [backendUrl]);

  // Function to scroll to bottom of chat
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Function to get selected text from the page
  useEffect(() => {
    const handleSelection = () => {
      const selectedText = window.getSelection().toString().trim();
      if (selectedText) {
        setSelectedText(selectedText);
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => {
      document.removeEventListener('mouseup', handleSelection);
    };
  }, []);

  // Function to send message to backend
  const sendMessage = async (query, context = null) => {
    if (!query.trim() && !context) return;

    setIsLoading(true);

    // Update connection status to show we're trying to connect
    if (connectionManager.current) {
      connectionManager.current.updateStatus(CONNECTION_STATUS.RECONNECTING, 'Sending message');
    }

    // Add user message to chat
    const userMessage = {
      id: Date.now(),
      text: query,
      sender: 'user',
      timestamp: new Date().toISOString(),
      context: context || null
    };

    setMessages(prev => [...prev, userMessage]);

    try {
      // Call the backend API using the service
      const result = await apiService.askQuestion(query, context);

      if (result.success) {
        // Update connection status to connected on success
        if (connectionManager.current) {
          connectionManager.current.updateStatus(CONNECTION_STATUS.CONNECTED, 'Message sent successfully');
        }

        // Add bot response to chat
        const botMessage = {
          id: Date.now() + 1,
          text: result.data.response || result.data.answer || 'Sorry, I could not process your request.',
          sender: 'bot',
          timestamp: new Date().toISOString(),
          metadata: result.data.metadata || null,
          sources: result.data.sources || result.data.source_documents || null
        };

        setMessages(prev => [...prev, botMessage]);
      } else if (result.operationInProgress) {
        // Handle case where operation is already in progress
        const warningMessage = {
          id: Date.now() + 1,
          text: result.error,
          sender: 'bot',
          timestamp: new Date().toISOString(),
          isWarning: true
        };

        setMessages(prev => [...prev, warningMessage]);
      } else {
        // Handle API error
        throw new Error(result.error);
      }
    } catch (error) {
      console.error('Error sending message:', error);

      // Update connection status based on error
      // On mobile, be more tolerant of connection issues
      if (connectionManager.current) {
        // Don't immediately mark as ERROR for network-related issues on mobile
        if (error.message.includes('Failed to fetch') ||
            error.message.includes('NetworkError') ||
            error.message.includes('timeout') ||
            error.message.includes('CORS') ||
            error.message.includes('network') ||
            error.name === 'TypeError' ||
            error.name === 'AbortError') {
          // Keep as CONNECTED but show error to user - mobile networks can be flaky
          connectionManager.current.updateStatus(CONNECTION_STATUS.CONNECTED, 'Connection issue detected');
        } else {
          connectionManager.current.updateStatus(CONNECTION_STATUS.ERROR, error.message);
        }
      }

      // Add error message to chat
      const errorMessage = {
        id: Date.now() + 1,
        text: error.message.includes('timeout')
          ? ERROR_MESSAGES.REQUEST_TIMEOUT
          : error.message.includes('Failed to fetch') ||
            error.message.includes('NetworkError') ||
            error.message.includes('network') ||
            error.name === 'TypeError'
            ? 'Connection failed. Mobile networks can be slower. Please try again.'
            : error.name === 'AbortError'
              ? 'Request timed out. Mobile networks may be slow. Please try again.'
              : 'Sorry, I encountered an error. Please check your connection and try again.',
        sender: 'bot',
        timestamp: new Date().toISOString(),
        isError: true,
        canRetry: true // Flag to indicate if retry is possible
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);

      // If there was preserved input, restore it after the attempt
      if (preservedInput) {
        setInputValue(preservedInput);
        setPreservedInput('');
      } else {
        setInputValue('');
      }
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputValue.trim() || selectedText) {
      // Preserve the input value in case of connection failure
      if (inputValue.trim()) {
        setPreservedInput(inputValue);
      }
      sendMessage(inputValue, selectedText);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (inputValue.trim() || selectedText) {
        handleSubmit(e);
      }
    }
  };

  // Function to handle retrying a failed message
  const handleRetryMessage = (error_message) => {
    // Find the user message that corresponds to this error
    const userMessageIndex = messages.findIndex((msg, index) => {
      // The user message should be the one before the error message
      return index < messages.length - 1 &&
             messages[index + 1]?.id === error_message.id &&
             messages[index].sender === 'user';
    });

    if (userMessageIndex !== -1) {
      const userMessage = messages[userMessageIndex];
      // Preserve the input and resend the query
      setPreservedInput(userMessage.text);
      sendMessage(userMessage.text, userMessage.context);
    }
  };

  // Function to clear chat
  const clearChat = () => {
    setMessages([]);
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <div className="header-content">
          <h3>Physical AI Book Assistant</h3>
          <div className={`connection-status ${connectionStatus}`}>
            <span className="status-indicator"></span>
            <span className="status-text">
              {connectionStatus === CONNECTION_STATUS.CONNECTED && 'Online'}
              {connectionStatus === CONNECTION_STATUS.DISCONNECTED && 'Offline'}
              {connectionStatus === CONNECTION_STATUS.RECONNECTING && 'Reconnecting...'}
              {connectionStatus === CONNECTION_STATUS.ERROR && 'Error'}
            </span>
          </div>
        </div>
        <button className="clear-chat-btn" onClick={clearChat} title="Clear chat">
          ×
        </button>
      </div>

      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <p>Ask me anything about the Physical AI Book! Select text on the page and ask a question about it, or type your question below.</p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`message ${message.sender} ${message.isError ? 'error' : ''} ${message.isWarning ? 'warning' : ''}`}
            >
              <div className="message-content">
                {message.context && (
                  <div className="message-context">
                    <small>Context: "{message.context.substring(0, 100)}{message.context.length > 100 ? '...' : ''}"</small>
                  </div>
                )}
                <div className="message-text">{message.text}</div>
                {message.isError && message.canRetry && !isLoading && (
                  <div className="error-actions">
                    <button className="retry-button" onClick={() => handleRetryMessage(message)}>
                      Retry
                    </button>
                  </div>
                )}
                {message.sources && message.sources.length > 0 && (
                  <div className="message-sources">
                    <details>
                      <summary>Sources</summary>
                      <ul>
                        {message.sources.map((source, index) => (
                          <li key={index}>
                            {source.url ? (
                              <a href={source.url} target="_blank" rel="noopener noreferrer">
                                {source.title || source.url}
                              </a>
                            ) : (
                              <span>{source.title || source.page || `Source ${index + 1}`}</span>
                            )}
                          </li>
                        ))}
                      </ul>
                    </details>
                  </div>
                )}
              </div>
              <div className="message-timestamp">
                {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="message bot loading">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {selectedText && (
        <div className="selected-text-preview">
          <small>Selected: "{selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}"</small>
          <button
            className="use-selection-btn"
            onClick={() => sendMessage(inputValue, selectedText)}
            disabled={isLoading || !inputValue.trim()}
          >
            Ask about selection
          </button>
        </div>
      )}

      <form className="chat-input-form" onSubmit={handleSubmit}>
        <textarea
          ref={textareaRef}
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about the Physical AI Book..."
          disabled={isLoading}
          rows={1}
          className="chat-input"
        />
        <button
          type="submit"
          disabled={isLoading || (!inputValue.trim() && !selectedText)}
          className="send-button"
        >
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </form>
    </div>
  );
};

export default ChatInterface;