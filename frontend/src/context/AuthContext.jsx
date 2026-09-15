import { createContext, useContext, useEffect, useState } from 'react'
import { getMe, login as loginRequest, register as registerRequest } from '../api/authApi'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem('aivoa_token'))
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(Boolean(token))

  useEffect(() => {
    const handleUnauthorized = () => {
      setToken(null)
      setUser(null)
    }
    window.addEventListener('aivoa:unauthorized', handleUnauthorized)
    return () => window.removeEventListener('aivoa:unauthorized', handleUnauthorized)
  }, [])

  useEffect(() => {
    if (!token) {
      setLoading(false)
      return
    }
    getMe()
      .then(setUser)
      .catch(() => {
        localStorage.removeItem('aivoa_token')
        setToken(null)
        setUser(null)
      })
      .finally(() => setLoading(false))
  }, [token])

  const login = async (email, password) => {
    const data = await loginRequest(email, password)
    localStorage.setItem('aivoa_token', data.access_token)
    setToken(data.access_token)
    const profile = await getMe()
    setUser(profile)
  }

  const register = async (payload) => {
    await registerRequest(payload)
    await login(payload.email, payload.password)
  }

  const logout = () => {
    localStorage.removeItem('aivoa_token')
    setToken(null)
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
