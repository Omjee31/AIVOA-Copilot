import client from './client'

export const logComplaint = (message) =>
  client.post('/api/chat/log', { message }).then(({ data }) => data)

export const editComplaintWithAI = (complaintId, message) =>
  client.post('/api/chat/edit', {
    complaint_id: complaintId,
    message,
  }).then(({ data }) => data)