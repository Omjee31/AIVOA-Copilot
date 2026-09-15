import { useCallback, useState } from 'react'
import { getApiError } from '../api/client'
import { getComplaint, listComplaints } from '../api/complaintApi'

export function useComplaint() {
  const [complaints, setComplaints] = useState([])
  const [complaint, setComplaint] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const loadComplaints = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const data = await listComplaints()
      setComplaints(data)
      return data
    } catch (loadError) {
      setError(getApiError(loadError, 'Could not load complaints.'))
      throw loadError
    } finally {
      setLoading(false)
    }
  }, [])

  const loadComplaint = useCallback(async (id) => {
    setLoading(true)
    setError('')
    try {
      const data = await getComplaint(id)
      setComplaint(data)
      return data
    } catch (loadError) {
      setError(getApiError(loadError, 'Could not load complaint.'))
      throw loadError
    } finally {
      setLoading(false)
    }
  }, [])

  return { complaints, complaint, setComplaint, loading, error, loadComplaints, loadComplaint }
}
