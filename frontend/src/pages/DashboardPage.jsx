import { FileText, Plus, ShieldCheck, TrendingUp } from 'lucide-react'
import { Link } from 'react-router-dom'
import { useEffect } from 'react'
import { EmptyState, PageHeading, PrimaryButton } from '../components/dashboard/AppShell'
import AppShell from '../components/dashboard/AppShell'
import ComplaintTable from '../components/dashboard/ComplaintTable'
import { useComplaint } from '../hooks/useComplaint'

export default function DashboardPage() {
  const { complaints, loading, error, loadComplaints } = useComplaint()
  useEffect(() => { loadComplaints().catch(() => {}) }, [loadComplaints])
  const active = complaints.filter((item) => !['resolved', 'closed'].includes(item.status)).length
  return <AppShell><PageHeading kicker="Operations overview" title="Complaint desk" description="A quiet view of every customer signal currently in your care." action={<Link to="/complaints/new"><PrimaryButton><Plus size={17} /> New complaint</PrimaryButton></Link>} />
    <div className="mb-8 grid gap-4 sm:grid-cols-3"><Metric icon={FileText} label="Total complaints" value={complaints.length} detail="Across your workspace" /><Metric icon={TrendingUp} label="Active cases" value={active} detail="Needs attention" /><Metric icon={ShieldCheck} label="AI assisted" value={complaints.length} detail="Structured records" /></div>
    {error && <div className="mb-5 rounded-xl bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div>}
    {loading ? <div className="rounded-2xl border border-line bg-white p-12 text-center text-sm text-slate-500">Loading complaint desk...</div> : complaints.length ? <ComplaintTable complaints={complaints} /> : <EmptyState onCreate={() => { window.location.href = '/complaints/new' }} />}
  </AppShell>
}

function Metric({ icon: Icon, label, value, detail }) { return <div className="rounded-2xl border border-line bg-white p-5 shadow-panel"><div className="flex items-start justify-between"><div><p className="text-xs font-bold uppercase tracking-wider text-slate-400">{label}</p><p className="mt-3 font-display text-3xl font-bold text-ink">{value}</p><p className="mt-1 text-sm text-slate-500">{detail}</p></div><span className="grid h-10 w-10 place-items-center rounded-xl bg-mint text-fern"><Icon size={19} /></span></div></div> }
