import json

from langchain_groq import ChatGroq

from app.config import settings
from app.agents.state import InterviewState


FOLLOWUP_DECISION_PROMPT = """You are conducting a technical interview. Time is limited -- you can ask AT MOST one follow-up per question, and most answers should NOT get a follow-up.

The candidate was asked:
"{question}"

They answered:
"{answer}"

Only request a follow-up if the answer is vague, superficial, evasive, or fails to address the core of the question.
Do NOT request a follow-up just because there is some additional edge case, optimization, or detail the candidate didn't mention --
real answers are never 100% exhaustive, and that is fine. A specific, technically grounded answer that addresses
the main ask should move on, even if minor refinements are theoretically possible.

Return ONLY valid JSON in this exact shape, no markdown, no preamble:
{{"needs_followup": true or false, "followup_question": "the follow-up question text, or empty string if not needed"}}
"""

MAX_FOLLOWUPS_PER_QUESTION = 1


def interview_agent(state: InterviewState) -> dict:
    """
    LangGraph node: manages one turn of the interview conversation.
    """
    questions = state["questions"]
    current_index = state.get("current_question_index", 0)
    conversation_history = state.get("conversation_history", [])
    latest_answer = state.get("latest_answer", "")
    followup_count = state.get("followup_count", 0)

    current_question = questions[current_index]

    updated_history = conversation_history + [
        {"question": current_question, "answer": latest_answer}
    ]

    # Hard cap: if we've already asked the max follow-ups for this question, force advance
    if followup_count >= MAX_FOLLOWUPS_PER_QUESTION:
        next_index = current_index + 1
        next_question = questions[next_index] if next_index < len(questions) else None
        return {
            "conversation_history": updated_history,
            "current_question_index": next_index,
            "next_question": next_question,
            "interview_complete": next_question is None,
            "followup_count": 0,
        }

    llm = ChatGroq(
        api_key=settings.groq_api_key,
        model="llama-3.3-70b-versatile",
        temperature=0.3,
    )

    prompt = FOLLOWUP_DECISION_PROMPT.format(question=current_question, answer=latest_answer)
    response = llm.invoke(prompt)
    raw_output = response.content.strip()

    if raw_output.startswith("```"):
        raw_output = raw_output.strip("`")
        if raw_output.startswith("json"):
            raw_output = raw_output[4:].strip()

    try:
        decision = json.loads(raw_output)
    except json.JSONDecodeError:
        decision = {"needs_followup": False, "followup_question": ""}

    if decision.get("needs_followup") and decision.get("followup_question"):
        return {
            "conversation_history": updated_history,
            "current_question_index": current_index,
            "next_question": decision["followup_question"],
            "interview_complete": False,
            "followup_count": followup_count + 1,
        }
    else:
        next_index = current_index + 1
        next_question = questions[next_index] if next_index < len(questions) else None
        return {
            "conversation_history": updated_history,
            "current_question_index": next_index,
            "next_question": next_question,
            "interview_complete": next_question is None,
            "followup_count": 0,
        }