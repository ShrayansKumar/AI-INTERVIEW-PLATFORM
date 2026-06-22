import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import apiClient from '../../lib/apiClient'

function RegisterForm({ onSwitchToLogin, embedded = false }) {
  const navigate = useNavigate()

  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      await apiClient.post('/api/v1/auth/register', { name, email, password })
      if (embedded) {
        onSwitchToLogin()
      } else {
        navigate('/login')
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="w-full max-w-sm">
      <h1 className="text-2xl font-bold text-text-primary mb-1">Create your account</h1>
      <p className="text-text-secondary text-sm mb-8">Start practicing for real interviews</p>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-text-secondary text-sm mb-1.5">Full name</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            className="w-full bg-bg-card-hover border border-border rounded-lg px-4 py-2.5 text-text-primary focus:outline-none focus:ring-2 focus:ring-accent/50 focus:border-accent"
            placeholder="Shrayans Kumar"
          />
        </div>

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
            minLength={8}
            className="w-full bg-bg-card-hover border border-border rounded-lg px-4 py-2.5 text-text-primary focus:outline-none focus:ring-2 focus:ring-accent/50 focus:border-accent"
            placeholder="At least 8 characters"
          />
        </div>

        {error && <p className="text-red-400 text-sm">{error}</p>}

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-accent text-accent-text font-semibold rounded-lg py-2.5 hover:opacity-90 transition-opacity disabled:opacity-50"
        >
          {loading ? 'Creating account...' : 'Sign up'}
        </button>
      </form>

      <p className="text-text-secondary text-sm mt-6 text-center">
        Already have an account?{' '}
        {embedded ? (
          <button onClick={onSwitchToLogin} className="text-accent hover:underline">
            Log in
          </button>
        ) : (
          <Link to="/login" className="text-accent hover:underline">Log in</Link>
        )}
      </p>
    </div>
  )
}

export default RegisterForm