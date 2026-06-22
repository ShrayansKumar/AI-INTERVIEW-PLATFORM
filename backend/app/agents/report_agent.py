from app.agents.state import InterviewState


def report_agent(state: InterviewState) -> dict:
    """
    LangGraph node: compiles the final interview report summarizing
    all data: resume, questions asked, scores, feedback, and overall recommendation.
    """
    resume_data = state.get("resume_data", {})
    company_name = state.get("company_name", "")
    questions = state.get("questions", [])
    evaluations = state.get("evaluations", [])
    feedback = state.get("feedback", {})

    # Calculate average scores across all questions
    if evaluations:
        avg_technical = sum(e.get("technical_accuracy", 0) for e in evaluations) / len(evaluations)
        avg_communication = sum(e.get("communication", 0) for e in evaluations) / len(evaluations)
        avg_problem_solving = sum(e.get("problem_solving", 0) for e in evaluations) / len(evaluations)
        avg_depth = sum(e.get("depth", 0) for e in evaluations) / len(evaluations)
        overall_score = (avg_technical + avg_communication + avg_problem_solving + avg_depth) / 4
    else:
        avg_technical = avg_communication = avg_problem_solving = avg_depth = overall_score = 0

    # Generate recommendation based on overall score
    if overall_score >= 7.5:
        recommendation = "STRONG PASS - Recommend for next round"
    elif overall_score >= 6:
        recommendation = "PASS - Candidate shows promise, consider for next round"
    elif overall_score >= 4:
        recommendation = "BORDERLINE - Consider with additional context or focused follow-up"
    else:
        recommendation = "DOES NOT MEET BAR - Not recommended for advancement"

    final_report = {
        "company": company_name,
        "candidate_summary": {
            "top_skills": resume_data.get("skills", [])[:5],
            "projects": [p["name"] for p in resume_data.get("projects", [])],
        },
        "interview_metrics": {
            "questions_asked": len(questions),
            "average_technical_accuracy": round(avg_technical, 2),
            "average_communication": round(avg_communication, 2),
            "average_problem_solving": round(avg_problem_solving, 2),
            "average_depth": round(avg_depth, 2),
            "overall_score": round(overall_score, 2),
        },
        "feedback": feedback,
        "recommendation": recommendation,
    }

    return {"final_report": final_report}