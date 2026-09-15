import client from './client'

export const login = (email, password) =>
  client.post('/auth/login', new URLSearchParams({ username: email, password }), {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  }).then(({ data }) => data)

export const register = (payload) => client.post('/auth/register', payload).then(({ data }) => data)
export const getMe = () => client.get('/auth/me').then(({ data }) => data)
