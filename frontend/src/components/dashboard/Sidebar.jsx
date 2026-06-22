import { Link, useLocation } from 'react-router-dom'
import { useState } from 'react'
import { useAuthStore } from '../../store/authStore'

const navItems = [
  { label: 'Dashboard', path: '/', icon: '◧' },
  { label: 'New Interview', path: '/resume-upload', icon: '✦' },
  { label: 'History', path: '/history', icon: '◷' },
]

const adminItems = [
  { label: 'Companies', path: '/admin/companies' },
  { label: 'Knowledge Base', path: '/admin/knowledge-base' },
  { label: 'Users', path: '/admin/users' },
]

function Sidebar() {
  const location = useLocation()
  const logout = useAuthStore((state) => state.logout)
  const [adminOpen, setAdminOpen] = useState(location.pathname.startsWith('/admin'))

  return (
    <aside className="w-64 bg-bg-card border-r border-border h-screen flex flex-col p-4">
      <div className="mb-8 px-2">
        <h2 className="text-text-primary font-bold text-lg">Interview AI</h2>
      </div>

      <nav className="flex-1 space-y-1">
        {navItems.map((item) => {
          const isActive = location.pathname === item.path
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-accent-soft text-accent'
                  : 'text-text-secondary hover:bg-bg-card-hover hover:text-text-primary'
              }`}
            >
              <span>{item.icon}</span>
              {item.label}
            </Link>
          )
        })}

        {/* Admin section — expandable group */}
        <button
          onClick={() => setAdminOpen((prev) => !prev)}
          className={`w-full flex items-center justify-between gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
            location.pathname.startsWith('/admin')
              ? 'bg-accent-soft text-accent'
              : 'text-text-secondary hover:bg-bg-card-hover hover:text-text-primary'
          }`}
        >
          <span className="flex items-center gap-3">
            <span>⚙</span>
            Admin
          </span>
          <span className="text-xs">{adminOpen ? '▾' : '▸'}</span>
        </button>

        {adminOpen && (
          <div className="ml-4 pl-3 border-l border-border space-y-1">
            {adminItems.map((item) => {
              const isActive = location.pathname === item.path
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`block px-3 py-2 rounded-lg text-sm transition-colors ${
                    isActive
                      ? 'bg-accent-soft text-accent'
                      : 'text-text-secondary hover:bg-bg-card-hover hover:text-text-primary'
                  }`}
                >
                  {item.label}
                </Link>
              )
            })}
          </div>
        )}
      </nav>

      <button
        onClick={logout}
        className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-text-secondary hover:bg-bg-card-hover hover:text-text-primary transition-colors"
      >
        <span>⏻</span>
        Log out
      </button>
    </aside>
  )
}

export default Sidebar