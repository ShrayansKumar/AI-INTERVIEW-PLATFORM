import { useState, useEffect } from 'react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'
import apiClient from '../../lib/apiClient'

function TopicBreakdownChart() {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    apiClient.get('/api/v1/analytics/topic-breakdown')
      .then((res) => {
        const d = res.data
        setData([
          { name: 'Technical', value: d.average_technical_accuracy },
          { name: 'Communication', value: d.average_communication },
          { name: 'Problem Solving', value: d.average_problem_solving },
          { name: 'Depth', value: d.average_depth },
        ])
      })
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <p className="text-text-secondary text-sm">Loading...</p>

  return (
    <div className="bg-bg-card border border-border rounded-2xl p-6">
      <h3 className="text-text-primary font-semibold mb-4">Average Performance by Metric</h3>
      <ResponsiveContainer width="100%" height={220}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#2a2a2a" />
          <XAxis dataKey="name" stroke="#8a8a8a" fontSize={12} />
          <YAxis domain={[0, 10]} stroke="#8a8a8a" fontSize={12} />
          <Tooltip
            contentStyle={{ backgroundColor: '#1a1a1a', border: '1px solid #2a2a2a', borderRadius: '8px' }}
            labelStyle={{ color: '#fafafa' }}
          />
          <Bar dataKey="value" fill="#5eead4" radius={[6, 6, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

export default TopicBreakdownChart