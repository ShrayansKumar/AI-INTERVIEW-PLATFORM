import json

from langchain_groq import ChatGroq

from app.config import settings
from app.agents.state import InterviewState


EVALUATION_PROMPT = """You are an expert technical interviewer evaluating a candidate's answer.

Question asked:
"{question}"

Candidate's answer:
"{answer}"

Score this answer on four dimensions, each from 0 to 10 (0 = no merit, 10 = expert-level):
- technical_accuracy: Is the technical content correct and precise?
- communication: Is the answer clearly structured and easy to follow?
- problem_solving: Does the answer show structured reasoning, tradeoff awareness, and a logical approach?
- depth: Does the answer go beyond surface-level facts into genuine understanding?

Be a strict, realistic evaluator. A vague, generic, or placeholder answer (e.g. "it's a React app", "string", "I don't know")
should score very low (0-2) across all dimensions. A specific, technically grounded, well-reasoned answer should score
high (7-10). Most real answers fall somewhere in between -- use the full range, do not default to the middle.

Return ONLY valid JSON in this exact shape, no markdown, no preamble:
{{"technical_accuracy": <int>, "communication": <int>, "problem_solving": <int>, "depth": <int>, "summary": "one sentence justification"}}
"""


def evaluation_agent(state: InterviewState) -> dict:
    """
    LangGraph node: scores every Q&A pair in conversation_history on
    technical accuracy, communication, problem solving, and depth.
    """
    conversation_history = state.get("conversation_history", [])

    llm = ChatGroq(
        api_key=settings.groq_api_key,
        model="llama-3.3-70b-versatile",
        temperature=0,
    )

    evaluations = []

    for turn in conversation_history:
        question = turn["question"]
        answer = turn["answer"]

        prompt = EVALUATION_PROMPT.format(question=question, answer=answer)
        response = llm.invoke(prompt)
        raw_output = response.content.strip()

        if raw_output.startswith("```"):
            raw_output = raw_output.strip("`")
            if raw_output.startswith("json"):
                raw_output = raw_output[4:].strip()

        try:
            scores = json.loads(raw_output)
        except json.JSONDecodeError:
            scores = {
                "technical_accuracy": 0,
                "communication": 0,
                "problem_solving": 0,
                "depth": 0,
                "summary": "Evaluation parsing failed",
            }

        evaluations.append({
            "question": question,
            "answer": answer,
            **scores,
        })

    return {"evaluations": evaluations}