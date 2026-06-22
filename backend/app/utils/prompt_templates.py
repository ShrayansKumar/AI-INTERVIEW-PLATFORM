RESUME_STRUCTURING_PROMPT = """You are a resume parsing assistant. Extract structured information from the resume text below.

Return ONLY valid JSON (no markdown, no preamble, no explanation) in exactly this shape:

{{
  "skills": ["skill1", "skill2", ...],
  "projects": [
    {{"name": "Project Name", "description": "Brief one-line description"}},
    ...
  ],
  "experience": [
    {{"role": "Role Title", "organization": "Org Name", "duration": "approx duration if mentioned"}},
    ...
  ],
  "education": [
    {{"institution": "Name", "degree": "Degree", "cgpa_or_score": "if mentioned"}}
  ],
  "coursework": ["course1", "course2", ...],
  "extracurriculars": [
    {{"activity": "Activity/Role Title", "description": "Brief one-line description"}}
  ]
}}

If a section has no data, return an empty list for it. Do not invent information not present in the text.

Resume text:
---
{resume_text}
---

JSON output:"""