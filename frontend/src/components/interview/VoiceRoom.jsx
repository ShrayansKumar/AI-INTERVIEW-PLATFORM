import { useEffect, useRef, useState } from 'react'
import { useAudioRecorder } from '../../hooks/useAudioRecorder'
import AudioVisualizer from './AudioVisualizer'
import QuestionCard from './QuestionCard'
import LiveTranscript from './LiveTranscript'

function base64ToBlobUrl(base64, mimeType = 'audio/wav') {
  if (!base64) return null
  const byteString = atob(base64)
  const byteArray = new Uint8Array(byteString.length)
  for (let i = 0; i < byteString.length; i++) {
    byteArray[i] = byteString.charCodeAt(i)
  }
  const blob = new Blob([byteArray], { type: mimeType })
  return URL.createObjectURL(blob)
}

function VoiceRoom({
  currentQuestion,
  currentAudioBase64,
  transcript,
  questionIndex,
  loading,
  onSubmitAnswer,
}) {
  const { isRecording, error: recordError, startRecording, stopRecording } = useAudioRecorder()
  const audioRef = useRef(null)
  const [hasPlayedCurrentQuestion, setHasPlayedCurrentQuestion] = useState(false)

  // Auto-play the question audio whenever a new question arrives
  useEffect(() => {
    if (currentAudioBase64 && audioRef.current) {
      const url = base64ToBlobUrl(currentAudioBase64)
      audioRef.current.src = url
      audioRef.current.play().catch(() => {
        // Autoplay can be blocked by the browser until the user interacts once —
        // not a bug, just a browser policy. The replay button below handles this.
      })
      setHasPlayedCurrentQuestion(true)

      return () => URL.revokeObjectURL(url)
    }
  }, [currentAudioBase64])

  const handleReplayQuestion = () => {
    audioRef.current?.play()
  }

  const handleRecordToggle = async () => {
    if (isRecording) {
      const blob = await stopRecording()
      if (blob) {
        await onSubmitAnswer(blob)
      }
    } else {
      await startRecording()
    }
  }

  return (
    <div className="flex flex-col items-center gap-6">
      <audio ref={audioRef} className="hidden" />

      <QuestionCard question={currentQuestion} questionIndex={questionIndex} />

      <button
        onClick={handleReplayQuestion}
        className="text-text-secondary text-sm hover:text-accent transition-colors"
      >
        ↻ Replay question
      </button>

      <AudioVisualizer isRecording={isRecording} />

      {recordError && <p className="text-red-400 text-sm">{recordError}</p>}

      <button
        onClick={handleRecordToggle}
        disabled={loading}
        className={`px-8 py-3 rounded-full font-semibold transition-colors disabled:opacity-50 ${
          isRecording
            ? 'bg-red-500 text-white hover:bg-red-600'
            : 'bg-accent text-accent-text hover:opacity-90'
        }`}
      >
        {loading ? 'Processing...' : isRecording ? '■ Stop & submit' : '● Start answering'}
      </button>

      <LiveTranscript transcript={transcript} />
    </div>
  )
}

export default VoiceRoom