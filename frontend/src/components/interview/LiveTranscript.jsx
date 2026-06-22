function LiveTranscript({ transcript }) {
  if (!transcript) return null

  return (
    <div className="bg-bg-card-hover border border-border rounded-xl p-4 max-w-2xl">
      <p className="text-text-secondary text-xs mb-1">Your last answer (transcribed)</p>
      <p className="text-text-primary text-sm">{transcript}</p>
    </div>
  )
}

export default LiveTranscript