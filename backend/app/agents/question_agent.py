import json

from langchain_groq import ChatGroq

from app.config import settings
from app.agents.state import InterviewState
from app.db.session import AsyncSessionLocal
from app.services.retrieval_service import retrieve_relevant_chunks
from app.services.resume_retrieval_service import retrieve_resume_chunks
from app.services.difficulty_service import compute_next_difficulty, difficulty_instruction


QUESTION_GENERATION_PROMPT = """You are an expert technical interviewer preparing questions for a candidate interviewing at {company_name}.

Relevant excerpts retrieved from the candidate's resume:
{resume_context}

Relevant company-specific context (job requirements, past interview patterns, OA topics):
{company_context}

Difficulty guidance: {difficulty_note}

Generate EXACTLY 5 personalized interview questions, with this STRICT mandatory distribution:

- Question 1: Must be about the candidate's WORK/RESEARCH EXPERIENCE (look for an "experience" section in
  the resume excerpts above -- reference specific technical details, methods, or results mentioned there).
  If truly no experience section exists in the excerpts, ask about the candidate's most technically complex project instead.
- Question 2: Must be about ONE of the candidate's PROJECTS (reference the project name directly).
- Question 3: Must be about a DIFFERENT project than Question 2, OR a company-context technical topic (DSA/system design/DBMS) if only one project exists.
- Question 4: Must draw on EDUCATION or COURSEWORK (e.g. a fundamentals question tied to a listed course).
- Question 5: Must be BEHAVIORAL, ideally referencing an EXTRACURRICULAR activity if one is listed in the excerpts.

Each question must reference SPECIFIC details from the resume excerpts (names, technologies, metrics) --
do not write a generic version of any question. Question 1 in particular must not be skipped or merged into
a project question if an experience section with real content is present in the excerpts above.

Return ONLY a valid JSON array of strings, no markdown, no preamble. Example format:
["question 1", "question 2", "question 3", "question 4", "question 5"]
"""


async def question_agent(state: InterviewState) -> dict:
    company_name = state["company_name"]
    user_id = state.get("user_id")
    evaluations_so_far = state.get("evaluations", [])

    async with AsyncSessionLocal() as db:
        company_chunks = await retrieve_relevant_chunks(
            db, query=f"{company_name} interview questions topics", company=company_name, top_k=5
        )

        resume_chunks = []
        if user_id:
            resume_chunks = await retrieve_resume_chunks(
                db, user_id=user_id, query=f"interview question topics for {company_name} role", top_k=8
            )

    company_context = "\n".join(c.content for c in company_chunks)
    resume_context = "\n".join(c.content for c in resume_chunks) or "No resume data available."

    difficulty_level = compute_next_difficulty(evaluations_so_far)
    difficulty_note = difficulty_instruction(difficulty_level)

    llm = ChatGroq(
        api_key=settings.groq_api_key,
        model="llama-3.3-70b-versatile",
        temperature=0.3,
    )

    prompt = QUESTION_GENERATION_PROMPT.format(
        company_name=company_name,
        resume_context=resume_context,
        company_context=company_context,
        difficulty_note=difficulty_note,
    )

    response = llm.invoke(prompt)
    raw_output = response.content.strip()

    if raw_output.startswith("```"):
        raw_output = raw_output.strip("`")
        if raw_output.startswith("json"):
            raw_output = raw_output[4:].strip()

    try:
        questions = json.loads(raw_output)
    except json.JSONDecodeError:
        raise ValueError(f"LLM did not return valid JSON array. Raw output: {raw_output[:500]}")

    return {
        "company_context": company_context,
        "questions": questions,
    }