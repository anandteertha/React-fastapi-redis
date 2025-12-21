import axios from 'axios'
import toast from 'react-hot-toast'

export const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    toast.error('Request failed. Please try again.')
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    // Show success toast for POST, PUT, DELETE requests
    const method = response.config.method?.toUpperCase()
    if (method === 'POST' || method === 'PUT' || method === 'DELETE') {
      const message = getSuccessMessage(method, response.config.url)
      if (message) {
        toast.success(message)
      }
    }
    return response
  },
  (error) => {
    const status = error.response?.status
    const message = error.response?.data?.detail || error.message || 'An error occurred'
    
    // Handle 401 - redirect to login
    if (status === 401) {
      localStorage.removeItem('token')
      toast.error('Session expired. Please login again.')
      window.location.href = '/login'
      return Promise.reject(error)
    }
    
    // Show error toast
    toast.error(message)
    return Promise.reject(error)
  }
)

// Helper function to get success messages
function getSuccessMessage(method, url) {
  if (!url) return null
  
  if (url.includes('/auth/register')) {
    return 'Account created successfully!'
  }
  if (url.includes('/auth/login')) {
    return 'Login successful!'
  }
  if (url.includes('/meals')) {
    return method === 'POST' ? 'Meal added successfully!' : method === 'PUT' ? 'Meal updated!' : 'Meal deleted!'
  }
  if (url.includes('/preferences')) {
    return 'Preferences saved!'
  }
  if (url.includes('/goals')) {
    return method === 'POST' ? 'Goal created!' : method === 'PUT' ? 'Goal updated!' : 'Goal deleted!'
  }
  if (url.includes('/foods')) {
    return method === 'POST' ? 'Food added!' : method === 'PUT' ? 'Food updated!' : 'Food deleted!'
  }
  
  return null // Don't show toast for GET requests or unknown endpoints
}

