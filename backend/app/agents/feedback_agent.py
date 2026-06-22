import json

from langchain_groq import ChatGroq

from app.config import settings
from app.agents.state import InterviewState


FEEDBACK_GENERATION_PROMPT = """You are providing constructive interview feedback based on a candidate's performance.

Evaluations across all answers:
{evaluations_summary}

Candidate's resume highlights:
{resume_highlights}

Generate actionable feedback with three sections:

1. Strengths: What did the candidate do well? (2-3 points)
2. Weaknesses: Where did they struggle? (2-3 points)
3. Improvement areas: Concrete suggestions for growth (2-3 points)

Be specific and constructive. Reference actual answers they gave. Tie feedback to their background/skills where relevant.

Return ONLY valid JSON in this exact shape, no markdown, no preamble:
{{
  "strengths": ["strength 1", "strength 2", ...],
  "weaknesses": ["weakness 1", "weakness 2", ...],
  "improvement_areas": ["area 1: specific suggestion", "area 2: specific suggestion", ...]
}}
"""


def feedback_agent(state: InterviewState) -> dict:
    """
    LangGraph node: synthesizes evaluations + resume data into actionable feedback.
    """
    evaluations = state.get("evaluations", [])
    resume_data = state.get("resume_data", {})

    evaluations_summary = "\n".join(
        f"Q: {e['question']}\n"
        f"  Technical: {e['technical_accuracy']}/10, Communication: {e['communication']}/10, "
        f"Problem-Solving: {e['problem_solving']}/10, Depth: {e['depth']}/10\n"
        f"  Summary: {e['summary']}"
        for e in evaluations
    )

    resume_highlights = f"Skills: {', '.join(resume_data.get('skills', [])[:10])}. " \
                        f"Projects: {', '.join(p['name'] for p in resume_data.get('projects', []))}. " \
                        f"Experience: {'; '.join(e['role'] for e in resume_data.get('experience', []))}"

    llm = ChatGroq(
        api_key=settings.groq_api_key,
        model="llama-3.3-70b-versatile",
        temperature=0.2,
    )

    prompt = FEEDBACK_GENERATION_PROMPT.format(
        evaluations_summary=evaluations_summary,
        resume_highlights=resume_highlights,
    )
    response = llm.invoke(prompt)
    raw_output = response.content.strip()

    if raw_output.startswith("```"):
        raw_output = raw_output.strip("`")
        if raw_output.startswith("json"):
            raw_output = raw_output[4:].strip()

    try:
        feedback = json.loads(raw_output)
    except json.JSONDecodeError:
        feedback = {
            "strengths": [],
            "weaknesses": [],
            "improvement_areas": [],
        }

    return {"feedback": feedback}