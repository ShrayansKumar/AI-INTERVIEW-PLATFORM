import { useAdminAuthStore } from '../../store/adminAuthStore'
import AdminLoginForm from './AdminLoginForm'

function AdminProtectedRoute({ children }) {
  const isAdminAuthenticated = useAdminAuthStore((state) => !!state.adminToken)

  if (!isAdminAuthenticated) {
    return (
      <div className="relative">
        <div className="blur-sm pointer-events-none select-none">
          {children}
        </div>
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-bg-card border border-border rounded-2xl p-8 w-full max-w-sm shadow-2xl">
            <AdminLoginForm />
          </div>
        </div>
      </div>
    )
  }

  return children
}

export default AdminProtectedRoute