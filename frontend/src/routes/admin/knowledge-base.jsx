import { useState, useEffect } from 'react'
import Sidebar from '../../components/dashboard/Sidebar'
import adminApiClient from '../../lib/adminApiClient'

function AdminKnowledgeBasePage() {
  const [chunks, setChunks] = useState([])
  const [companyFilter, setCompanyFilter] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const [content, setContent] = useState('')
  const [source, setSource] = useState('interview_experience')
  const [company, setCompany] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const fetchChunks = async () => {
    setLoading(true)
    try {
      const params = companyFilter ? { company: companyFilter } : {}
      const res = await adminApiClient.get('/api/v1/admin/knowledge-base', { params })
      setChunks(res.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Could not load knowledge base.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchChunks()
  }, [companyFilter])

  const handleCreate = async (e) => {
    e.preventDefault()
    if (!content.trim() || !company.trim()) return

    setSubmitting(true)
    setError('')
    try {
      await adminApiClient.post('/api/v1/admin/knowledge-base', { content, source, company })
      setContent('')
      setCompany('')
      fetchChunks()
    } catch (err) {
      setError(err.response?.data?.detail || 'Could not add chunk.')
    } finally {
      setSubmitting(false)
    }
  }

  const handleDelete = async (id) => {
    if (!confirm('Delete this knowledge base entry?')) return
    try {
      await adminApiClient.delete(`/api/v1/admin/knowledge-base/${id}`)
      fetchChunks()
    } catch (err) {
      setError(err.response?.data?.detail || 'Could not delete entry.')
    }
  }

  return (
    <div className="flex">
      <Sidebar />
      <main className="flex-1 p-8 bg-bg-base min-h-screen">
        <h1 className="text-2xl font-bold text-text-primary mb-1">Admin · Knowledge Base</h1>
        <p className="text-text-secondary mb-8">Manage RAG content used for question generation</p>

        <form onSubmit={handleCreate} className="bg-bg-card border border-border rounded-2xl p-6 max-w-lg mb-8 space-y-3">
          <h3 className="text-text-primary font-semibold mb-2">Add a knowledge chunk</h3>
          <input
            type="text"
            value={company}
            onChange={(e) => setCompany(e.target.value)}
            placeholder="Company (e.g. Amazon)"
            className="w-full bg-bg-card-hover border border-border rounded-lg px-3 py-2 text-text-primary text-sm focus:outline-none focus:ring-2 focus:ring-accent/50"
          />
          <select
            value={source}
            onChange={(e) => setSource(e.target.value)}
            className="w-full bg-bg-card-hover border border-border rounded-lg px-3 py-2 text-text-primary text-sm focus:outline-none focus:ring-2 focus:ring-accent/50"
          >
            <option value="job_description">job_description</option>
            <option value="interview_experience">interview_experience</option>
            <option value="oa_question">oa_question</option>
            <option value="topic_focus">topic_focus</option>
          </select>
          <textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder="Content text..."
            rows={3}
            className="w-full bg-bg-card-hover border border-border rounded-lg px-3 py-2 text-text-primary text-sm focus:outline-none focus:ring-2 focus:ring-accent/50"
          />
          <button
            type="submit"
            disabled={submitting}
            className="bg-accent text-accent-text font-semibold rounded-lg px-4 py-2 text-sm hover:opacity-90 transition-opacity disabled:opacity-50"
          >
            {submitting ? 'Embedding & saving...' : 'Add chunk'}
          </button>
        </form>

        <div className="mb-4 max-w-lg">
          <input
            type="text"
            value={companyFilter}
            onChange={(e) => setCompanyFilter(e.target.value)}
            placeholder="Filter by company..."
            className="w-full bg-bg-card border border-border rounded-lg px-3 py-2 text-text-primary text-sm focus:outline-none focus:ring-2 focus:ring-accent/50"
          />
        </div>

        {error && <p className="text-red-400 text-sm mb-4">{error}</p>}
        {loading && <p className="text-text-secondary">Loading...</p>}

        <div className="space-y-2 max-w-2xl">
          {chunks.map((chunk) => (
            <div
              key={chunk.id}
              className="flex items-start justify-between bg-bg-card border border-border rounded-xl p-4"
            >
              <div className="flex-1">
                <div className="flex gap-2 mb-1">
                  <span className="bg-accent-soft text-accent text-xs px-2 py-0.5 rounded-full">
                    {chunk.company}
                  </span>
                  <span className="bg-bg-card-hover text-text-secondary text-xs px-2 py-0.5 rounded-full">
                    {chunk.source}
                  </span>
                </div>
                <p className="text-text-primary text-sm">{chunk.content}</p>
              </div>
              <button
                onClick={() => handleDelete(chunk.id)}
                className="text-red-400 text-sm hover:text-red-300 ml-4 flex-shrink-0"
              >
                Delete
              </button>
            </div>
          ))}
        </div>
      </main>
    </div>
  )
}

export default AdminKnowledgeBasePage