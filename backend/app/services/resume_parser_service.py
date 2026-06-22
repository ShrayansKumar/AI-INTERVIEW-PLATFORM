import json

import fitz  # PyMuPDF
from langchain_groq import ChatGroq

from app.config import settings
from app.utils.prompt_templates import RESUME_STRUCTURING_PROMPT


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts all text content from a PDF file given as raw bytes.
    """
    text_parts = []

    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text_parts.append(page.get_text())

    return "\n".join(text_parts).strip()


def structure_resume_text(resume_text: str) -> dict:
    """
    Sends raw resume text to Groq and returns structured JSON
    with skills, projects, experience, and education.
    """
    llm = ChatGroq(
        api_key=settings.groq_api_key,
        model="llama-3.3-70b-versatile",
        temperature=0,
    )

    prompt = RESUME_STRUCTURING_PROMPT.format(resume_text=resume_text)
    response = llm.invoke(prompt)

    raw_output = response.content.strip()

    # Strip markdown code fences if the model wraps the JSON in ```json ... ```
    if raw_output.startswith("```"):
        raw_output = raw_output.strip("`")
        if raw_output.startswith("json"):
            raw_output = raw_output[4:].strip()

    try:
        structured_data = json.loads(raw_output)
    except json.JSONDecodeError:
        raise ValueError(f"LLM did not return valid JSON. Raw output: {raw_output[:500]}")

    return structured_data