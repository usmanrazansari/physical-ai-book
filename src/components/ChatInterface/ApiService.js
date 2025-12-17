/**
 * API Service for Chat Interface
 * Handles all communication with the backend RAG agent
 */

class ApiService {
  constructor(baseURL) {
    this.baseURL = baseURL;
  }

  /**
   * Send a query to the backend RAG agent
   * @param {string} query - The user's question
   * @param {string|null} context - Optional context from selected text
   * @returns {Promise<Object>} The response from the backend
   */
  async askQuestion(query, context = null) {
    try {
      // Prepare the payload
      const payload = {
        query: query,
        ...(context && { context: context })
      };

      // Call the backend API
      const response = await fetch(`${this.baseURL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`Backend error: ${response.status} - ${response.statusText}`);
      }

      const data = await response.json();
      return {
        success: true,
        data: data
      };
    } catch (error) {
      console.error('Error in askQuestion:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Check if the backend service is available
   * @returns {Promise<boolean>} Whether the backend is reachable
   */
  async checkHealth() {
    try {
      const response = await fetch(`${this.baseURL}/health`, {
        method: 'GET',
      });

      return response.ok;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  }

  /**
   * Send a streaming query to the backend (if supported)
   * @param {string} query - The user's question
   * @param {string|null} context - Optional context from selected text
   * @param {Function} onMessage - Callback for each message chunk
   * @param {Function} onError - Callback for errors
   * @returns {Promise<void>}
   */
  async askQuestionStreaming(query, context = null, onMessage, onError) {
    try {
      // Prepare the payload
      const payload = {
        query: query,
        ...(context && { context: context }),
        stream: true // Indicate that we want a streaming response
      };

      // Check if the browser supports fetch with streaming
      if (!window.ReadableStream) {
        throw new Error('Streaming is not supported in this browser');
      }

      const response = await fetch(`${this.baseURL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`Backend error: ${response.status} - ${response.statusText}`);
      }

      // Handle streaming response
      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      let done = false;
      while (!done) {
        const { value, done: readerDone } = await reader.read();
        done = readerDone;

        if (value) {
          const chunk = decoder.decode(value, { stream: true });
          // Process the chunk - this would depend on your backend's streaming format
          // For now, we'll just send the chunk as-is
          onMessage(chunk);
        }
      }
    } catch (error) {
      console.error('Error in streaming askQuestion:', error);
      onError(error.message);
    }
  }
}

// Default instance - can be configured with environment variable or prop
let apiServiceInstance = null;

export const getApiService = (baseURL) => {
  if (!apiServiceInstance) {
    apiServiceInstance = new ApiService(baseURL);
  }
  return apiServiceInstance;
};

export default ApiService;