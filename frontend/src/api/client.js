import axios from 'axios'

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL?.trim()

if (!apiBaseUrl) {
  throw new Error('VITE_API_BASE_URL is required to connect to the API.')
}

const client = axios.create({
  baseURL: apiBaseUrl.replace(/\/$/, ''),
  headers: { 'Content-Type': 'application/json' },
})

client.interceptors.request.use((config) => {
  const token = localStorage.getItem('aivoa_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('aivoa_token')
      window.dispatchEvent(new Event('aivoa:unauthorized'))
    }
    return Promise.reject(error)
  },
)

export const getApiError = (error, fallback = 'Something went wrong. Please try again.') => {
  const detail = error?.response?.data?.detail
  if (Array.isArray(detail)) return detail.map((item) => item.msg || item).join(', ')
  if (typeof detail === 'string') return detail
  return error?.message || fallback
}

export default client
