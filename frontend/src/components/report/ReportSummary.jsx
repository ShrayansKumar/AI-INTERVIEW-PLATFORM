function ReportSummary({ report }) {
  if (!report) return null

  const { final_report, evaluations } = report
  const metrics = final_report.interview_metrics || {}
  const feedback = final_report.feedback || {}

  return (
    <div className="space-y-6 max-w-3xl">
      {/* Overall score + recommendation */}
      <div className="bg-bg-card border border-border rounded-2xl p-6">
        <p className="text-text-secondary text-sm mb-1">Overall Score</p>
        <p className="text-text-primary text-4xl font-bold mb-3">
          {metrics.overall_score} / 10
        </p>
        <span className="inline-block bg-accent-soft text-accent text-sm font-medium px-3 py-1.5 rounded-full">
          {final_report.recommendation}
        </span>
      </div>

      {/* Metric breakdown */}
      <div className="bg-bg-card border border-border rounded-2xl p-6">
        <h3 className="text-text-primary font-semibold mb-4">Metric Breakdown</h3>
        <div className="grid grid-cols-2 gap-4">
          {[
            ['Technical Accuracy', metrics.average_technical_accuracy],
            ['Communication', metrics.average_communication],
            ['Problem Solving', metrics.average_problem_solving],
            ['Depth', metrics.average_depth],
          ].map(([label, value]) => (
            <div key={label} className="bg-bg-card-hover rounded-xl p-4">
              <p className="text-text-secondary text-xs mb-1">{label}</p>
              <p className="text-text-primary text-xl font-bold">{value} / 10</p>
            </div>
          ))}
        </div>
      </div>

      {/* Strengths / Weaknesses / Improvements */}
      {[
        ['Strengths', feedback.strengths, 'text-accent'],
        ['Weaknesses', feedback.weaknesses, 'text-amber-400'],
        ['Improvement Areas', feedback.improvement_areas, 'text-text-secondary'],
      ].map(([title, items, color]) => (
        <div key={title} className="bg-bg-card border border-border rounded-2xl p-6">
          <h3 className={`font-semibold mb-3 ${color}`}>{title}</h3>
          <ul className="space-y-2">
            {(items || []).map((item, i) => (
              <li key={i} className="text-text-primary text-sm leading-relaxed">
                • {item}
              </li>
            ))}
          </ul>
        </div>
      ))}

      {/* Question-by-question */}
      <div className="bg-bg-card border border-border rounded-2xl p-6">
        <h3 className="text-text-primary font-semibold mb-4">Question Breakdown</h3>
        <div className="space-y-4">
          {(evaluations || []).map((ev, i) => (
            <div key={i} className="border-b border-border pb-4 last:border-0 last:pb-0">
              <p className="text-text-primary text-sm font-medium mb-1">
                Q{i + 1}: {ev.question}
              </p>
              <p className="text-text-secondary text-xs mb-2">{ev.summary}</p>
              <div className="flex gap-3 text-xs">
                <span className="text-accent">Technical: {ev.technical_accuracy}/10</span>
                <span className="text-text-secondary">Communication: {ev.communication}/10</span>
                <span className="text-text-secondary">Problem Solving: {ev.problem_solving}/10</span>
                <span className="text-text-secondary">Depth: {ev.depth}/10</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default ReportSummary