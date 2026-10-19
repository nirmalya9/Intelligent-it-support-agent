from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from app.schemas import TicketRequest, TicketAnalysis
from app.agent.graph import analyze_ticket
load_dotenv()
app = FastAPI(title="Intelligent IT Support Agent", description="ML classification, RAG, LangGraph and simulated diagnostics", version="1.0.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/tickets/analyze", response_model=TicketAnalysis)
def analyze(request: TicketRequest):
    try:
        result = analyze_ticket(request.title, request.description)
        return TicketAnalysis(ticket_title=request.title, predicted_category=result["category"],
            category_confidence=round(result["confidence"], 4), priority=result["priority"],
            recommendation=result["recommendation"], response=result["response"],
            sources=[{"title": s["title"], "source": s["source"], "excerpt": s["excerpt"], "score": round(s["score"], 4)} for s in result.get("sources", [])],
            diagnostics=result.get("diagnostics", {}), audit_trail=result.get("audit_trail", []),
            disclaimer="Demo only. Diagnostics are simulated; recommendations require human review.")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Ticket analysis failed: {type(exc).__name__}: {exc}")

@app.get("/classifier/evaluate")
def evaluate_classifier():
    from app.ml.classifier import evaluate_holdout
    try:
        return evaluate_holdout()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
