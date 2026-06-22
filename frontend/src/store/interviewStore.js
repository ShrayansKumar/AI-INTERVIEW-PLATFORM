import { create } from "zustand";

export const useInterviewStore = create((set) => ({
  sessionId: null,
  currentQuestion: null,
  currentQuestionAudio: null,
  interviewComplete: false,
  currentQuestionIndex: 0,

  startSession: (sessionId, firstQuestion) =>
    set({
      sessionId,
      currentQuestion: firstQuestion,
      interviewComplete: false,
      currentQuestionIndex: 0,
    }),

  advanceQuestion: (nextQuestion, audioBase64, isComplete, questionIndex) =>
    set({
      currentQuestion: nextQuestion,
      currentQuestionAudio: audioBase64,
      interviewComplete: isComplete,
      currentQuestionIndex: questionIndex,
    }),

  resetSession: () =>
    set({
      sessionId: null,
      currentQuestion: null,
      currentQuestionAudio: null,
      interviewComplete: false,
      currentQuestionIndex: 0,
    }),
}));
