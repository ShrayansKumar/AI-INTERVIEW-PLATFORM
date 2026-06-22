import { useEffect } from 'react'
import AppRoutes from './routes/index'
import { useAuthStore } from './store/authStore'

function App() {
  const initAuth = useAuthStore((state) => state.initAuth)
  const fetchCurrentUser = useAuthStore((state) => state.fetchCurrentUser)
  const authChecked = useAuthStore((state) => state.authChecked)
  const accessToken = useAuthStore((state) => state.accessToken)

  useEffect(() => {
    initAuth()
  }, [])

  useEffect(() => {
    if (accessToken) fetchCurrentUser()
  }, [accessToken])

  if (!authChecked) {
    return <div className="min-h-screen bg-bg-base" />
  }

  return <AppRoutes />
}

export default App