from app.agents.state import InterviewState
from app.services.resume_parser_service import structure_resume_text


def resume_agent(state: InterviewState) -> dict:
    """
    LangGraph node: structures the raw resume text into skills/projects/experience.
    """
    resume_text = state["resume_text"]
    structured_data = structure_resume_text(resume_text)

    return {"resume_data": structured_data}