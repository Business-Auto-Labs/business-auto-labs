import type { AppProps } from "next/app";
import { AppErrorBoundary } from "../components/AppErrorBoundary";
import "../styles/globals.css";

export default function App({ Component, pageProps }: AppProps) {
  return (
    <AppErrorBoundary>
      <Component {...pageProps} />
    </AppErrorBoundary>
  );
}
