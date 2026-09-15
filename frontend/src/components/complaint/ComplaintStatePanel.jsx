import { CalendarDays, Package, ShieldAlert } from 'lucide-react'
import { AIStamp } from '../dashboard/AppShell'

const fields = [
  ['product_name', 'Product name', Package],
  ['product_strength_or_grade', 'Strength / grade'],
  ['batch_number', 'Batch / lot'],
  ['manufacturing_date', 'Manufacturing date', CalendarDays],
  ['expiry_date', 'Expiry date', CalendarDays],
  ['affected_quantity', 'Affected quantity'],
  ['problem_description', 'Problem description'],
  ['reporter_information', 'Reporter information'],
]

function display(value) {
  if (value === null || value === undefined || value === '') return 'Not provided'
  return String(value)
}

export default function ComplaintStatePanel({ complaint, risk }) {
  return <section className="rounded-2xl border border-line bg-white p-5 shadow-panel sm:p-7">
    <div className="mb-6 flex items-start justify-between gap-4"><div><p className="mb-1 text-xs font-bold uppercase tracking-[0.16em] text-coral">Structured record</p><h2 className="font-display text-xl font-bold text-ink">Complaint details</h2></div><AIStamp /></div>
    <div className="grid gap-x-6 gap-y-5 sm:grid-cols-2">
      {fields.map(([key, label, Icon]) => <div key={key} className={key === 'problem_description' || key === 'reporter_information' ? 'sm:col-span-2' : ''}><div className="mb-1.5 flex items-center gap-2 text-[11px] font-bold uppercase tracking-wider text-slate-400">{Icon && <Icon size={13} />}{label}</div><div className={`min-h-11 rounded-xl border border-line/80 bg-paper px-3.5 py-3 text-sm leading-5 ${key === 'problem_description' ? 'whitespace-pre-wrap' : ''} ${display(complaint?.[key]) === 'Not provided' ? 'text-slate-400' : 'font-semibold text-ink'}`}>{display(complaint?.[key])}</div></div>)}
    </div>
    <div className="mt-7 border-t border-line pt-6"><div className="mb-4 flex items-center gap-2"><ShieldAlert size={18} className="text-coral" /><h3 className="font-display text-lg font-bold text-ink">AI risk assessment</h3></div><div className="grid gap-4 sm:grid-cols-3"><div><p className="label">Severity</p><div className="mt-2 flex items-center gap-2"><span className={`h-2.5 w-2.5 rounded-full ${risk?.severity_level === 'Critical' ? 'bg-red-500' : risk?.severity_level === 'Major' ? 'bg-coral' : 'bg-fern'}`} /><span className="font-display font-bold text-ink">{risk?.severity_level || 'Pending'}</span></div></div><div><p className="label">Suggested action</p><p className="mt-2 text-sm font-semibold leading-5 text-ink">{display(risk?.suggested_action)}</p></div><div><p className="label">Reasoning</p><p className="mt-2 text-sm leading-5 text-slate-600">{display(risk?.reasoning)}</p></div></div></div>
  </section>
}
