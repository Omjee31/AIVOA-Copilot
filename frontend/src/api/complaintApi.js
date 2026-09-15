import client from './client'

export const listComplaints = () => client.get('/complaints').then(({ data }) => data)
export const getComplaint = (id) => client.get(`/complaints/${id}`).then(({ data }) => data)
export const createComplaint = (payload) => client.post('/complaints', payload).then(({ data }) => data)
export const updateComplaint = (id, payload) => client.put(`/complaints/${id}`, payload).then(({ data }) => data)
export const deleteComplaint = (id) => client.delete(`/complaints/${id}`)
