"use client"

import { createContext, useContext, useState, useEffect } from "react"
import { authAPI } from "../services/api"

const AuthContext = createContext()

export function useAuth() {
  return useContext(AuthContext)
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check for existing session
    const initializeAuth = async () => {
      const token = localStorage.getItem("access_token")
      const savedUser = localStorage.getItem("aikshetra_user")

      if (token && savedUser) {
        try {
          // Verify token is still valid by fetching current user
          const userData = await authAPI.getCurrentUser()
          setUser(userData)
          setIsAuthenticated(true)
        } catch (error) {
          // Token is invalid, clear storage
          localStorage.removeItem("access_token")
          localStorage.removeItem("refresh_token")
          localStorage.removeItem("aikshetra_user")
        }
      }
      setLoading(false)
    }

    initializeAuth()
  }, [])

  const login = async (credentials) => {
    try {
      const response = await authAPI.login(credentials)

      if (response.access && response.user) {
        // Store tokens and user data
        localStorage.setItem("access_token", response.access)
        localStorage.setItem("refresh_token", response.refresh)
        localStorage.setItem("aikshetra_user", JSON.stringify(response.user))

        setUser(response.user)
        setIsAuthenticated(true)

        return { success: true, user: response.user }
      }

      return { success: false, error: "Invalid response from server" }
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.response?.data?.non_field_errors?.[0] || "Login failed"
      return { success: false, error: errorMessage }
    }
  }

  const register = async (userData) => {
    try {
      const response = await authAPI.register(userData)
      return { success: true, user: response.user, message: response.message }
    } catch (error) {
      const errorMessage =
        error.response?.data?.email?.[0] || error.response?.data?.non_field_errors?.[0] || "Registration failed"
      return { success: false, error: errorMessage }
    }
  }

  const logout = () => {
    const refreshToken = localStorage.getItem("refresh_token")

    // Call logout API to blacklist token
    if (refreshToken) {
      authAPI.logout(refreshToken).catch(console.error)
    }

    // Clear local storage
    localStorage.removeItem("access_token")
    localStorage.removeItem("refresh_token")
    localStorage.removeItem("aikshetra_user")

    setUser(null)
    setIsAuthenticated(false)

    // Navigate to login page
    window.location.href = "/login"
  }

  const updateUser = async (profileData) => {
    try {
      const updatedUser = await authAPI.updateProfile(profileData)
      setUser(updatedUser)
      localStorage.setItem("aikshetra_user", JSON.stringify(updatedUser))
      return { success: true, user: updatedUser }
    } catch (error) {
      const errorMessage = error.response?.data?.detail || "Profile update failed"
      return { success: false, error: errorMessage }
    }
  }

  const value = {
    user,
    isAuthenticated,
    login,
    register,
    logout,
    updateUser,
    loading,
  }

  return <AuthContext.Provider value={value}>{!loading && children}</AuthContext.Provider>
}
