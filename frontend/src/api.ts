import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://yes-chef-uj7s.onrender.com/api/'

// Create configured axios instance
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    // Add any other default headers here
  },
  withCredentials: true // If using cookies for authentication
})

// Add request interceptors
apiClient.interceptors.request.use(
  (config) => {
    // You can modify requests here (e.g., add auth tokens)
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Add response interceptors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle errors globally
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // Handle unauthorized access
          break
        case 404:
          // Handle not found errors
          break
        // Add other cases as needed
      }
    }
    return Promise.reject(error)
  }
)