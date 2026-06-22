import { useState } from 'react'
import adminApiClient from '../../lib/adminApiClient'
import { useAdminAuthStore } from '../../store/adminAuthStore'

function AdminLoginForm() {
  const setAdminAuth = useAdminAuthStore((state) => state.setAdminAuth)

  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await adminApiClient.post('/api/v1/admin-auth/login', { username, password })
      setAdminAuth(response.data.access_token, { username })
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid admin credentials')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="w-full max-w-sm">
      <h1 className="text-2xl font-bold text-text-primary mb-1">Admin access</h1>
      <p className="text-text-secondary text-sm mb-8">Restricted area — authorized personnel only</p>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-text-secondary text-sm mb-1.5">Username</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            className="w-full bg-bg-card-hover border border-border rounded-lg px-4 py-2.5 text-text-primary focus:outline-none focus:ring-2 focus:ring-accent/50 focus:border-accent"
          />
        </div>

        <div>
          <label className="block text-text-secondary text-sm mb-1.5">Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="w-full bg-bg-card-hover border border-border rounded-lg px-4 py-2.5 text-text-primary focus:outline-none focus:ring-2 focus:ring-accent/50 focus:border-accent"
          />
        </div>

        {error && <p className="text-red-400 text-sm">{error}</p>}

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-accent text-accent-text font-semibold rounded-lg py-2.5 hover:opacity-90 transition-opacity disabled:opacity-50"
        >
          {loading ? 'Verifying...' : 'Enter admin panel'}
        </button>
      </form>
    </div>
  )
}

export default AdminLoginForm