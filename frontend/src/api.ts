import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://yes-chef-uj7s.onrender.com/api/'

// Create configured axios instance
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true // Enable sending cookies with requests
})

// Add request interceptors
apiClient.interceptors.request.use(
  (config) => {
    // Get CSRF token from cookie
    const csrfToken = document.cookie
      .split('; ')
      .find(row => row.startsWith('csrftoken='))
      ?.split('=')[1]

    if (csrfToken) {
      config.headers['X-CSRFToken'] = csrfToken
    }

    // Add any other headers or modifications here
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
          console.error('Unauthorized access. Please log in.')
          // You might want to redirect to login page or clear user state
          break
        case 403:
          // Handle forbidden access
          console.error('Forbidden access. Please check your permissions.')
          break
        case 404:
          // Handle not found errors
          console.error('Resource not found.')
          break
        // Add other cases as needed
      }
    }
    return Promise.reject(error)
  }
)