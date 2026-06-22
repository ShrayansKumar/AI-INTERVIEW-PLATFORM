import { useNavigate } from 'react-router-dom'
import Sidebar from '../components/dashboard/Sidebar'
import ScoreTrendChart from '../components/dashboard/ScoreTrendChart'
import TopicBreakdownChart from '../components/dashboard/TopicBreakdownChart'
import ProfileMenu from '../components/dashboard/ProfileMenu'

function DashboardPage() {
  const navigate = useNavigate()

  return (
    <div className="flex">
      <Sidebar />
      <main className="flex-1 p-8 bg-bg-base min-h-screen">
        <div className="flex items-center justify-between mb-1">
          <h1 className="text-2xl font-bold text-text-primary">Dashboard</h1>
          <ProfileMenu />
        </div>
        <p className="text-text-secondary mb-8">Your interview performance over time</p>

        <div className="bg-bg-card border border-border rounded-2xl p-6 max-w-md mb-8">
          <p className="text-text-secondary text-sm mb-1">Ready to practice?</p>
          <p className="text-text-primary text-lg font-semibold mb-4">Start a new mock interview</p>
          <button
            onClick={() => navigate('/resume-upload')}
            className="bg-accent text-accent-text font-semibold rounded-lg px-5 py-2.5 hover:opacity-90 transition-opacity"
          >
            New Interview
          </button>
        </div>

        <div className="grid grid-cols-2 gap-6 max-w-4xl">
          <ScoreTrendChart />
          <TopicBreakdownChart />
        </div>
      </main>
    </div>
  )
}

export default DashboardPage