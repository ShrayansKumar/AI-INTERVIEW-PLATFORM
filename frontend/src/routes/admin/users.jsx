import { useState, useEffect } from 'react'
import Sidebar from '../../components/dashboard/Sidebar'
import adminApiClient from '../../lib/adminApiClient'

function AdminUsersPage() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    adminApiClient.get('/api/v1/admin/users')
      .then((res) => setUsers(res.data))
      .catch((err) => setError(err.response?.data?.detail || 'Could not load users.'))
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="flex">
      <Sidebar />
      <main className="flex-1 p-8 bg-bg-base min-h-screen">
        <h1 className="text-2xl font-bold text-text-primary mb-1">Admin · Users</h1>
        <p className="text-text-secondary mb-8">All registered users</p>

        {loading && <p className="text-text-secondary">Loading...</p>}
        {error && <p className="text-red-400">{error}</p>}

        <div className="bg-bg-card border border-border rounded-2xl overflow-hidden max-w-2xl">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-border text-text-secondary text-left">
                <th className="px-4 py-3">Name</th>
                <th className="px-4 py-3">Email</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user.id} className="border-b border-border last:border-0">
                  <td className="px-4 py-3 text-text-primary">{user.name}</td>
                  <td className="px-4 py-3 text-text-secondary">{user.email}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  )
}

export default AdminUsersPage