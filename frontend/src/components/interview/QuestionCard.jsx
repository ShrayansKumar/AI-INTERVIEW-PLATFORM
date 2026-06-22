function QuestionCard({ question, questionIndex, totalQuestions = 5 }) {
  return (
    <div className="bg-bg-card border border-border rounded-2xl p-6 max-w-2xl">
      <p className="text-accent text-xs font-medium mb-2">
        Question {questionIndex + 1}
      </p>
      <p className="text-text-primary text-lg leading-relaxed">{question}</p>
    </div>
  )
}

export default QuestionCard