'use client';

import { useState, useEffect } from 'react';
import { getSites, decideLaunch, LaunchSite, LaunchResponse } from '@/lib/api';

export default function Home() {
  const [sites, setSites] = useState<LaunchSite[]>([]);
  const [selectedSite, setSelectedSite] = useState('');
  const [launchTime, setLaunchTime] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<LaunchResponse | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    // Load sites on mount
    getSites().then(setSites).catch(console.error);

    // Set default launch time to 1 hour from now
    const now = new Date();
    now.setHours(now.getHours() + 1);
    const isoTime = now.toISOString().slice(0, 16);
    setLaunchTime(isoTime);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await decideLaunch({
        site_code: selectedSite,
        launch_time: new Date(launchTime).toISOString(),
      });
      setResult(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const getVerdictColor = (verdict: string) => {
    switch (verdict) {
      case 'GO':
        return 'text-green-600 dark:text-green-400';
      case 'MARGINAL':
        return 'text-yellow-600 dark:text-yellow-400';
      case 'NO-GO':
        return 'text-red-600 dark:text-red-400';
      default:
        return 'text-gray-600 dark:text-gray-400';
    }
  };

  const getVerdictBg = (verdict: string) => {
    switch (verdict) {
      case 'GO':
        return 'bg-green-100 dark:bg-green-900/30';
      case 'MARGINAL':
        return 'bg-yellow-100 dark:bg-yellow-900/30';
      case 'NO-GO':
        return 'bg-red-100 dark:bg-red-900/30';
      default:
        return 'bg-gray-100 dark:bg-gray-900/30';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 text-white p-8">
      <div className="max-w-4xl mx-auto">
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
            🚀 Launch Go/No-Go Advisor
          </h1>
          <p className="text-gray-400 text-lg">
            AI-powered launch readiness assessment for the Big Refueler
          </p>
        </header>

        <form onSubmit={handleSubmit} className="bg-slate-800/50 rounded-2xl p-8 mb-8 backdrop-blur">
          <div className="mb-6">
            <label className="block text-sm font-medium mb-2">Launch Site</label>
            <select
              value={selectedSite}
              onChange={(e) => setSelectedSite(e.target.value)}
              required
              className="w-full px-4 py-3 bg-slate-700 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
            >
              <option value="">Select a launch site</option>
              {sites.map((site) => (
                <option key={site.code} value={site.code}>
                  {site.name} ({site.code})
                </option>
              ))}
            </select>
          </div>

          <div className="mb-6">
            <label className="block text-sm font-medium mb-2">Launch Time (UTC)</label>
            <input
              type="datetime-local"
              value={launchTime}
              onChange={(e) => setLaunchTime(e.target.value)}
              required
              className="w-full px-4 py-3 bg-slate-700 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
            />
          </div>

          <button
            type="submit"
            disabled={loading || !selectedSite}
            className="w-full bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 disabled:from-gray-600 disabled:to-gray-700 disabled:cursor-not-allowed py-4 rounded-lg font-semibold text-lg transition-all duration-200 shadow-lg"
          >
            {loading ? 'Analyzing...' : 'Check Launch Conditions'}
          </button>
        </form>

        {error && (
          <div className="bg-red-900/30 border border-red-500 rounded-lg p-4 mb-8">
            <p className="text-red-400">{error}</p>
          </div>
        )}

        {result && (
          <div className={`rounded-2xl p-8 ${getVerdictBg(result.verdict)} border border-gray-700`}>
            <div className="flex items-center justify-between mb-6">
              <h2 className={`text-4xl font-bold ${getVerdictColor(result.verdict)}`}>
                {result.verdict}
              </h2>
              <div className="text-right">
                <div className="text-sm text-gray-400">Risk Score</div>
                <div className={`text-3xl font-bold ${getVerdictColor(result.verdict)}`}>
                  {result.risk_score}/100
                </div>
              </div>
            </div>

            <div className="mb-6">
              <h3 className="text-lg font-semibold mb-2">Analysis</h3>
              <p className="text-gray-300">{result.why}</p>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-2">Rule Citations</h3>
              <ul className="list-disc list-inside space-y-1">
                {result.rule_citations.map((citation, idx) => (
                  <li key={idx} className="text-gray-300 text-sm">
                    {citation}
                  </li>
                ))}
              </ul>
            </div>

            {result.data && (
              <details className="mt-6">
                <summary className="cursor-pointer text-sm text-gray-400 hover:text-gray-300">
                  View Raw Data
                </summary>
                <pre className="mt-2 p-4 bg-slate-900/50 rounded-lg overflow-auto text-xs text-gray-300">
                  {JSON.stringify(result.data, null, 2)}
                </pre>
              </details>
            )}
          </div>
        )}

        <footer className="text-center mt-12 text-gray-500 text-sm">
          <p>Powered by Meteomatics Weather API, NOAA SWPC, and Space-Track.org</p>
        </footer>
      </div>
    </div>
  );
}
