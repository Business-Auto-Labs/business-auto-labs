import { useCallback, useEffect, useRef, useState } from "react";
import { API_BASE_URL, fetchBackendHealth } from "../src/lib/api";

type HealthState =
  | { status: "checking" }
  | { status: "healthy" }
  | { status: "unavailable"; message: string };

export function ApiHealthCard() {
  const [state, setState] = useState<HealthState>({ status: "checking" });
  const activeRequest = useRef<AbortController | null>(null);

  const checkHealth = useCallback(async () => {
    activeRequest.current?.abort();
    const controller = new AbortController();
    activeRequest.current = controller;
    let timedOut = false;

    setState({ status: "checking" });
    const timeoutId = window.setTimeout(() => {
      timedOut = true;
      controller.abort();
    }, 8000);

    try {
      await fetchBackendHealth(controller.signal);
      if (!controller.signal.aborted) setState({ status: "healthy" });
    } catch (error) {
      if (!controller.signal.aborted || timedOut) {
        const message = timedOut
          ? "The health check timed out. Confirm the backend is running, then retry."
          : error instanceof Error && error.message.startsWith("Health check failed")
            ? error.message + " Check the backend terminal, then retry."
            : "Could not connect. Confirm the backend is running and the configured address is correct.";
        setState({ status: "unavailable", message });
      }
    } finally {
      window.clearTimeout(timeoutId);
      if (activeRequest.current === controller) activeRequest.current = null;
    }
  }, []);

  useEffect(() => {
    void checkHealth();
    return () => activeRequest.current?.abort();
  }, [checkHealth]);

  const isHealthy = state.status === "healthy";
  const isChecking = state.status === "checking";
  const label = isChecking ? "Checking" : isHealthy ? "Healthy" : "Unavailable";
  const statusClasses = isChecking
    ? "border-amber-200 bg-amber-50 text-amber-800"
    : isHealthy
      ? "border-emerald-200 bg-emerald-50 text-emerald-800"
      : "border-rose-200 bg-rose-50 text-rose-800";
  const dotClasses = isChecking ? "bg-amber-500" : isHealthy ? "bg-emerald-600" : "bg-rose-600";

  return (
    <article aria-labelledby="backend-card-title" className="rounded-2xl border border-slate-200 bg-white p-5 sm:p-6">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h3 className="text-base font-semibold text-slate-950" id="backend-card-title">Backend API</h3>
          <p className="mt-1 text-sm text-slate-600">FastAPI health endpoint</p>
        </div>
        <span
          className={"inline-flex min-h-8 items-center gap-2 rounded-full border px-3 text-xs font-semibold " + statusClasses}
          role="status"
          aria-live="polite"
          aria-atomic="true"
        >
          <span aria-hidden="true" className={"h-2 w-2 rounded-full " + dotClasses} />
          {label}
        </span>
      </div>

      <dl className="mt-6 border-t border-slate-100 pt-4">
        <dt className="text-xs font-medium uppercase tracking-wide text-slate-500">Health check URL</dt>
        <dd className="mt-2 break-all font-mono text-xs text-slate-700">{API_BASE_URL}/health</dd>
      </dl>

      {state.status === "unavailable" ? (
        <p className="mt-4 rounded-lg border border-rose-200 bg-rose-50 px-3 py-2.5 text-sm leading-5 text-rose-800" role="alert">
          {state.message}
        </p>
      ) : null}

      <button
        className="mt-5 inline-flex min-h-11 items-center justify-center rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition-colors hover:bg-slate-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-primary focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-60"
        disabled={isChecking}
        onClick={() => void checkHealth()}
        type="button"
      >
        {isChecking ? "Checking..." : "Retry connection"}
      </button>
    </article>
  );
}
