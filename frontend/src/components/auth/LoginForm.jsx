import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import apiClient from '../../lib/apiClient'
import { useAuthStore } from '../../store/authStore'

function LoginForm({ onSwitchToRegister, embedded = false }) {
  const navigate = useNavigate()
  const setAuth = useAuthStore((state) => state.setAuth)

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await apiClient.post('/api/v1/auth/login', { email, password })
      const { access_token, refresh_token } = response.data
      setAuth(access_token, refresh_token, { email })
      if (!embedded) navigate('/')
      // If embedded in the modal, the modal disappears automatically once
      // useAuthStore's accessToken updates — no navigation needed.
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed. Check your credentials.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="w-full max-w-sm">
      <h1 className="text-2xl font-bold text-text-primary mb-1">Welcome back</h1>
      <p className="text-text-secondary text-sm mb-8">Log in to continue your interview prep</p>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-text-secondary text-sm mb-1.5">Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="w-full bg-bg-card-hover border border-border rounded-lg px-4 py-2.5 text-text-primary focus:outline-none focus:ring-2 focus:ring-accent/50 focus:border-accent"
            placeholder="you@example.com"
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
            placeholder="••••••••"
          />
        </div>

        {error && <p className="text-red-400 text-sm">{error}</p>}

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-accent text-accent-text font-semibold rounded-lg py-2.5 hover:opacity-90 transition-opacity disabled:opacity-50"
        >
          {loading ? 'Logging in...' : 'Log in'}
        </button>
      </form>

      <p className="text-text-secondary text-sm mt-6 text-center">
        Don't have an account?{' '}
        {embedded ? (
          <button onClick={onSwitchToRegister} className="text-accent hover:underline">
            Sign up
          </button>
        ) : (
          <Link to="/register" className="text-accent hover:underline">Sign up</Link>
        )}
      </p>
    </div>
  )
}

export default LoginForm