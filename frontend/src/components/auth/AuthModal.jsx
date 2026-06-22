import { useState } from 'react'
import LoginForm from './LoginForm'
import RegisterForm from './RegisterForm'

function AuthModal() {
  const [mode, setMode] = useState('login')

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-bg-card border border-border rounded-2xl p-8 w-full max-w-sm shadow-2xl">
        {mode === 'login' ? (
          <LoginForm onSwitchToRegister={() => setMode('register')} embedded />
        ) : (
          <RegisterForm onSwitchToLogin={() => setMode('login')} embedded />
        )}
      </div>
    </div>
  )
}

export default AuthModal