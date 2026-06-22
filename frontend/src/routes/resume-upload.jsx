import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import Sidebar from '../components/dashboard/Sidebar'
import ResumeUploader from '../components/resume/ResumeUploader'
import ResumePreview from '../components/resume/ResumePreview'
import apiClient from '../lib/apiClient'

function ResumeUploadPage() {
  const navigate = useNavigate()
  const [resumeData, setResumeData] = useState(null)
  const [resumeText, setResumeText] = useState('')
  const [checkingExisting, setCheckingExisting] = useState(true)
  const [hasExisting, setHasExisting] = useState(false)

  useEffect(() => {
    apiClient.get('/api/v1/resume/current')
      .then((res) => {
        if (res.data) {
          setResumeData(res.data.structured_data)
          setResumeText(res.data.extracted_text)
          setHasExisting(true)
        }
      })
      .catch(() => {
        // No existing resume — fine, just show the upload form
      })
      .finally(() => setCheckingExisting(false))
  }, [])

  const handleUploadComplete = (data) => {
    setResumeData(data)
    setResumeText(data.extracted_text || '')
    setHasExisting(true)
  }

  const handleContinue = () => {
    navigate('/company-select', { state: { resumeData, resumeText } })
  }

  const handleUploadNew = () => {
    setHasExisting(false)
    setResumeData(null)
    setResumeText('')
  }

  if (checkingExisting) {
    return (
      <div className="flex">
        <Sidebar />
        <main className="flex-1 p-8 bg-bg-base min-h-screen">
          <p className="text-text-secondary">Checking for an existing resume...</p>
        </main>
      </div>
    )
  }

  return (
    <div className="flex">
      <Sidebar />
      <main className="flex-1 p-8 bg-bg-base min-h-screen">
        <h1 className="text-2xl font-bold text-text-primary mb-1">New Interview</h1>
        <p className="text-text-secondary mb-8">
          {hasExisting ? 'We found your resume on file' : 'Upload your resume to get started'}
        </p>

        <div className="flex flex-col gap-6">
          {hasExisting ? (
            <>
              <ResumePreview resumeData={resumeData} />
              <div className="flex gap-3">
                <button
                  onClick={handleContinue}
                  className="bg-accent text-accent-text font-semibold rounded-lg px-6 py-2.5 hover:opacity-90 transition-opacity"
                >
                  Continue with this resume →
                </button>
                <button
                  onClick={handleUploadNew}
                  className="text-text-secondary text-sm hover:text-text-primary transition-colors"
                >
                  Upload a different resume
                </button>
              </div>
            </>
          ) : (
            <>
              <ResumeUploader onUploadComplete={handleUploadComplete} />
              {resumeData && (
                <>
                  <ResumePreview resumeData={resumeData} />
                  <button
                    onClick={handleContinue}
                    className="w-fit bg-accent text-accent-text font-semibold rounded-lg px-6 py-2.5 hover:opacity-90 transition-opacity"
                  >
                    Continue to company selection →
                  </button>
                </>
              )}
            </>
          )}
        </div>
      </main>
    </div>
  )
}

export default ResumeUploadPage