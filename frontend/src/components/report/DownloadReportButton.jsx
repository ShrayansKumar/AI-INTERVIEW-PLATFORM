import { useState } from 'react'
import apiClient from '../../lib/apiClient'

function DownloadReportButton({ sessionId }) {
  const [downloading, setDownloading] = useState(false)

  const handleDownload = async () => {
    setDownloading(true)
    try {
      const response = await apiClient.get(`/api/v1/report/${sessionId}/pdf`, {
        responseType: 'blob',
      })

      const url = URL.createObjectURL(response.data)
      const link = document.createElement('a')
      link.href = url
      link.download = `interview_report_${sessionId}.pdf`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
    } catch (err) {
      console.error('PDF download failed', err)
    } finally {
      setDownloading(false)
    }
  }

  return (
    <button
      onClick={handleDownload}
      disabled={downloading}
      className="bg-accent text-accent-text font-semibold rounded-lg px-5 py-2.5 hover:opacity-90 transition-opacity disabled:opacity-50"
    >
      {downloading ? 'Preparing PDF...' : 'Download PDF Report'}
    </button>
  )
}

export default DownloadReportButton