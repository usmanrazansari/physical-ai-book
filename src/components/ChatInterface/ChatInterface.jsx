import React, { useState, useRef, useEffect } from 'react';
import './ChatInterface.css';
import { getApiService } from './ApiService';

const ChatInterface = ({ backendUrl = 'http://localhost:8000' }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const [connectionError, setConnectionError] = useState(false);
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  // Initialize API service
  const apiService = getApiService(backendUrl);

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
    setConnectionError(false); // Reset connection error state

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
      } else {
        // Handle API error
        throw new Error(result.error);
      }
    } catch (error) {
      console.error('Error sending message:', error);
      setConnectionError(true);

      // Add error message to chat
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error. Please check your connection and try again.',
        sender: 'bot',
        timestamp: new Date().toISOString(),
        isError: true
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      setInputValue('');
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputValue.trim() || selectedText) {
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

  // Function to clear chat
  const clearChat = () => {
    setMessages([]);
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h3>Physical AI Book Assistant</h3>
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
              className={`message ${message.sender} ${message.isError ? 'error' : ''}`}
            >
              <div className="message-content">
                {message.context && (
                  <div className="message-context">
                    <small>Context: "{message.context.substring(0, 100)}{message.context.length > 100 ? '...' : ''}"</small>
                  </div>
                )}
                <div className="message-text">{message.text}</div>
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