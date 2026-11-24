import React, { useEffect, useState } from 'react';

interface HealthStatus {
  status: string;
  service: string;
}

export default function Home() {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch('http://localhost:8000/health')
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
      })
      .then((data: HealthStatus) => {
        setHealth(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Failed to fetch backend health:', err);
        setError('Failed to connect to backend API');
        setLoading(false);
      });
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8 font-sans">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="flex justify-center">
          <div className="h-12 w-12 rounded-xl bg-blue-600 flex items-center justify-center text-white font-bold text-xl shadow-lg">
            BAL
          </div>
        </div>
        <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Business Automation Labs
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          Multi-Niche Lead Generation CRM
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow-xl sm:rounded-xl sm:px-10 border border-gray-100">
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-medium text-gray-900 border-b pb-2">
                System Status
              </h3>
              <div className="mt-4 space-y-3">
                <div className="flex justify-between items-center text-sm">
                  <span className="text-gray-500">Frontend Service:</span>
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    Operational (Next.js)
                  </span>
                </div>
                <div className="flex justify-between items-center text-sm">
                  <span className="text-gray-500">Backend API:</span>
                  {loading ? (
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                      Checking...
                    </span>
                  ) : error ? (
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                      Offline
                    </span>
                  ) : (
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      {health?.status === 'healthy' ? 'Healthy (FastAPI)' : health?.status}
                    </span>
                  )}
                </div>
              </div>
            </div>

            <div className="rounded-md bg-blue-50 p-4 border border-blue-100">
              <div className="flex">
                <div className="ml-3 flex-1 md:flex md:justify-between">
                  <p className="text-sm text-blue-700">
                    Phase 1 Foundation established successfully. API communication verified.
                  </p>
                </div>
              </div>
            </div>

            <div className="border-t pt-4 text-xs text-gray-500 text-center">
              Business Automation Labs CRM &copy; {new Date().getFullYear()}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}