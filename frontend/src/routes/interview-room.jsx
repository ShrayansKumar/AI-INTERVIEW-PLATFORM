import { useEffect, useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import Sidebar from '../components/dashboard/Sidebar'
import VoiceRoom from '../components/interview/VoiceRoom'
import { useInterviewSession } from '../hooks/useInterviewSession'
import apiClient from '../lib/apiClient'

function InterviewRoomPage() {
  const location = useLocation()
  const navigate = useNavigate()
  const startData = location.state

  const [exiting, setExiting] = useState(false)

  const {
    sessionId,
    currentQuestion,
    currentAudioBase64,
    transcript,
    interviewComplete,
    questionIndex,
    loading,
    error,
    initSession,
    submitAnswer,
  } = useInterviewSession()

  useEffect(() => {
    if (!startData?.session_id) {
      navigate('/resume-upload')
      return
    }
    initSession(startData.session_id, startData.next_question, startData.next_question_audio_url)
  }, [])

  useEffect(() => {
    if (interviewComplete && sessionId) {
      navigate(`/report/${sessionId}`)
    }
  }, [interviewComplete, sessionId])

  const handleQuietExit = async () => {
    if (!confirm('Exit the interview now? Nothing will be saved.')) return

    setExiting(true)
    try {
      if (sessionId) {
        await apiClient.delete(`/api/v1/interview/${sessionId}`)
      }
    } catch (err) {
      console.error('Failed to delete session:', err)
    } finally {
      navigate('/')
    }
  }

  if (!startData?.session_id) return null

  return (
    <div className="flex">
      <Sidebar />
      <main className="flex-1 p-8 bg-bg-base min-h-screen flex flex-col items-center justify-center relative">
        <button
          onClick={handleQuietExit}
          disabled={exiting}
          className="absolute top-6 right-8 text-text-secondary text-sm hover:text-red-400 transition-colors disabled:opacity-50"
        >
          {exiting ? 'Exiting...' : '✕ Exit interview'}
        </button>

        {error && <p className="text-red-400 text-sm mb-4 absolute top-8">{error}</p>}

        <VoiceRoom
          currentQuestion={currentQuestion}
          currentAudioBase64={currentAudioBase64}
          transcript={transcript}
          questionIndex={questionIndex}
          loading={loading}
          onSubmitAnswer={submitAnswer}
        />
      </main>
    </div>
  )
}

export default InterviewRoomPage