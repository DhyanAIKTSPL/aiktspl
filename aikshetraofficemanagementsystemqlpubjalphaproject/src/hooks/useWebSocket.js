"use client"

import { useEffect, useRef, useCallback } from "react"
import { useAuth } from "../contexts/AuthContext"
import websocketService from "../services/websocket"

export const useWebSocket = (endpoint, onMessage, options = {}) => {
  const { user } = useAuth()
  const { onError = null, onClose = null, autoConnect = true, reconnect = true } = options

  const wsRef = useRef(null)
  const reconnectTimeoutRef = useRef(null)

  const connect = useCallback(() => {
    if (!user?.id || wsRef.current) return

    wsRef.current = websocketService.connect(endpoint, user.id, onMessage, onError, onClose)
  }, [endpoint, user?.id, onMessage, onError, onClose])

  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current)
      reconnectTimeoutRef.current = null
    }

    websocketService.disconnect(endpoint)
    wsRef.current = null
  }, [endpoint])

  const send = useCallback(
    (message) => {
      return websocketService.send(endpoint, message)
    },
    [endpoint],
  )

  const isConnected = useCallback(() => {
    return websocketService.isConnected(endpoint)
  }, [endpoint])

  useEffect(() => {
    if (autoConnect && user?.id) {
      connect()
    }

    return () => {
      disconnect()
    }
  }, [autoConnect, user?.id, connect, disconnect])

  return {
    connect,
    disconnect,
    send,
    isConnected,
  }
}

export const useNotifications = (onNotification) => {
  const { user } = useAuth()

  return useWebSocket("notifications", (data) => {
    switch (data.type) {
      case "new_notification":
        onNotification(data.notification)
        break
      case "unread_count":
        // Handle unread count update
        if (window.updateNotificationCount) {
          window.updateNotificationCount(data.count)
        }
        break
      case "notifications_list":
        // Handle notifications list
        if (window.updateNotificationsList) {
          window.updateNotificationsList(data.notifications)
        }
        break
      default:
        console.log("Unknown notification message type:", data.type)
    }
  })
}

export const useAttendance = (onAttendanceUpdate) => {
  return useWebSocket("attendance", (data) => {
    if (data.type === "attendance_update") {
      onAttendanceUpdate(data.data)
    }
  })
}

export const useTasks = (onTaskUpdate) => {
  return useWebSocket("tasks", (data) => {
    switch (data.type) {
      case "task_assigned":
      case "task_update":
        onTaskUpdate(data.data)
        break
      default:
        console.log("Unknown task message type:", data.type)
    }
  })
}

export const useSystemAnnouncements = (onAnnouncement) => {
  const { user } = useAuth()

  useEffect(() => {
    if (!user?.id) return

    const handleMessage = (data) => {
      if (data.type === "system_announcement") {
        onAnnouncement(data.data)
      }
    }

    const wsUrl = `${process.env.REACT_APP_WS_URL || "ws://localhost:8000"}/ws/system/`
    const ws = new WebSocket(wsUrl)

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        handleMessage(data)
      } catch (error) {
        console.error("Error parsing system message:", error)
      }
    }

    return () => {
      ws.close()
    }
  }, [user?.id, onAnnouncement])
}
