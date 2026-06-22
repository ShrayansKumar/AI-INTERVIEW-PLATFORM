from typing import TypedDict, Optional


class InterviewState(TypedDict):
    resume_text: str
    company_name: str
    user_id: Optional[str]  # NEW — needed for question_agent to retrieve this user's resume chunks

    resume_data: Optional[dict]

    company_context: Optional[str]
    questions: Optional[list[str]]

    current_question_index: Optional[int]
    conversation_history: Optional[list[dict]]
    latest_answer: Optional[str]
    next_question: Optional[str]
    interview_complete: Optional[bool]
    followup_count: Optional[int]

    evaluations: Optional[list[dict]]
    feedback: Optional[dict]
    final_report: Optional[dict]