import { useState, useCallback } from "react";
import apiClient from "../lib/apiClient";

export function useInterviewSession() {
  const [sessionId, setSessionId] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [currentAudioBase64, setCurrentAudioBase64] = useState(null);
  const [transcript, setTranscript] = useState("");
  const [interviewComplete, setInterviewComplete] = useState(false);
  const [questionIndex, setQuestionIndex] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const initSession = useCallback((id, question, audioBase64) => {
    setSessionId(id);
    setCurrentQuestion(question);
    setCurrentAudioBase64(audioBase64);
    setInterviewComplete(false);
    setQuestionIndex(0);
    setTranscript("");
  }, []);

  const submitAnswer = useCallback(
    async (audioBlob) => {
      if (!sessionId) {
        setError("No active session.");
        return;
      }

      setLoading(true);
      setError("");

      const formData = new FormData();
      formData.append("file", audioBlob, "answer.webm");

      try {
        const response = await apiClient.post(
          `/api/v1/interview/answer-voice?session_id=${sessionId}`,
          formData,
          { headers: { "Content-Type": "multipart/form-data" } },
        );

        const data = response.data;
        setTranscript(data.transcript);
        setCurrentQuestion(data.next_question);
        setCurrentAudioBase64(data.next_question_audio_url);
        setInterviewComplete(data.interview_complete);
        setQuestionIndex(data.current_question_index);

        return data;
      } catch (err) {
        setError(err.response?.data?.detail || "Failed to submit answer.");
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [sessionId],
  );

  return {
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
  };
}
