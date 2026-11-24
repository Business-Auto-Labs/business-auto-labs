export const API_BASE_URL = (
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000"
).replace(/\/+$/, "");

export interface BackendHealth {
  status: "healthy";
  service: "backend";
}

export async function fetchBackendHealth(signal: AbortSignal): Promise<BackendHealth> {
  const response = await fetch(API_BASE_URL + "/health", {
    method: "GET",
    headers: { Accept: "application/json" },
    cache: "no-store",
    signal,
  });

  if (!response.ok) {
    throw new Error("Health check failed with HTTP " + response.status + ".");
  }

  const payload: unknown = await response.json();
  if (!payload || typeof payload !== "object" || Array.isArray(payload)) {
    throw new Error("The backend returned an invalid health response.");
  }

  const body = payload as Record<string, unknown>;
  if (body.status !== "healthy" || body.service !== "backend") {
    throw new Error("The backend returned an unexpected health status.");
  }

  return { status: "healthy", service: "backend" };
}
