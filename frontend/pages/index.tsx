import Head from "next/head";
import { ApiHealthCard } from "../components/ApiHealthCard";
import { DashboardShell } from "../components/DashboardShell";

export default function HomePage() {
  return (
    <>
      <Head>
        <title>Overview | Business Automation Labs CRM</title>
        <meta name="description" content="Workspace status for the Business Automation Labs CRM foundation." />
      </Head>

      <DashboardShell>
        <section aria-labelledby="overview-title" id="overview">
          <p className="text-sm font-semibold text-brand-primary">Workspace</p>
          <h1 className="mt-2 text-3xl font-semibold tracking-tight text-slate-950 sm:text-4xl" id="overview-title">
            System overview
          </h1>
          <p className="mt-3 max-w-2xl text-base leading-7 text-slate-600">
            Check the application services connected to this local workspace.
          </p>
        </section>

        <section aria-labelledby="system-health-title" className="mt-8 sm:mt-10" id="system-health">
          <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <h2 className="text-lg font-semibold text-slate-950" id="system-health-title">Application services</h2>
              <p className="mt-1 text-sm text-slate-600">
                Backend status is checked from this page and can be retried at any time.
              </p>
            </div>
            <p className="text-xs font-medium text-slate-500">Foundation environment</p>
          </div>

          <div className="mt-4 grid gap-4 lg:grid-cols-2">
            <article className="rounded-2xl border border-slate-200 bg-white p-5 sm:p-6">
              <div className="flex flex-wrap items-start justify-between gap-4">
                <div>
                  <h3 className="text-base font-semibold text-slate-950">Frontend</h3>
                  <p className="mt-1 text-sm text-slate-600">Next.js workspace interface</p>
                </div>
                <span className="inline-flex min-h-8 items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50 px-3 text-xs font-semibold text-emerald-800">
                  <span aria-hidden="true" className="h-2 w-2 rounded-full bg-emerald-600" />
                  Serving page
                </span>
              </div>
              <p className="mt-6 border-t border-slate-100 pt-4 text-sm leading-6 text-slate-600">
                The frontend is serving this workspace. The backend connection is reported separately.
              </p>
            </article>

            <ApiHealthCard />
          </div>
        </section>
      </DashboardShell>
    </>
  );
}
