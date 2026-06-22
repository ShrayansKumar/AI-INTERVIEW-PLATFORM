import { useState, useRef, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuthStore } from '../../store/authStore'
import apiClient from '../../lib/apiClient'

function ProfileMenu() {
  const navigate = useNavigate()
  const logout = useAuthStore((state) => state.logout)
  const user = useAuthStore((state) => state.user)

  const [open, setOpen] = useState(false)
  const [uploading, setUploading] = useState(false)
  const menuRef = useRef(null)
  const fileInputRef = useRef(null)

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const handleFileChange = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    setUploading(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await apiClient.post('/api/v1/auth/me/profile-picture', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      useAuthStore.setState((state) => ({
        user: { ...state.user, profile_picture_url: response.data.profile_picture_url },
      }))
    } catch (err) {
      console.error('Failed to upload profile picture', err)
    } finally {
      setUploading(false)
    }
  }

  const initials = user?.name
    ? user.name.split(' ').map((n) => n[0]).join('').slice(0, 2).toUpperCase()
    : '?'

  return (
    <div className="relative" ref={menuRef}>
      <button
        onClick={() => setOpen((prev) => !prev)}
        className="flex items-center gap-2.5 hover:bg-bg-card-hover rounded-full pr-3 pl-1 py-1 transition-colors"
      >
        {user?.profile_picture_url ? (
          <img
            src={user.profile_picture_url}
            alt="Profile"
            className="w-8 h-8 rounded-full object-cover border border-border"
          />
        ) : (
          <div className="w-8 h-8 rounded-full bg-accent-soft text-accent flex items-center justify-center text-xs font-semibold">
            {initials}
          </div>
        )}
        <span className="text-text-primary text-sm font-medium">{user?.name || 'Account'}</span>
      </button>

      {open && (
        <div className="absolute right-0 mt-2 w-48 bg-bg-card border border-border rounded-xl shadow-lg overflow-hidden z-50">
          <button
            onClick={() => {
              fileInputRef.current?.click()
              setOpen(false)
            }}
            disabled={uploading}
            className="w-full text-left px-4 py-2.5 text-sm text-text-primary hover:bg-bg-card-hover transition-colors disabled:opacity-50"
          >
            {uploading ? 'Uploading...' : 'Update profile picture'}
          </button>
          <button
            onClick={() => {
              logout()
              navigate('/login')
            }}
            className="w-full text-left px-4 py-2.5 text-sm text-red-400 hover:bg-bg-card-hover transition-colors"
          >
            Log out
          </button>
        </div>
      )}

      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        className="hidden"
      />
    </div>
  )
}

export default ProfileMenu