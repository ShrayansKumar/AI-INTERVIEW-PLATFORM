import { BrowserRouter, Routes, Route } from 'react-router-dom'
import ProtectedRoute from './ProtectedRoute'

// Temporary placeholder components — replaced in Day 23
function LoginPlaceholder() {
  return <div className="min-h-screen bg-bg-base flex items-center justify-center text-text-primary">Login Page (Day 23)</div>
}
function DashboardPlaceholder() {
  return <div className="min-h-screen bg-bg-base flex items-center justify-center text-text-primary">Dashboard (Day 23)</div>
}

function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPlaceholder />} />
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <DashboardPlaceholder />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  )
}

export default AppRouter