import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import AuthShell from '../components/auth/AuthShell'
import { getApiError } from '../api/client'
import { useAuth } from '../context/AuthContext'

export default function LoginPage() {
  const { login } = useAuth(); const navigate = useNavigate(); const location = useLocation(); const [form, setForm] = useState({ email: '', password: '' }); const [error, setError] = useState(''); const [loading, setLoading] = useState(false)
  const submit = async (event) => { event.preventDefault(); setLoading(true); setError(''); try { await login(form.email, form.password); navigate(location.state?.from || '/dashboard') } catch (submitError) { setError(getApiError(submitError, 'Could not sign in. Check your credentials.')) } finally { setLoading(false) } }
  return <AuthShell eyebrow="Secure workspace" title="Welcome back" description="Sign in to continue reviewing customer complaints with an accountable AI copilot." footer={<>New to AIVOA? <Link className="font-bold text-fern hover:text-ink" to="/register">Create an account</Link></>}><form onSubmit={submit} className="space-y-5"><div><label className="label" htmlFor="email">Email</label><input id="email" required type="email" value={form.email} onChange={(event) => setForm({ ...form, email: event.target.value })} className="input" placeholder="you@company.com" /></div><div><label className="label" htmlFor="password">Password</label><input id="password" required type="password" value={form.password} onChange={(event) => setForm({ ...form, password: event.target.value })} className="input" placeholder="Your password" /></div>{error && <p className="rounded-xl bg-red-50 px-3 py-2.5 text-sm text-red-700">{error}</p>}<button disabled={loading} className="w-full rounded-xl bg-ink px-4 py-3 text-sm font-bold text-white transition hover:bg-fern disabled:opacity-50">{loading ? 'Signing in...' : 'Sign in to workspace'}</button></form></AuthShell>
}
