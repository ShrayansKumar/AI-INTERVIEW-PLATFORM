import { useState, useEffect } from 'react'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'
import apiClient from '../../lib/apiClient'

function ScoreTrendChart() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    apiClient.get('/api/v1/analytics/score-trend')
      .then((res) => {
        const formatted = res.data.map((item, i) => ({
          name: `Session ${i + 1}`,
          score: item.score,
        }))
        setData(formatted)
      })
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <p className="text-text-secondary text-sm">Loading...</p>
  if (data.length === 0) return <p className="text-text-secondary text-sm">No completed interviews yet.</p>

  return (
    <div className="bg-bg-card border border-border rounded-2xl p-6">
      <h3 className="text-text-primary font-semibold mb-4">Score Trend</h3>
      <ResponsiveContainer width="100%" height={220}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#2a2a2a" />
          <XAxis dataKey="name" stroke="#8a8a8a" fontSize={12} />
          <YAxis domain={[0, 10]} stroke="#8a8a8a" fontSize={12} />
          <Tooltip
            contentStyle={{ backgroundColor: '#1a1a1a', border: '1px solid #2a2a2a', borderRadius: '8px' }}
            labelStyle={{ color: '#fafafa' }}
          />
          <Line type="monotone" dataKey="score" stroke="#5eead4" strokeWidth={2} dot={{ fill: '#5eead4' }} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

export default ScoreTrendChart