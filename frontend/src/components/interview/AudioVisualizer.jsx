function AudioVisualizer({ isRecording }) {
  return (
    <div className="flex items-center justify-center gap-1.5 h-12">
      {isRecording ? (
        <>
          {[0, 1, 2, 3, 4].map((i) => (
            <div
              key={i}
              className="w-1.5 bg-accent rounded-full animate-pulse"
              style={{
                height: `${20 + (i % 3) * 10}px`,
                animationDelay: `${i * 0.15}s`,
              }}
            />
          ))}
        </>
      ) : (
        <div className="w-2 h-2 bg-text-secondary rounded-full" />
      )}
    </div>
  )
}

export default AudioVisualizer