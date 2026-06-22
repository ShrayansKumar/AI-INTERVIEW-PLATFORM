import { useState } from 'react'
import apiClient from '../../lib/apiClient'

function ResumeUploader({ onUploadComplete }) {
  const [file, setFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState('')

  const handleFileChange = (e) => {
    const selected = e.target.files[0]
    if (selected && selected.type !== 'application/pdf') {
      setError('Only PDF files are supported.')
      setFile(null)
      return
    }
    setError('')
    setFile(selected)
  }

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a PDF file first.')
      return
    }

    setUploading(true)
    setError('')

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await apiClient.post('/api/v1/resume/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })

      onUploadComplete(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed. Please try again.')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="bg-bg-card border border-border rounded-2xl p-6 max-w-md">
      <p className="text-text-secondary text-sm mb-1">Step 1</p>
      <h2 className="text-text-primary text-lg font-semibold mb-4">Upload your resume</h2>

      <label className="block border-2 border-dashed border-border rounded-xl p-6 text-center cursor-pointer hover:border-accent/50 transition-colors mb-4">
        <input
          type="file"
          accept="application/pdf"
          onChange={handleFileChange}
          className="hidden"
        />
        <p className="text-text-secondary text-sm">
          {file ? file.name : 'Click to choose a PDF, or drag it here'}
        </p>
      </label>

      {error && <p className="text-red-400 text-sm mb-4">{error}</p>}

      <button
        onClick={handleUpload}
        disabled={uploading || !file}
        className="w-full bg-accent text-accent-text font-semibold rounded-lg py-2.5 hover:opacity-90 transition-opacity disabled:opacity-50"
      >
        {uploading ? 'Uploading & analyzing...' : 'Upload resume'}
      </button>
    </div>
  )
}

export default ResumeUploader