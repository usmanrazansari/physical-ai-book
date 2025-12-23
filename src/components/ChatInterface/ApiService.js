/**
 * API Service for Chat Interface
 * Handles all communication with the backend RAG agent
 */

import RetryMechanism from './RetryMechanism';
import { DEFAULT_RETRY_CONFIG, ERROR_MESSAGES } from './constants';

class ApiService {
  constructor(baseURL, retryConfig = {}) {
    this.baseURL = baseURL;
    this.retryMechanism = new RetryMechanism({ ...DEFAULT_RETRY_CONFIG, ...retryConfig });
  }

  /**
   * Send a query to the backend RAG agent
   * @param {string} query - The user's question
   * @param {string|null} context - Optional context from selected text
   * @returns {Promise<Object>} The response from the backend
   */
  async askQuestion(query, context = null) {
    try {
      return await this.retryMechanism.executeWithRetry(async (attempt) => {
        try {
          // Prepare the payload
          const payload = {
            query: query,
            ...(context && { context: context })
          };

          // Call the backend API with timeout
          const controller = new AbortController();
          const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

          const response = await fetch(`${this.baseURL}/chat`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
            signal: controller.signal
          });

          clearTimeout(timeoutId);

          if (!response.ok) {
            throw new Error(`Backend error: ${response.status} - ${response.statusText}`);
          }

          const data = await response.json();
          return {
            success: true,
            data: data
          };
        } catch (error) {
          // Log the error for debugging
          console.error(`Attempt ${attempt + 1} failed:`, error.message);

          // If it's an abort error (timeout), throw a specific error
          if (error.name === 'AbortError') {
            throw new Error(ERROR_MESSAGES.REQUEST_TIMEOUT);
          }

          throw error;
        }
      }, (error) => {
        // Determine if we should retry based on the error
        return this.shouldRetry(error);
      });
    } catch (error) {
      // If it's the "operation in progress" error, return a special response
      if (error.message.includes('already in progress')) {
        return {
          success: false,
          error: 'Request already in progress. Please wait for the previous request to complete.',
          operationInProgress: true
        };
      }
      throw error;
    }
  }

  /**
   * Determines if an operation should be retried based on the error
   * @param {Error} error - The error that occurred
   * @returns {boolean} Whether to retry
   */
  shouldRetry(error) {
    // Retry on network errors, timeouts, and server errors (5xx)
    const errorMessage = error.message.toLowerCase();
    return (
      errorMessage.includes('failed to fetch') ||
      errorMessage.includes('networkerror') ||
      errorMessage.includes('timeout') ||
      errorMessage.includes('aborterror') ||
      error.message.includes('5') // catches 5xx status errors
    );
  }

  /**
   * Check if the backend service is available
   * @returns {Promise<boolean>} Whether the backend is reachable
   */
  async checkHealth() {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout

      const response = await fetch(`${this.baseURL}/health`, {
        method: 'GET',
        signal: controller.signal
      });

      clearTimeout(timeoutId);
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

      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 second timeout

      const response = await fetch(`${this.baseURL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
        signal: controller.signal
      });

      clearTimeout(timeoutId);

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

  /**
   * Cancel the current operation if possible
   */
  cancelCurrentOperation() {
    this.retryMechanism.cancelCurrentOperation();
  }

  /**
   * Get retry mechanism status
   */
  getRetryStatus() {
    return {
      isRetrying: this.retryMechanism.isRetrying(),
      currentAttempt: this.retryMechanism.getCurrentAttempt(),
      maxRetries: this.retryMechanism.config.maxRetries
    };
  }
}

// Default instance - can be configured with environment variable or prop
let apiServiceInstance = null;

export const getApiService = (baseURL, retryConfig = {}) => {
  if (!apiServiceInstance) {
    apiServiceInstance = new ApiService(baseURL, retryConfig);
  }
  return apiServiceInstance;
};

export default ApiService;