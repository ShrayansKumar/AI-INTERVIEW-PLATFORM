import json

from langchain_groq import ChatGroq

from app.config import settings
from app.services.embedding_service import generate_embedding


CHUNKING_PROMPT = """You are splitting a resume into meaningful, detailed chunks for retrieval.

Below is the full raw resume text. Split it into chunks by section (e.g. each project gets its own chunk,
each work/research experience gets its own chunk, education gets its own chunk, coursework gets its own chunk,
each extracurricular gets its own chunk, skills get their own chunk).

CRITICAL: Preserve ALL detail from the original text in each chunk -- bullet points, specific technologies,
metrics, achievements. Do NOT summarize or shorten anything. Copy the relevant text for each section
faithfully, just reorganized into separate chunks.

Return ONLY a valid JSON array of objects in this exact shape, no markdown, no preamble:
[
  {{"section": "project", "content": "full detailed text for this project, all bullet points included"}},
  {{"section": "experience", "content": "full detailed text for this experience entry"}},
  {{"section": "education", "content": "..."}},
  {{"section": "coursework", "content": "..."}},
  {{"section": "extracurricular", "content": "..."}},
  {{"section": "skills", "content": "..."}}
]

Resume text:
---
{resume_text}
---

JSON output:"""


def chunk_resume_text_detailed(raw_text: str) -> list[dict]:
    """
    Uses an LLM to split the FULL raw resume text into detailed, section-based
    chunks -- preserving all bullet points and specifics, not just summary fields.
    """
    llm = ChatGroq(
        api_key=settings.groq_api_key,
        model="llama-3.3-70b-versatile",
        temperature=0,
    )

    prompt = CHUNKING_PROMPT.format(resume_text=raw_text)
    response = llm.invoke(prompt)
    raw_output = response.content.strip()

    if raw_output.startswith("```"):
        raw_output = raw_output.strip("`")
        if raw_output.startswith("json"):
            raw_output = raw_output[4:].strip()

    try:
        chunks = json.loads(raw_output)
    except json.JSONDecodeError:
        # Fallback: treat the whole resume as one chunk rather than failing entirely
        chunks = [{"section": "raw", "content": raw_text}]

    return chunks


async def embed_and_store_resume_chunks(db, user_id, structured_data: dict, raw_text: str):
    from app.models.resume_chunk import ResumeChunk
    from sqlalchemy import delete

    # Clear old chunks for this user first (resume may have been re-uploaded)
    await db.execute(delete(ResumeChunk).where(ResumeChunk.user_id == user_id))

    chunks = chunk_resume_text_detailed(raw_text)

    for chunk in chunks:
        content = chunk.get("content", "").strip()
        if not content:
            continue
        embedding = generate_embedding(content)
        db.add(ResumeChunk(
            user_id=user_id,
            content=content,
            section=chunk.get("section", "raw"),
            embedding=embedding,
        ))

    await db.commit()