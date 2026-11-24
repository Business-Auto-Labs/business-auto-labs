import { Component, type ErrorInfo, type ReactNode } from "react";

type Props = { children: ReactNode };
type State = { hasError: boolean };

export class AppErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false };

  static getDerivedStateFromError(): State {
    return { hasError: true };
  }

  componentDidCatch(error: Error, info: ErrorInfo): void {
    console.error("Unhandled application rendering error", error, info);
  }

  render(): ReactNode {
    if (this.state.hasError) {
      return (
        <main className="flex min-h-screen items-center justify-center bg-slate-50 px-4 py-12">
          <section className="w-full max-w-lg rounded-2xl border border-slate-200 bg-white p-6 sm:p-8" role="alert">
            <p className="text-sm font-semibold uppercase tracking-wide text-rose-700">Application error</p>
            <h1 className="mt-3 text-2xl font-semibold tracking-tight text-slate-950">This page could not be displayed.</h1>
            <p className="mt-2 text-sm leading-6 text-slate-600">
              Reload the workspace. If the problem continues, check the frontend terminal for details.
            </p>
            <button
              className="mt-6 inline-flex min-h-11 items-center justify-center rounded-lg bg-brand-primary px-4 py-2 text-sm font-semibold text-white transition-colors hover:bg-blue-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-primary focus-visible:ring-offset-2"
              onClick={() => window.location.reload()}
              type="button"
            >
              Reload workspace
            </button>
          </section>
        </main>
      );
    }

    return this.props.children;
  }
}
