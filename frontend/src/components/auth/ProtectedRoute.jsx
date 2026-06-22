import { useAuthStore } from '../../store/authStore'
import AuthModal from './AuthModal'

function ProtectedRoute({ children }) {
  const isAuthenticated = useAuthStore((state) => !!state.accessToken)

  if (!isAuthenticated) {
    return (
      <div className="relative">
        <div className="blur-sm pointer-events-none select-none">
          {children}
        </div>
        <AuthModal />
      </div>
    )
  }

  return children
}

export default ProtectedRoute