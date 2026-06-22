import { BrowserRouter, Routes, Route } from 'react-router-dom'
import ProtectedRoute from '../components/auth/ProtectedRoute'
import LoginPage from './login'
import RegisterPage from './register'
import DashboardPage from './dashboard'
import ResumeUploadPage from './resume-upload'
import CompanySelectPage from './company-select'
import InterviewRoomPage from './interview-room'
import ReportPage from './report'
import HistoryPage from './history'
import AdminCompaniesPage from './admin/companies'
import AdminKnowledgeBasePage from './admin/knowledge-base'
import AdminUsersPage from './admin/users'
import AdminProtectedRoute from '../components/admin/AdminProtectedRoute'

function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <DashboardPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/resume-upload"
          element={
            <ProtectedRoute>
              <ResumeUploadPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/company-select"
          element={
            <ProtectedRoute>
              <CompanySelectPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/interview-room"
          element={
            <ProtectedRoute>
              <InterviewRoomPage />
            </ProtectedRoute>
          }
        />
        <Route path="/report/:sessionId" element={<ProtectedRoute><ReportPage /></ProtectedRoute>} />
        <Route path="/history" element={<ProtectedRoute><HistoryPage /></ProtectedRoute>} />
        <Route path="/admin/companies" element={<AdminProtectedRoute><AdminCompaniesPage /></AdminProtectedRoute>} />
        <Route path="/admin/knowledge-base" element={<AdminProtectedRoute><AdminKnowledgeBasePage /></AdminProtectedRoute>} />
        <Route path="/admin/users" element={<AdminProtectedRoute><AdminUsersPage /></AdminProtectedRoute>} />
      </Routes>
    </BrowserRouter>
  )
}

export default AppRoutes