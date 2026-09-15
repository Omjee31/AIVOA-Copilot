import client from './client'

export const extractDocument = (complaintId, file) => {
  const formData = new FormData()
  if (complaintId) formData.append('complaint_id', complaintId)
  formData.append('file', file)
  return client.post('/document/extract', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }).then(({ data }) => data)
}

export const getAuditHistory = (complaintId) =>
  client.get(`/audit/${complaintId}`).then(({ data }) => data)
