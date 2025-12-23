# Data Model: Chatbot Connection Error Fix

## Key Entities

### Connection Status
- **Name**: ConnectionStatus
- **Description**: Represents the current state of communication with the chatbot service
- **Attributes**:
  - status: String (connected, disconnected, reconnecting, error)
  - lastConnected: DateTime (timestamp of last successful connection)
  - retryCount: Integer (number of reconnection attempts)
  - nextRetryTime: DateTime (when next retry is scheduled)

### Error Message
- **Name**: ErrorMessage
- **Description**: Contains information about the failure reason and potential recovery steps
- **Attributes**:
  - message: String (user-friendly error message)
  - code: String (error code for debugging)
  - timestamp: DateTime (when error occurred)
  - retryable: Boolean (whether retry is possible)
  - action: String (suggested action for user)

### Retry Mechanism
- **Name**: RetryMechanism
- **Description**: Handles automatic reconnection attempts with exponential backoff
- **Attributes**:
  - maxRetries: Integer (maximum number of retry attempts)
  - baseDelay: Integer (base delay in milliseconds for exponential backoff)
  - maxDelay: Integer (maximum delay in milliseconds)
  - backoffMultiplier: Float (multiplier for exponential backoff)
  - currentAttempt: Integer (current attempt number)

## Relationships
- ChatInterface manages one ConnectionStatus
- ChatInterface displays zero or more ErrorMessage instances
- ConnectionStatus uses one RetryMechanism for reconnection logic

## State Transitions
- Connected → Disconnected (when connection fails)
- Disconnected → Reconnecting (when retry is initiated)
- Reconnecting → Connected (when connection succeeds)
- Reconnecting → Error (when retry fails and max attempts reached)
- Error → Reconnecting (when user manually retries)