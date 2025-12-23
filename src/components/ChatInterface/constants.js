// Connection status constants
export const CONNECTION_STATUS = {
  CONNECTED: 'connected',
  DISCONNECTED: 'disconnected',
  RECONNECTING: 'reconnecting',
  ERROR: 'error'
};

// Default retry configuration
export const DEFAULT_RETRY_CONFIG = {
  maxRetries: 5,
  baseDelay: 1000, // 1 second
  maxDelay: 30000, // 30 seconds
  backoffMultiplier: 2
};

// Error messages
export const ERROR_MESSAGES = {
  CONNECTION_FAILED: 'Connection to chat service failed. Retrying...',
  REQUEST_TIMEOUT: 'Request timed out. Retrying...',
  GENERAL_ERROR: 'An error occurred. Please try again.'
};