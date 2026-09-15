import { ClipboardList, LogOut, Plus, Sparkles } from 'lucide-react'
import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'

export default function AppShell({ children }) {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  return (
    <div className="min-h-screen bg-paper">
      <header className="sticky top-0 z-20 border-b border-line/80 bg-paper/90 backdrop-blur-xl">
        <div className="mx-auto flex max-w-[1440px] items-center justify-between px-5 py-4 lg:px-8">
          <NavLink to="/dashboard" className="flex items-center gap-3">
            <span className="grid h-10 w-10 place-items-center rounded-xl bg-ink font-display text-lg font-bold text-white shadow-sm">A</span>
            <span><span className="block font-display text-lg font-bold tracking-tight">AIVOA</span><span className="block text-[10px] font-bold uppercase tracking-[0.2em] text-fern">Complaint Copilot</span></span>
          </NavLink>
          <div className="flex items-center gap-3">
            <span className="hidden text-right sm:block"><span className="block text-sm font-semibold text-ink">{user?.full_name}</span><span className="block text-xs text-slate-500">{user?.email}</span></span>
            <button onClick={() => { logout(); navigate('/login') }} className="grid h-10 w-10 place-items-center rounded-xl border border-line bg-white text-slate-500 transition hover:border-coral hover:text-coral" title="Sign out" aria-label="Sign out"><LogOut size={17} /></button>
          </div>
        </div>
      </header>
      <main className="mx-auto max-w-[1440px] px-5 py-7 lg:px-8">{children}</main>
    </div>
  )
}

export function PageHeading({ kicker, title, description, action }) {
  return <div className="mb-8 flex flex-col justify-between gap-5 sm:flex-row sm:items-end"><div><p className="mb-2 text-xs font-bold uppercase tracking-[0.18em] text-coral">{kicker}</p><h1 className="font-display text-3xl font-bold tracking-tight text-ink sm:text-4xl">{title}</h1>{description && <p className="mt-2 max-w-2xl text-slate-500">{description}</p>}</div>{action}</div>
}

export function PrimaryButton({ children, onClick, type = 'button', disabled = false, className = '' }) {
  return <button type={type} onClick={onClick} disabled={disabled} className={`inline-flex items-center justify-center gap-2 rounded-xl bg-fern px-4 py-2.5 text-sm font-bold text-white shadow-sm transition hover:bg-ink disabled:cursor-not-allowed disabled:opacity-50 ${className}`}>{children}</button>
}

export function EmptyState({ onCreate }) {
  return <div className="rounded-2xl border border-dashed border-line bg-white px-6 py-16 text-center"><div className="mx-auto grid h-14 w-14 place-items-center rounded-2xl bg-mint text-fern"><ClipboardList size={26} /></div><h2 className="mt-5 font-display text-xl font-bold text-ink">Your complaint desk is clear</h2><p className="mx-auto mt-2 max-w-sm text-sm leading-6 text-slate-500">Start with a natural-language report and let the copilot structure the details for you.</p><PrimaryButton onClick={onCreate} className="mt-6"><Plus size={16} /> New complaint</PrimaryButton></div>
}

export function AIStamp() { return <span className="inline-flex items-center gap-1.5 rounded-full bg-mint px-2.5 py-1 text-[11px] font-bold uppercase tracking-wider text-fern"><Sparkles size={12} /> AI assisted</span> }
