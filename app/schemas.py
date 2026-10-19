from pydantic import BaseModel, Field
from typing import Literal

class TicketRequest(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=5, max_length=4000)

class SourceDocument(BaseModel):
    title: str
    source: str
    excerpt: str
    score: float

class TicketAnalysis(BaseModel):
    ticket_title: str
    predicted_category: str
    category_confidence: float
    priority: Literal["low", "medium", "high"]
    recommendation: Literal["recommend_resolve", "request_information", "escalate"]
    response: str
    sources: list[SourceDocument]
    diagnostics: dict[str, str]
    audit_trail: list[str]
    disclaimer: str
