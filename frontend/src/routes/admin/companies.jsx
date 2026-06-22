import { useState, useEffect } from 'react'
import Sidebar from '../../components/dashboard/Sidebar'
import adminApiClient from '../../lib/adminApiClient'

function AdminCompaniesPage() {
  const [companies, setCompanies] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const fetchCompanies = async () => {
    setLoading(true)
    try {
      const res = await adminApiClient.get('/api/v1/admin/companies')
      setCompanies(res.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Could not load companies.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchCompanies()
  }, [])

  const handleCreate = async (e) => {
    e.preventDefault()
    if (!name.trim()) return

    setSubmitting(true)
    setError('')
    try {
      await adminApiClient.post('/api/v1/admin/companies', { name, description })
      setName('')
      setDescription('')
      fetchCompanies()
    } catch (err) {
      setError(err.response?.data?.detail || 'Could not create company.')
    } finally {
      setSubmitting(false)
    }
  }

  const handleDelete = async (id) => {
    if (!confirm('Delete this company?')) return
    try {
      await adminApiClient.delete(`/api/v1/admin/companies/${id}`)
      fetchCompanies()
    } catch (err) {
      setError(err.response?.data?.detail || 'Could not delete company.')
    }
  }

  return (
    <div className="flex">
      <Sidebar />
      <main className="flex-1 p-8 bg-bg-base min-h-screen">
        <h1 className="text-2xl font-bold text-text-primary mb-1">Admin · Companies</h1>
        <p className="text-text-secondary mb-8">Manage companies available for interviews</p>

        <form onSubmit={handleCreate} className="bg-bg-card border border-border rounded-2xl p-6 max-w-md mb-8 space-y-3">
          <h3 className="text-text-primary font-semibold mb-2">Add a company</h3>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Company name"
            className="w-full bg-bg-card-hover border border-border rounded-lg px-3 py-2 text-text-primary text-sm focus:outline-none focus:ring-2 focus:ring-accent/50"
          />
          <input
            type="text"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Description (optional)"
            className="w-full bg-bg-card-hover border border-border rounded-lg px-3 py-2 text-text-primary text-sm focus:outline-none focus:ring-2 focus:ring-accent/50"
          />
          <button
            type="submit"
            disabled={submitting}
            className="bg-accent text-accent-text font-semibold rounded-lg px-4 py-2 text-sm hover:opacity-90 transition-opacity disabled:opacity-50"
          >
            {submitting ? 'Adding...' : 'Add company'}
          </button>
        </form>

        {error && <p className="text-red-400 text-sm mb-4">{error}</p>}
        {loading && <p className="text-text-secondary">Loading...</p>}

        <div className="space-y-2 max-w-md">
          {companies.map((company) => (
            <div
              key={company.id}
              className="flex items-center justify-between bg-bg-card border border-border rounded-xl p-4"
            >
              <div>
                <p className="text-text-primary font-medium">{company.name}</p>
                <p className="text-text-secondary text-xs">{company.description}</p>
              </div>
              <button
                onClick={() => handleDelete(company.id)}
                className="text-red-400 text-sm hover:text-red-300"
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

export default AdminCompaniesPage