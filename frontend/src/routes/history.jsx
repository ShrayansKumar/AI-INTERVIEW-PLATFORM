import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import Sidebar from '../components/dashboard/Sidebar'
import apiClient from '../lib/apiClient'

function HistoryPage() {
  const [sessions, setSessions] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    apiClient.get('/api/v1/analytics/score-trend')
      .then((res) => {
        // Show most recent first
        const sorted = [...res.data].sort((a, b) => new Date(b.date) - new Date(a.date))
        setSessions(sorted)
      })
      .catch((err) => setError(err.response?.data?.detail || 'Could not load history.'))
      .finally(() => setLoading(false))
  }, [])

  const formatDate = (isoString) => {
    return new Date(isoString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
    })
  }

  const scoreColor = (score) => {
    if (score >= 7) return 'text-accent'
    if (score >= 5) return 'text-amber-400'
    return 'text-red-400'
  }

  return (
    <div className="flex">
      <Sidebar />
      <main className="flex-1 p-8 bg-bg-base min-h-screen">
        <h1 className="text-2xl font-bold text-text-primary mb-1">Interview History</h1>
        <p className="text-text-secondary mb-8">All your completed practice sessions</p>

        {loading && <p className="text-text-secondary">Loading...</p>}
        {error && <p className="text-red-400">{error}</p>}

        {!loading && sessions.length === 0 && (
          <div className="bg-bg-card border border-border rounded-2xl p-8 max-w-md text-center">
            <p className="text-text-secondary mb-4">No completed interviews yet.</p>
            <Link
              to="/resume-upload"
              className="inline-block bg-accent text-accent-text font-semibold rounded-lg px-5 py-2.5 hover:opacity-90 transition-opacity"
            >
              Start your first interview
            </Link>
          </div>
        )}

        <div className="space-y-3 max-w-2xl">
          {sessions.map((session) => (
            <Link
              key={session.session_id}
              to={`/report/${session.session_id}`}
              className="flex items-center justify-between bg-bg-card border border-border rounded-xl p-4 hover:bg-bg-card-hover transition-colors"
            >
              <div>
                <p className="text-text-primary font-medium">
                  {formatDate(session.date)}
                </p>
                <p className="text-text-secondary text-xs mt-0.5">
                  Session {session.session_id.slice(0, 8)}...
                </p>
              </div>
              <p className={`text-xl font-bold ${scoreColor(session.score)}`}>
                {session.score} / 10
              </p>
            </Link>
          ))}
        </div>
      </main>
    </div>
  )
}

export default HistoryPage