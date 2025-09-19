import axios from "axios"

// API base configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000/api"

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token")
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem("refresh_token")
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
            refresh: refreshToken,
          })

          const { access } = response.data
          localStorage.setItem("access_token", access)

          // Retry original request with new token
          originalRequest.headers.Authorization = `Bearer ${access}`
          return api(originalRequest)
        }
      } catch (refreshError) {
        // Refresh failed, redirect to login
        localStorage.removeItem("access_token")
        localStorage.removeItem("refresh_token")
        localStorage.removeItem("aikshetra_user")
        window.location.href = "/login"
      }
    }

    return Promise.reject(error)
  },
)

// Authentication API
export const authAPI = {
  login: async (credentials) => {
    const response = await api.post("/auth/login/", credentials)
    return response.data
  },

  register: async (userData) => {
    const response = await api.post("/auth/register/", userData)
    return response.data
  },

  logout: async (refreshToken) => {
    const response = await api.post("/auth/logout/", { refresh_token: refreshToken })
    return response.data
  },

  getCurrentUser: async () => {
    const response = await api.get("/auth/current-user/")
    return response.data
  },

  getUserStats: async () => {
    const response = await api.get("/auth/user-stats/")
    return response.data
  },

  updateProfile: async (profileData) => {
    const response = await api.patch("/auth/profile/", profileData)
    return response.data
  },

  changePassword: async (passwordData) => {
    const response = await api.post("/auth/change-password/", passwordData)
    return response.data
  },

  updateProfilePicture: async (file) => {
    const formData = new FormData()
    formData.append("profile_picture", file)
    const response = await api.post("/auth/update-profile-picture/", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    })
    return response.data
  },

  searchUsers: async (query) => {
    const response = await api.get(`/auth/search-users/?q=${encodeURIComponent(query)}`)
    return response.data
  },

  // Admin functions
  getPendingUsers: async () => {
    const response = await api.get("/auth/pending-users/")
    return response.data
  },

  approveUser: async (userId, action) => {
    const response = await api.patch(`/auth/approve-user/${userId}/`, { action })
    return response.data
  },
}

// Employee Management API
export const employeeAPI = {
  getDepartments: async () => {
    const response = await api.get("/employees/departments/")
    return response.data
  },

  createDepartment: async (departmentData) => {
    const response = await api.post("/employees/departments/", departmentData)
    return response.data
  },

  updateDepartment: async (id, departmentData) => {
    const response = await api.patch(`/employees/departments/${id}/`, departmentData)
    return response.data
  },

  getPositions: async () => {
    const response = await api.get("/employees/positions/")
    return response.data
  },

  getEmployeeDetails: async () => {
    const response = await api.get("/employees/employee-details/")
    return response.data
  },
}

// Attendance API
export const attendanceAPI = {
  getAttendanceRecords: async () => {
    const response = await api.get("/attendance/records/")
    return response.data
  },

  checkIn: async () => {
    const response = await api.post("/attendance/check-in/")
    return response.data
  },

  checkOut: async () => {
    const response = await api.post("/attendance/check-out/")
    return response.data
  },

  getLeaveRequests: async () => {
    const response = await api.get("/attendance/leave-requests/")
    return response.data
  },

  createLeaveRequest: async (leaveData) => {
    const response = await api.post("/attendance/leave-requests/", leaveData)
    return response.data
  },

  approveLeave: async (leaveId, action, reason = "") => {
    const response = await api.post(`/attendance/leave-requests/${leaveId}/approve/`, {
      action,
      reason,
    })
    return response.data
  },
}

// Tasks API
export const tasksAPI = {
  getProjects: async () => {
    const response = await api.get("/tasks/projects/")
    return response.data
  },

  createProject: async (projectData) => {
    const response = await api.post("/tasks/projects/", projectData)
    return response.data
  },

  getTasks: async () => {
    const response = await api.get("/tasks/")
    return response.data
  },

  createTask: async (taskData) => {
    const response = await api.post("/tasks/", taskData)
    return response.data
  },

  updateTask: async (taskId, taskData) => {
    const response = await api.patch(`/tasks/${taskId}/`, taskData)
    return response.data
  },

  completeTask: async (taskId, completionNotes = "") => {
    const response = await api.post(`/tasks/${taskId}/complete/`, {
      completion_notes: completionNotes,
    })
    return response.data
  },

  getTaskComments: async (taskId) => {
    const response = await api.get(`/tasks/${taskId}/comments/`)
    return response.data
  },

  addTaskComment: async (taskId, comment, attachment = null) => {
    const formData = new FormData()
    formData.append("comment", comment)
    if (attachment) {
      formData.append("attachment", attachment)
    }

    const response = await api.post(`/tasks/${taskId}/comments/`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    })
    return response.data
  },
}

// Salary API
export const salaryAPI = {
  getSalaryStructures: async () => {
    const response = await api.get("/salary/structures/")
    return response.data
  },

  getEmployeeSalaries: async () => {
    const response = await api.get("/salary/employee-salaries/")
    return response.data
  },

  getPayrollRecords: async () => {
    const response = await api.get("/salary/payroll/")
    return response.data
  },

  createPayroll: async (payrollData) => {
    const response = await api.post("/salary/payroll/", payrollData)
    return response.data
  },
}

// Learning API
export const learningAPI = {
  getCourses: async () => {
    const response = await api.get("/learning/courses/")
    return response.data
  },

  createCourse: async (courseData) => {
    const response = await api.post("/learning/courses/", courseData)
    return response.data
  },

  enrollInCourse: async (courseId) => {
    const response = await api.post(`/learning/courses/${courseId}/enroll/`)
    return response.data
  },

  getEnrollments: async () => {
    const response = await api.get("/learning/enrollments/")
    return response.data
  },

  getLearningPaths: async () => {
    const response = await api.get("/learning/learning-paths/")
    return response.data
  },

  getTrainingSessions: async () => {
    const response = await api.get("/learning/training-sessions/")
    return response.data
  },
}

// Notifications API
export const notificationsAPI = {
  getNotifications: async () => {
    const response = await api.get("/notifications/")
    return response.data
  },

  markNotificationRead: async (notificationId) => {
    const response = await api.post(`/notifications/${notificationId}/read/`)
    return response.data
  },

  getNotificationPreferences: async () => {
    const response = await api.get("/notifications/preferences/")
    return response.data
  },

  updateNotificationPreferences: async (preferences) => {
    const response = await api.patch("/notifications/preferences/", preferences)
    return response.data
  },

  getSystemAnnouncements: async () => {
    const response = await api.get("/notifications/announcements/")
    return response.data
  },

  createSystemAnnouncement: async (announcementData) => {
    const response = await api.post("/notifications/announcements/", announcementData)
    return response.data
  },
}

export default api
