import type { ReactNode } from "react";

type Props = { children: ReactNode };

export function DashboardShell({ children }: Props) {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-950">
      <a
        className="sr-only rounded-md bg-white px-4 py-3 font-medium text-brand-primary focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-primary focus-visible:ring-offset-2"
        href="#main-content"
      >
        Skip to main content
      </a>

      <aside className="border-b border-slate-200 bg-white px-4 py-4 sm:px-6 lg:fixed lg:inset-y-0 lg:left-0 lg:z-20 lg:flex lg:w-64 lg:flex-col lg:border-b-0 lg:border-r lg:px-6">
        <div className="flex items-center gap-3">
          <div aria-hidden="true" className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-brand-primary text-sm font-bold tracking-wide text-white">
            BA
          </div>
          <div className="min-w-0">
            <p className="truncate text-sm font-semibold text-slate-950">Business Automation Labs</p>
            <p className="mt-0.5 text-xs text-slate-500">CRM workspace</p>
          </div>
        </div>

        <nav aria-label="Primary navigation" className="mt-4 grid grid-cols-2 gap-2 sm:max-w-sm lg:mt-10 lg:max-w-none lg:grid-cols-1">
          <a
            aria-current="page"
            className="flex min-h-11 items-center gap-3 rounded-lg bg-blue-50 px-3 text-sm font-semibold text-blue-800 transition-colors hover:bg-blue-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-primary focus-visible:ring-offset-2"
            href="#overview"
          >
            <span aria-hidden="true" className="h-1.5 w-1.5 rounded-full bg-brand-primary" />
            Overview
          </a>
          <a
            className="flex min-h-11 items-center gap-3 rounded-lg px-3 text-sm font-medium text-slate-600 transition-colors hover:bg-slate-100 hover:text-slate-950 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-primary focus-visible:ring-offset-2"
            href="#system-health"
          >
            System health
          </a>
        </nav>

        <div className="mt-4 hidden border-t border-slate-200 pt-4 text-xs leading-5 text-slate-500 lg:mt-auto lg:block">
          Foundation workspace<br />Local development
        </div>
      </aside>

      <div className="min-w-0 lg:ml-64">
        <header className="flex min-h-16 items-center justify-between gap-4 border-b border-slate-200 bg-white px-4 sm:px-6 lg:px-10">
          <div>
            <p className="text-xs font-medium text-slate-500">Workspace / Overview</p>
            <p className="mt-1 text-sm font-semibold text-slate-800">Business Automation Labs CRM</p>
          </div>
          <span className="inline-flex min-h-8 items-center rounded-full border border-slate-200 bg-slate-50 px-3 text-xs font-medium text-slate-600">
            Local setup
          </span>
        </header>

        <main className="mx-auto w-full max-w-7xl px-4 py-8 sm:px-6 sm:py-10 lg:px-10" id="main-content" tabIndex={-1}>
          {children}
        </main>
      </div>
    </div>
  );
}
