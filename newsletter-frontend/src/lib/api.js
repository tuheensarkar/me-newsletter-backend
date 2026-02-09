// lib/api.js
import axios from 'axios'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add authentication token if available
    const token = localStorage.getItem('authToken')
    if (token) {
      config.headers.Authorization = `Token ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('authToken')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Newsletter API endpoints
export const newsletterService = {
  getAll: () => api.get('/newsletters/').then(res => res.data.result),
  getRecent: () => api.get('/newsletters/recent/').then(res => res.data.result),
  getBySlug: (slug) => api.get(`/newsletters/${slug}/`).then(res => res.data.result),
  getPrevious: () => api.get('/newsletters/previous/').then(res => res.data.result),
}

// Subscription API endpoints
export const subscriptionService = {
  subscribe: (email) => api.post('/subscribe/', { email }).then(res => res.data),
}

// Health check endpoints
export const healthService = {
  getStatus: () => api.get('/status/').then(res => res.data),
  getHealth: () => api.get('/health/').then(res => res.data),
}

export default api