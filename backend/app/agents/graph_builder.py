from langgraph.graph import StateGraph, END

from app.agents.state import InterviewState
from app.agents.resume_agent import resume_agent
from app.agents.question_agent import question_agent
from app.agents.interview_agent import interview_agent
from app.agents.evaluation_agent import evaluation_agent
from app.agents.feedback_agent import feedback_agent
from app.agents.report_agent import report_agent


def interview_loop_condition(state: InterviewState) -> str:
    """
    Conditional edge: if interview is complete, move to evaluation.
    Otherwise, loop back to interview_agent for the next question.
    """
    if state.get("interview_complete"):
        return "evaluation_agent"
    else:
        return "interview_agent"


def build_graph():
    graph = StateGraph(InterviewState)

    # Add all 6 nodes
    graph.add_node("resume_agent", resume_agent)
    graph.add_node("question_agent", question_agent)
    graph.add_node("interview_agent", interview_agent)
    graph.add_node("evaluation_agent", evaluation_agent)
    graph.add_node("feedback_agent", feedback_agent)
    graph.add_node("report_agent", report_agent)

    # Linear chain: resume → question
    graph.set_entry_point("resume_agent")
    graph.add_edge("resume_agent", "question_agent")

    # After question_agent, initialize the interview loop
    graph.add_edge("question_agent", "interview_agent")

    # Conditional: interview_agent loops back to itself if not complete, else advances
    graph.add_conditional_edges(
        "interview_agent",
        interview_loop_condition,
        {
            "interview_agent": "interview_agent",
            "evaluation_agent": "evaluation_agent",
        }
    )

    # Linear chain: evaluation → feedback → report → END
    graph.add_edge("evaluation_agent", "feedback_agent")
    graph.add_edge("feedback_agent", "report_agent")
    graph.add_edge("report_agent", END)

    return graph.compile()


interview_graph = build_graph()