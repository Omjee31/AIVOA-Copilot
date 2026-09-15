import client from './client'

export const listComplaints = () =>
  client.get('/api/complaints').then(({ data }) => data)

export const getComplaint = (id) =>
  client.get(`/api/complaints/${id}`).then(({ data }) => data)

export const createComplaint = (payload) =>
  client.post('/api/complaints', payload).then(({ data }) => data)

export const updateComplaint = (id, payload) =>
  client.put(`/api/complaints/${id}`, payload).then(({ data }) => data)

export const deleteComplaint = (id) =>
  client.delete(`/api/complaints/${id}`)
