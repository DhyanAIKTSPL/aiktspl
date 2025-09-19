class WebSocketService {
  constructor() {
    this.connections = new Map()
    this.reconnectAttempts = new Map()
    this.maxReconnectAttempts = 5
    this.reconnectInterval = 3000
  }

  connect(endpoint, userId, onMessage, onError = null, onClose = null) {
    const wsUrl = `${process.env.REACT_APP_WS_URL || "ws://localhost:8000"}/ws/${endpoint}/${userId}/`

    if (this.connections.has(endpoint)) {
      this.disconnect(endpoint)
    }

    try {
      const ws = new WebSocket(wsUrl)

      ws.onopen = () => {
        console.log(`WebSocket connected: ${endpoint}`)
        this.reconnectAttempts.set(endpoint, 0)
      }

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          onMessage(data)
        } catch (error) {
          console.error("Error parsing WebSocket message:", error)
        }
      }

      ws.onerror = (error) => {
        console.error(`WebSocket error on ${endpoint}:`, error)
        if (onError) onError(error)
      }

      ws.onclose = (event) => {
        console.log(`WebSocket closed: ${endpoint}`, event.code, event.reason)
        this.connections.delete(endpoint)

        if (onClose) onClose(event)

        // Attempt to reconnect if not a normal closure
        if (event.code !== 1000) {
          this.attemptReconnect(endpoint, userId, onMessage, onError, onClose)
        }
      }

      this.connections.set(endpoint, ws)
      return ws
    } catch (error) {
      console.error(`Failed to create WebSocket connection for ${endpoint}:`, error)
      if (onError) onError(error)
    }
  }

  attemptReconnect(endpoint, userId, onMessage, onError, onClose) {
    const attempts = this.reconnectAttempts.get(endpoint) || 0

    if (attempts < this.maxReconnectAttempts) {
      this.reconnectAttempts.set(endpoint, attempts + 1)

      setTimeout(() => {
        console.log(`Attempting to reconnect ${endpoint} (attempt ${attempts + 1})`)
        this.connect(endpoint, userId, onMessage, onError, onClose)
      }, this.reconnectInterval * Math.pow(2, attempts)) // Exponential backoff
    } else {
      console.error(`Max reconnection attempts reached for ${endpoint}`)
    }
  }

  send(endpoint, message) {
    const ws = this.connections.get(endpoint)
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify(message))
      return true
    }
    console.warn(`WebSocket not connected for ${endpoint}`)
    return false
  }

  disconnect(endpoint) {
    const ws = this.connections.get(endpoint)
    if (ws) {
      ws.close(1000, "Client disconnect")
      this.connections.delete(endpoint)
      this.reconnectAttempts.delete(endpoint)
    }
  }

  disconnectAll() {
    for (const endpoint of this.connections.keys()) {
      this.disconnect(endpoint)
    }
  }

  isConnected(endpoint) {
    const ws = this.connections.get(endpoint)
    return ws && ws.readyState === WebSocket.OPEN
  }
}

// Create singleton instance
const websocketService = new WebSocketService()

// Specific service methods for different endpoints
export const notificationWebSocket = {
  connect: (userId, onMessage, onError, onClose) => {
    return websocketService.connect("notifications", userId, onMessage, onError, onClose)
  },

  send: (message) => {
    return websocketService.send("notifications", message)
  },

  disconnect: () => {
    websocketService.disconnect("notifications")
  },

  markRead: (notificationId) => {
    return websocketService.send("notifications", {
      type: "mark_read",
      notification_id: notificationId,
    })
  },

  getNotifications: () => {
    return websocketService.send("notifications", {
      type: "get_notifications",
    })
  },
}

export const attendanceWebSocket = {
  connect: (userId, onMessage, onError, onClose) => {
    return websocketService.connect("attendance", userId, onMessage, onError, onClose)
  },

  disconnect: () => {
    websocketService.disconnect("attendance")
  },
}

export const taskWebSocket = {
  connect: (userId, onMessage, onError, onClose) => {
    return websocketService.connect("tasks", userId, onMessage, onError, onClose)
  },

  disconnect: () => {
    websocketService.disconnect("tasks")
  },
}

export const systemWebSocket = {
  connect: (onMessage, onError, onClose) => {
    const wsUrl = `${process.env.REACT_APP_WS_URL || "ws://localhost:8000"}/ws/system/`

    if (websocketService.connections.has("system")) {
      websocketService.disconnect("system")
    }

    try {
      const ws = new WebSocket(wsUrl)

      ws.onopen = () => {
        console.log("System WebSocket connected")
      }

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          onMessage(data)
        } catch (error) {
          console.error("Error parsing system WebSocket message:", error)
        }
      }

      ws.onerror = (error) => {
        console.error("System WebSocket error:", error)
        if (onError) onError(error)
      }

      ws.onclose = (event) => {
        console.log("System WebSocket closed:", event.code, event.reason)
        websocketService.connections.delete("system")
        if (onClose) onClose(event)
      }

      websocketService.connections.set("system", ws)
      return ws
    } catch (error) {
      console.error("Failed to create system WebSocket connection:", error)
      if (onError) onError(error)
    }
  },

  disconnect: () => {
    websocketService.disconnect("system")
  },
}

export default websocketService
