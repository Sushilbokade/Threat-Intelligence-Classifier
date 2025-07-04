from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class LogEntry(BaseModel):
    text: str = Field(..., description="The log entry text to analyze")

class ThreatClassification(BaseModel):
    threat_level: str = Field(..., description="The classified threat level (LOW, MEDIUM, HIGH, CRITICAL)")
    explanation: str = Field(..., description="Detailed explanation of the threat classification")
    confidence: float = Field(..., description="Confidence score of the classification", ge=0.0, le=1.0)

class ClassificationHistory(BaseModel):
    text: str
    threat_level: str
    explanation: str
    confidence: float
    timestamp: datetime