import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://yes-chef-uj7s.onrender.com/api/'

// Create axios instance with default config
export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true, // Important for cookies
  headers: {
    'Content-Type': 'application/json',
  },
})

// Function to get CSRF token from cookie
const getCsrfToken = () => {
  const name = 'csrftoken'
  let cookieValue = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

// Add request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // Get CSRF token from cookie
    const csrfToken = getCsrfToken()
    if (csrfToken) {
      config.headers['X-CSRFToken'] = csrfToken
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Add response interceptor
apiClient.interceptors.response.use(
  (response) => {
    // Store CSRF token from response headers if present
    const csrfToken = response.headers['x-csrftoken'] || response.data?.csrfToken
    if (csrfToken) {
      document.cookie = `csrftoken=${csrfToken}; path=/; secure; samesite=none`
    }
    return response
  },
  async (error) => {
    if (error.response) {
      // Handle 401 Unauthorized
      if (error.response.status === 401) {
        console.error('Unauthorized access. Please log in.')
        // Optionally redirect to login page
        window.location.href = '/login'
      }
      // Handle 403 Forbidden
      else if (error.response.status === 403) {
        console.error('Forbidden access. Please check your permissions.')
        // Try to refresh CSRF token
        try {
          const response = await apiClient.get('/auth/csrf/')
          const csrfToken = response.data?.csrfToken
          if (csrfToken) {
            document.cookie = `csrftoken=${csrfToken}; path=/; secure; samesite=none`
            // Retry the original request
            const config = error.config
            config.headers['X-CSRFToken'] = csrfToken
            return apiClient(config)
          }
        } catch (refreshError) {
          console.error('Failed to refresh CSRF token:', refreshError)
        }
      }
      // Handle 404 Not Found
      else if (error.response.status === 404) {
        console.error('Resource not found.')
      }
    }
    return Promise.reject(error)
  }
)

export default apiClient