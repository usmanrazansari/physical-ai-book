import { DEFAULT_RETRY_CONFIG } from './constants';

class RetryMechanism {
  constructor(config = {}) {
    this.config = {
      ...DEFAULT_RETRY_CONFIG,
      ...config
    };
    this.currentAttempt = 0;
    this.abortController = null;
    this.operationId = null; // Track the current operation
    this.isOperationRunning = false; // Flag to prevent multiple simultaneous operations
  }

  calculateDelay(attempt) {
    // Exponential backoff: baseDelay * (backoffMultiplier ^ attempt)
    let delay = this.config.baseDelay * Math.pow(this.config.backoffMultiplier, attempt);
    // Cap the delay at maxDelay
    delay = Math.min(delay, this.config.maxDelay);
    // Add some jitter to prevent thundering herd
    delay = delay + Math.random() * 1000;
    return delay;
  }

  async executeWithRetry(operation, shouldRetry = () => true) {
    // Check if an operation is already running to prevent multiple simultaneous operations
    if (this.isOperationRunning) {
      throw new Error('Another operation is already in progress. Please wait for it to complete.');
    }

    // Mark operation as running
    this.isOperationRunning = true;
    this.currentAttempt = 0;

    try {
      while (this.currentAttempt < this.config.maxRetries) {
        try {
          // Create a new abort controller for each attempt
          this.abortController = new AbortController();

          // Execute the operation with a timeout
          const result = await this.executeWithTimeout(
            operation(this.currentAttempt),
            this.config.baseDelay * 10, // 10x base delay as timeout
            this.abortController.signal
          );

          // Reset current attempt on success
          this.currentAttempt = 0;
          return result;
        } catch (error) {
          this.currentAttempt++;

          // Check if we should stop retrying
          if (!shouldRetry(error) || this.currentAttempt >= this.config.maxRetries) {
            this.currentAttempt = 0; // Reset on final failure
            throw error;
          }

          // Wait before retrying
          const delay = this.calculateDelay(this.currentAttempt - 1);
          await this.delay(delay);
        }
      }
    } finally {
      // Mark operation as no longer running
      this.isOperationRunning = false;
      this.currentAttempt = 0;
    }
  }

  async executeWithTimeout(promise, timeoutMs, signal) {
    let timeoutId;

    const timeoutPromise = new Promise((_, reject) => {
      timeoutId = setTimeout(() => {
        if (signal) {
          signal.abort();
        }
        reject(new Error('Request timeout'));
      }, timeoutMs);
    });

    try {
      const result = await Promise.race([promise, timeoutPromise]);
      clearTimeout(timeoutId);
      return result;
    } catch (error) {
      clearTimeout(timeoutId);
      throw error;
    }
  }

  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  cancelCurrentOperation() {
    if (this.abortController) {
      this.abortController.abort();
    }
  }

  getCurrentAttempt() {
    return this.currentAttempt;
  }

  isRetrying() {
    return this.currentAttempt > 0;
  }

  reset() {
    this.currentAttempt = 0;
    if (this.abortController) {
      this.abortController.abort();
    }
  }
}

export default RetryMechanism;