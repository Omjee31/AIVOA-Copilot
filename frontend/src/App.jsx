import { Navigate, Route, Routes, useLocation } from 'react-router-dom'
import DashboardPage from './pages/DashboardPage'
import NewComplaintPage from './pages/NewComplaintPage'
import ComplaintDetailsPage from './pages/ComplaintDetailsPage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import { useAuth } from './context/AuthContext'

function ProtectedRoute({ children }) {
  const { user, loading } = useAuth(); const location = useLocation()
  if (loading) return <div className="grid min-h-screen place-items-center bg-paper text-sm text-slate-500">Loading workspace...</div>
  return user ? children : <Navigate to="/login" replace state={{ from: location.pathname }} />
}

export default function App() {
  return <Routes><Route path="/login" element={<LoginPage />} /><Route path="/register" element={<RegisterPage />} /><Route path="/dashboard" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} /><Route path="/complaints/new" element={<ProtectedRoute><NewComplaintPage /></ProtectedRoute>} /><Route path="/complaints/:id" element={<ProtectedRoute><ComplaintDetailsPage /></ProtectedRoute>} /><Route path="*" element={<Navigate to="/dashboard" replace />} /></Routes>
}
