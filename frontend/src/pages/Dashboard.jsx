import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api/client'
import { useAuth } from '../context/AuthContext'

function ScoreBadge({ score }) {
  const color =
    score >= 70 ? 'text-emerald-400 bg-emerald-400/10 border-emerald-400/30' :
    score >= 45 ? 'text-amber-400 bg-amber-400/10 border-amber-400/30' :
    'text-red-400 bg-red-400/10 border-red-400/30'
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold border ${color}`}>
      {Math.round(score)}%
    </span>
  )
}

export default function Dashboard() {
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [expanded, setExpanded] = useState(null)
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    api.get('/results')
      .then(({ data }) => setResults(data))
      .catch(() => setError('Failed to load results.'))
      .finally(() => setLoading(false))
  }, [])

  function handleLogout() {
    logout()
    navigate('/login')
  }

  return (
    <div className="min-h-screen px-4 py-8 animate-fade-in">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
          <div>
            <h1 className="text-3xl font-bold text-white">Dashboard</h1>
            <p className="text-gray-400 mt-1">
              Signed in as <span className="text-brand-400">{user?.email}</span>
            </p>
          </div>
          <div className="flex gap-3">
            <button onClick={() => navigate('/match')} className="btn-primary">
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
              </svg>
              New Analysis
            </button>
            <button onClick={handleLogout} className="btn-secondary">
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              Sign Out
            </button>
          </div>
        </div>

        {/* Stats Bar */}
        {results.length > 0 && (
          <div className="grid grid-cols-3 gap-4 mb-8">
            <div className="card text-center">
              <p className="text-3xl font-bold text-white">{results.length}</p>
              <p className="text-gray-400 text-sm mt-1">Analyses Run</p>
            </div>
            <div className="card text-center">
              <p className="text-3xl font-bold text-white">
                {Math.round(results.reduce((a, r) => a + r.match_score, 0) / results.length)}%
              </p>
              <p className="text-gray-400 text-sm mt-1">Avg Match Score</p>
            </div>
            <div className="card text-center">
              <p className="text-3xl font-bold text-white">
                {results.filter(r => r.match_score >= 70).length}
              </p>
              <p className="text-gray-400 text-sm mt-1">Strong Matches</p>
            </div>
          </div>
        )}

        {/* Content */}
        {loading ? (
          <div className="card flex items-center justify-center py-20">
            <svg className="animate-spin w-8 h-8 text-brand-500 mr-3" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
            </svg>
            <span className="text-gray-400">Loading your results…</span>
          </div>
        ) : error ? (
          <div className="card text-center py-12 text-red-400">{error}</div>
        ) : results.length === 0 ? (
          <div className="card text-center py-20">
            <div className="w-16 h-16 rounded-2xl bg-gray-800 flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h2 className="text-lg font-semibold text-gray-300">No analyses yet</h2>
            <p className="text-gray-500 text-sm mt-1 mb-6">Run your first resume analysis to see results here</p>
            <button onClick={() => navigate('/match')} className="btn-primary">
              Start Your First Analysis
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider">
              Past Analyses ({results.length})
            </h2>
            {results.map((r) => (
              <div key={r.id} className="card cursor-pointer hover:border-gray-700 transition-colors" onClick={() => setExpanded(expanded === r.id ? null : r.id)}>
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-3 mb-1">
                      <ScoreBadge score={r.match_score} />
                      <span className="text-xs text-gray-500">
                        {new Date(r.created_at).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                      </span>
                    </div>
                    <p className="text-gray-300 text-sm truncate">
                      {r.job_description.substring(0, 120)}…
                    </p>
                  </div>
                  <svg
                    className={`w-5 h-5 text-gray-500 shrink-0 transition-transform duration-200 ${expanded === r.id ? 'rotate-180' : ''}`}
                    fill="none" viewBox="0 0 24 24" stroke="currentColor"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </div>

                {expanded === r.id && (
                  <div className="mt-5 pt-5 border-t border-gray-800 space-y-4 animate-fade-in">
                    {r.matched_skills.length > 0 && (
                      <div>
                        <p className="text-xs font-semibold text-gray-400 uppercase mb-2">Matched Skills</p>
                        <div className="flex flex-wrap gap-1.5">
                          {r.matched_skills.map(s => <span key={s} className="badge-green">{s}</span>)}
                        </div>
                      </div>
                    )}
                    {r.missing_skills.length > 0 && (
                      <div>
                        <p className="text-xs font-semibold text-gray-400 uppercase mb-2">Missing Skills</p>
                        <div className="flex flex-wrap gap-1.5">
                          {r.missing_skills.map(s => <span key={s} className="badge-red">{s}</span>)}
                        </div>
                      </div>
                    )}
                    {r.suggestions.length > 0 && (
                      <div>
                        <p className="text-xs font-semibold text-gray-400 uppercase mb-2">Suggestions</p>
                        <ul className="space-y-1.5">
                          {r.suggestions.map((s, i) => (
                            <li key={i} className="flex items-start gap-2 text-xs text-gray-400">
                              <svg className="w-3.5 h-3.5 text-brand-400 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                              </svg>
                              {s}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
