from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Any
from app.ml.classifier import TicketClassifier
from app.rag.retriever import KnowledgeRetriever
from app.tools.diagnostics import run_simulated_diagnostics
from app.agent.llm import generate_with_optional_llm

classifier = TicketClassifier()
retriever = KnowledgeRetriever()

class AgentState(TypedDict, total=False):
    title: str
    description: str
    category: str
    confidence: float
    priority: str
    sources: list[dict[str, Any]]
    diagnostics: dict[str, str]
    recommendation: str
    response: str
    audit_trail: list[str]


def classify_node(state):
    result = classifier.predict(state["title"], state["description"])
    text = f"{state['title']} {state['description']}".lower()
    urgent_terms = ["multiple users", "business critical", "security breach", "suspected compromise", "production down"]
    priority = "high" if any(t in text for t in urgent_terms) else ("medium" if result["confidence"] < .45 else "low")
    return {"category": result["category"], "confidence": result["confidence"], "priority": priority,
            "audit_trail": state.get("audit_trail", []) + [f"ML classifier predicted {result['category']} (confidence {result['confidence']:.3f}).",
            f"Priority heuristic suggested {priority}; this is not an enterprise SLA assessment."]}


def retrieve_node(state):
    sources = retriever.search(f"{state['title']}. {state['description']}. Category: {state['category']}", k=3)
    return {"sources": sources, "audit_trail": state.get("audit_trail", []) + [f"Retrieved {len(sources)} knowledge chunks using semantic search."]}


def diagnose_node(state):
    diagnostics = run_simulated_diagnostics(state["category"], state["title"], state["description"])
    return {"diagnostics": diagnostics, "audit_trail": state.get("audit_trail", []) + ["Ran safe simulated diagnostics; no real systems were contacted."]}


def decide_node(state):
    text = f"{state['title']} {state['description']}".lower()
    urgent = any(t in text for t in ["multiple users", "business critical", "security breach", "suspected compromise", "production down"])
    best_score = max([s["score"] for s in state.get("sources", [])], default=0)
    if urgent:
        decision = "escalate"
    elif state.get("confidence", 0) < .35 or not state.get("sources") or best_score < .20:
        decision = "request_information"
    else:
        decision = "recommend_resolve"
    return {"recommendation": decision, "audit_trail": state.get("audit_trail", []) + [f"Decision {decision} based on simple rules, confidence, and retrieval scores; human review required."]}


def respond_node(state):
    sources = state.get("sources", [])
    ticket = {"title": state["title"], "description": state["description"]}
    response = generate_with_optional_llm(ticket, state["category"], state["priority"], sources,
                                          state.get("diagnostics", {}), state["recommendation"])
    if response:
        mode = "Optional LLM generated a response using retrieved evidence."
    else:
        if state["recommendation"] == "escalate":
            response = "Escalate to the appropriate support team using the official incident process. Do not attempt unapproved remediation."
        elif state["recommendation"] == "request_information":
            response = "The evidence is insufficient for a confident recommendation. Ask for the exact error, affected application/device, approximate time, and whether others are affected. Never request passwords, MFA codes, or tokens."
        else:
            response = "Suggested next steps from retrieved troubleshooting notes:\n" + "\n".join(f"- {s['excerpt']}" for s in sources[:2]) + "\n\nThese are recommendations only; no real diagnostic or remediation action was performed."
        response += "\n\nEvidence sources: " + (", ".join(s["source"] for s in sources) if sources else "none retrieved")
        mode = "Deterministic response template; no LLM API called."
    return {"response": response, "audit_trail": state.get("audit_trail", []) + [mode]}


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("classify", classify_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("diagnose", diagnose_node)
    graph.add_node("decide", decide_node)
    graph.add_node("respond", respond_node)
    graph.add_edge(START, "classify")
    graph.add_edge("classify", "retrieve")
    graph.add_edge("retrieve", "diagnose")
    graph.add_edge("diagnose", "decide")
    graph.add_edge("decide", "respond")
    graph.add_edge("respond", END)
    return graph.compile()

agent_graph = build_graph()


def analyze_ticket(title: str, description: str) -> dict:
    return agent_graph.invoke({"title": title, "description": description, "audit_trail": ["Ticket received."]})
