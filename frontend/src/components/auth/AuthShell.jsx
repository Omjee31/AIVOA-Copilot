import { ShieldCheck } from 'lucide-react'

export default function AuthShell({ eyebrow, title, description, children, footer }) {
  return (
    <main className="paper-grid flex min-h-screen items-center justify-center px-5 py-10">
      <div className="grid w-full max-w-5xl overflow-hidden rounded-[28px] border border-line bg-white shadow-panel md:grid-cols-[0.9fr_1.1fr]">
        <section className="relative hidden overflow-hidden bg-ink p-10 text-white md:block">
          <div className="absolute -right-24 -top-24 h-64 w-64 rounded-full border-[28px] border-coral/25" />
          <div className="absolute -bottom-20 -left-16 h-56 w-56 rounded-full border-[22px] border-mint/20" />
          <div className="relative flex h-full flex-col justify-between">
            <div>
              <div className="mb-16 flex items-center gap-3 text-sm font-semibold tracking-[0.18em] text-mint">
                <span className="grid h-9 w-9 place-items-center rounded-xl bg-coral text-white">A</span>
                AIVOA
              </div>
              <p className="max-w-xs font-display text-4xl font-semibold leading-tight">Complaint intelligence, with a human point of view.</p>
              <p className="mt-5 max-w-sm text-base leading-7 text-white/65">Capture the signal, understand the risk, and keep every decision traceable.</p>
            </div>
            <div className="flex items-center gap-3 text-sm text-white/65">
              <ShieldCheck size={18} className="text-mint" /> Private workspace for customer care teams
            </div>
          </div>
        </section>
        <section className="p-7 sm:p-12">
          <div className="mb-9 md:hidden">
            <div className="flex items-center gap-3 text-sm font-bold tracking-[0.18em] text-fern"><span className="grid h-9 w-9 place-items-center rounded-xl bg-coral text-white">A</span>AIVOA</div>
          </div>
          <p className="mb-3 text-xs font-bold uppercase tracking-[0.18em] text-coral">{eyebrow}</p>
          <h1 className="font-display text-3xl font-bold tracking-tight text-ink">{title}</h1>
          <p className="mt-3 max-w-md leading-6 text-slate-500">{description}</p>
          <div className="mt-8">{children}</div>
          {footer && <div className="mt-7 border-t border-line pt-6 text-sm text-slate-500">{footer}</div>}
        </section>
      </div>
    </main>
  )
}
