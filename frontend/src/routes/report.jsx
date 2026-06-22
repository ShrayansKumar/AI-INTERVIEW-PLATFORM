import { useParams } from 'react-router-dom'
import Sidebar from '../components/dashboard/Sidebar'
import ReportSummary from '../components/report/ReportSummary'
import DownloadReportButton from '../components/report/DownloadReportButton'
import { useReportData } from '../hooks/useReportData'

function ReportPage() {
  const { sessionId } = useParams()

  const { report, loading, error } = useReportData(sessionId)

  return (
    <div className="flex">
      <Sidebar />
      <main className="flex-1 p-8 bg-bg-base min-h-screen">
        <div className="flex items-center justify-between mb-8 max-w-3xl">
          <div>
            <h1 className="text-2xl font-bold text-text-primary mb-1">Interview Report</h1>
            <p className="text-text-secondary">Your performance breakdown</p>
          </div>
          {report && <DownloadReportButton sessionId={sessionId} />}
        </div>

        {loading && <p className="text-text-secondary">Loading report...</p>}
        {error && <p className="text-red-400">{error}</p>}
        {report && <ReportSummary report={report} />}
      </main>
    </div>
  )
}

export default ReportPage