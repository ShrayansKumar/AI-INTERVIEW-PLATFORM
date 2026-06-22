import { useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import Sidebar from '../components/dashboard/Sidebar'
import apiClient from '../lib/apiClient'

const AVAILABLE_COMPANIES = [
  { name: 'Amazon', description: 'E-commerce and cloud computing' },
  { name: 'Google', description: 'Search, cloud, and consumer tech' },
  { name: 'Microsoft', description: 'Enterprise software and cloud' },
  { name: 'Meta', description: 'Social platforms and AR/VR' },
  { name: 'Goldman Sachs', description: 'Investment banking and fintech' },
  { name: 'Uber', description: 'Ride-sharing and logistics' },
  { name: 'Salesforce', description: 'Enterprise SaaS and CRM' },
  { name: 'Atlassian', description: 'Developer and team collaboration tools' },
  { name: 'Flipkart', description: 'E-commerce at India scale' },
]

function CompanySelectPage() {
  const location = useLocation()
  const navigate = useNavigate()
  const { resumeText } = location.state || {}

  const [selectedCompany, setSelectedCompany] = useState(null)
  const [starting, setStarting] = useState(false)
  const [error, setError] = useState('')

  const handleStart = async () => {
    if (!resumeText) {
      setError('Resume text missing — please go back and upload your resume again.')
      return
    }
    if (!selectedCompany) {
      setError('Please select a company first.')
      return
    }

    setStarting(true)
    setError('')

    try {
      const response = await apiClient.post('/api/v1/interview/start-voice', {
        resume_text: resumeText,
        company_name: selectedCompany,
      })

      navigate('/interview-room', { state: { ...response.data } })
    } catch (err) {
      setError(err.response?.data?.detail || 'Could not start the interview.')
    } finally {
      setStarting(false)
    }
  }

  return (
    <div className="flex">
      <Sidebar />
      <main className="flex-1 p-8 bg-bg-base min-h-screen">
        <h1 className="text-2xl font-bold text-text-primary mb-1">Choose a company</h1>
        <p className="text-text-secondary mb-8">
          Questions will be tailored to this company's interview style
        </p>

        <div className="grid grid-cols-3 gap-4 max-w-2xl mb-6">
          {AVAILABLE_COMPANIES.map((company) => (
            <button
              key={company.name}
              onClick={() => setSelectedCompany(company.name)}
              className={`text-left p-4 rounded-xl border transition-colors ${
                selectedCompany === company.name
                  ? 'border-accent bg-accent-soft'
                  : 'border-border bg-bg-card hover:bg-bg-card-hover'
              }`}
            >
              <p className="text-text-primary font-semibold">{company.name}</p>
              <p className="text-text-secondary text-xs mt-1">{company.description}</p>
            </button>
          ))}
        </div>

        {error && <p className="text-red-400 text-sm mb-4">{error}</p>}

        <button
          onClick={handleStart}
          disabled={starting || !selectedCompany}
          className="bg-accent text-accent-text font-semibold rounded-lg px-6 py-2.5 hover:opacity-90 transition-opacity disabled:opacity-50"
        >
          {starting ? 'Preparing your interview...' : 'Start interview'}
        </button>
      </main>
    </div>
  )
}

export default CompanySelectPage