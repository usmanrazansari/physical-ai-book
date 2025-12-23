import { CONNECTION_STATUS } from './constants';

class ConnectionStatusManager {
  constructor(onStatusChange) {
    this.status = CONNECTION_STATUS.CONNECTED;
    this.lastConnected = new Date();
    this.retryCount = 0;
    this.nextRetryTime = null;
    this.onStatusChange = onStatusChange; // Callback to notify about status changes
    this.statusHistory = [];
  }

  updateStatus(newStatus, reason = null) {
    const oldStatus = this.status;
    this.status = newStatus;

    // Record status change in history
    this.statusHistory.push({
      status: newStatus,
      timestamp: new Date(),
      reason: reason
    });

    // Keep only the last 50 status changes to prevent memory issues
    if (this.statusHistory.length > 50) {
      this.statusHistory = this.statusHistory.slice(-50);
    }

    // Update related properties based on status
    if (newStatus === CONNECTION_STATUS.CONNECTED) {
      this.lastConnected = new Date();
      this.retryCount = 0;
      this.nextRetryTime = null;
    } else if (newStatus === CONNECTION_STATUS.DISCONNECTED ||
               newStatus === CONNECTION_STATUS.RECONNECTING) {
      this.retryCount += 1;
    }

    // Log status change for debugging
    console.log(`[ConnectionStatusManager] Status changed from ${oldStatus} to ${newStatus}`, {
      reason,
      retryCount: this.retryCount,
      timestamp: new Date().toISOString()
    });

    // Notify about status change if callback exists
    if (this.onStatusChange && oldStatus !== newStatus) {
      this.onStatusChange(newStatus, oldStatus, reason);
    }
  }

  getStatus() {
    return this.status;
  }

  isOnline() {
    return this.status === CONNECTION_STATUS.CONNECTED;
  }

  isReconnecting() {
    return this.status === CONNECTION_STATUS.RECONNECTING;
  }

  isDisconnected() {
    return this.status === CONNECTION_STATUS.DISCONNECTED || this.status === CONNECTION_STATUS.ERROR;
  }

  getRetryCount() {
    return this.retryCount;
  }

  resetRetryCount() {
    this.retryCount = 0;
  }

  getStatusInfo() {
    return {
      status: this.status,
      lastConnected: this.lastConnected,
      retryCount: this.retryCount,
      nextRetryTime: this.nextRetryTime,
      isOnline: this.isOnline(),
      isReconnecting: this.isReconnecting(),
      isDisconnected: this.isDisconnected()
    };
  }

  getStatusHistory() {
    return [...this.statusHistory]; // Return a copy to prevent external modification
  }
}

export default ConnectionStatusManager;