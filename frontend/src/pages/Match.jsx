import React, { useState, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api/client'

const ACCEPTED_TYPES = [
  'application/pdf',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  'text/plain',
]

function ScoreRing({ score }) {
  const radius = 54
  const circumference = 2 * Math.PI * radius
  const dash = (score / 100) * circumference
  const color =
    score >= 70 ? '#10b981' :
    score >= 45 ? '#f59e0b' : '#ef4444'

  return (
    <div className="flex flex-col items-center">
      <div className="relative w-40 h-40">
        <svg className="w-full h-full -rotate-90" viewBox="0 0 120 120">
          <circle cx="60" cy="60" r={radius} fill="none" stroke="#1f2937" strokeWidth="10" />
          <circle
            cx="60" cy="60" r={radius}
            fill="none"
            stroke={color}
            strokeWidth="10"
            strokeDasharray={`${dash} ${circumference}`}
            strokeLinecap="round"
            style={{ transition: 'stroke-dasharray 1s ease' }}
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-4xl font-bold text-white">{Math.round(score)}</span>
          <span className="text-xs text-gray-400 font-medium">/ 100</span>
        </div>
      </div>
      <span className="mt-2 text-sm font-medium" style={{ color }}>
        {score >= 70 ? 'Strong Match' : score >= 45 ? 'Moderate Match' : 'Weak Match'}
      </span>
    </div>
  )
}

export default function Match() {
  const [file, setFile] = useState(null)
  const [jobDesc, setJobDesc] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [dragOver, setDragOver] = useState(false)
  const fileRef = useRef()
  const navigate = useNavigate()

  function handleFileDrop(e) {
    e.preventDefault()
    setDragOver(false)
    const f = e.dataTransfer.files[0]
    if (f) validateAndSetFile(f)
  }

  function validateAndSetFile(f) {
    if (!ACCEPTED_TYPES.includes(f.type) && !f.name.match(/\.(pdf|docx|txt)$/i)) {
      setError('Only PDF, DOCX, and TXT files are accepted.')
      return
    }
    if (f.size > 5 * 1024 * 1024) {
      setError('File must be under 5 MB.')
      return
    }
    setError('')
    setFile(f)
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    if (!file) { setError('Please upload your resume.'); return }
    if (jobDesc.trim().length < 50) { setError('Job description must be at least 50 characters.'); return }

    setLoading(true)
    setResult(null)
    const form = new FormData()
    form.append('resume_file', file)
    form.append('job_description', jobDesc)

    try {
      const { data } = await api.post('/match', form, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setResult(data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Analysis failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen px-4 py-8 animate-fade-in">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-white">Resume Matcher</h1>
            <p className="text-gray-400 mt-1">Upload your resume and paste a job description for instant AI analysis</p>
          </div>
          <button onClick={() => navigate('/dashboard')} className="btn-secondary">
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
            Dashboard
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Input Form */}
          <div className="card">
            <form onSubmit={handleSubmit} className="space-y-5">
              <h2 className="text-lg font-semibold text-white mb-1">Upload Resume</h2>

              {/* Drop Zone */}
              <div
                className={`border-2 border-dashed rounded-xl p-6 text-center cursor-pointer transition-all duration-200 ${
                  dragOver
                    ? 'border-brand-500 bg-brand-500/10'
                    : file
                    ? 'border-emerald-500 bg-emerald-500/10'
                    : 'border-gray-700 hover:border-gray-600'
                }`}
                onDragOver={e => { e.preventDefault(); setDragOver(true) }}
                onDragLeave={() => setDragOver(false)}
                onDrop={handleFileDrop}
                onClick={() => fileRef.current?.click()}
              >
                <input
                  ref={fileRef}
                  type="file"
                  className="hidden"
                  accept=".pdf,.docx,.txt"
                  onChange={e => e.target.files[0] && validateAndSetFile(e.target.files[0])}
                  id="resume-file-input"
                />
                {file ? (
                  <div className="flex flex-col items-center gap-2">
                    <svg className="w-10 h-10 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <span className="text-emerald-400 font-medium text-sm">{file.name}</span>
                    <span className="text-gray-500 text-xs">{(file.size / 1024).toFixed(1)} KB</span>
                  </div>
                ) : (
                  <div className="flex flex-col items-center gap-2">
                    <svg className="w-10 h-10 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                    <span className="text-gray-400 text-sm">Drag & drop or <span className="text-brand-400">browse</span></span>
                    <span className="text-gray-600 text-xs">PDF, DOCX, TXT — max 5 MB</span>
                  </div>
                )}
              </div>

              {/* Job Description */}
              <div>
                <label className="label" htmlFor="job-desc">Job Description</label>
                <textarea
                  id="job-desc"
                  className="input-field resize-none"
                  rows={8}
                  placeholder="Paste the job description here (minimum 50 characters)…"
                  value={jobDesc}
                  onChange={e => setJobDesc(e.target.value)}
                  required
                />
                <p className="text-xs text-gray-600 mt-1">{jobDesc.length} characters</p>
              </div>

              {error && (
                <div className="flex items-start gap-2 p-3 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-sm">
                  <svg className="w-4 h-4 shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                  {error}
                </div>
              )}

              <button type="submit" className="btn-primary w-full" disabled={loading}>
                {loading ? (
                  <>
                    <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
                    </svg>
                    Analysing Resume…
                  </>
                ) : (
                  <>
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                    Analyse Now
                  </>
                )}
              </button>
            </form>
          </div>

          {/* Results Panel */}
          <div className="space-y-4">
            {loading && (
              <div className="card flex flex-col items-center justify-center py-16 animate-pulse-slow">
                <svg className="animate-spin w-12 h-12 text-brand-500 mb-4" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
                </svg>
                <p className="text-gray-400 font-medium">AI is analysing your resume…</p>
                <p className="text-gray-600 text-sm mt-1">This may take 15–30 seconds</p>
              </div>
            )}

            {result && !loading && (
              <div className="space-y-4 animate-slide-up">
                {/* Score */}
                <div className="card flex flex-col items-center py-8">
                  <h2 className="text-sm font-medium text-gray-400 uppercase tracking-wider mb-6">Match Score</h2>
                  <ScoreRing score={result.match_score} />
                </div>

                {/* Matched Skills */}
                <div className="card">
                  <h3 className="text-sm font-semibold text-gray-300 uppercase tracking-wider mb-3 flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-emerald-400 inline-block"/>
                    Matched Skills ({result.matched_skills.length})
                  </h3>
                  {result.matched_skills.length > 0 ? (
                    <div className="flex flex-wrap gap-2">
                      {result.matched_skills.map(s => (
                        <span key={s} className="badge-green">{s}</span>
                      ))}
                    </div>
                  ) : (
                    <p className="text-gray-500 text-sm">No matching skills found in the predefined list.</p>
                  )}
                </div>

                {/* Missing Skills */}
                <div className="card">
                  <h3 className="text-sm font-semibold text-gray-300 uppercase tracking-wider mb-3 flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-red-400 inline-block"/>
                    Missing Skills ({result.missing_skills.length})
                  </h3>
                  {result.missing_skills.length > 0 ? (
                    <div className="flex flex-wrap gap-2">
                      {result.missing_skills.map(s => (
                        <span key={s} className="badge-red">{s}</span>
                      ))}
                    </div>
                  ) : (
                    <p className="text-gray-500 text-sm">🎉 Your resume covers all the required skills!</p>
                  )}
                </div>

                {/* Suggestions */}
                <div className="card">
                  <h3 className="text-sm font-semibold text-gray-300 uppercase tracking-wider mb-3 flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-blue-400 inline-block"/>
                    Improvement Suggestions
                  </h3>
                  <ul className="space-y-2">
                    {result.suggestions.map((s, i) => (
                      <li key={i} className="flex items-start gap-2 text-sm text-gray-300">
                        <svg className="w-4 h-4 text-brand-400 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
                        {s}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            )}

            {!result && !loading && (
              <div className="card flex flex-col items-center justify-center py-16 text-center">
                <div className="w-16 h-16 rounded-2xl bg-gray-800 flex items-center justify-center mb-4">
                  <svg className="w-8 h-8 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <p className="text-gray-500 font-medium">Your Analysis Will Appear Here</p>
                <p className="text-gray-600 text-sm mt-1">Upload a resume and paste a job description to start</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
