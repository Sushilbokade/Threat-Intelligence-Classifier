from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import LogEntry, ThreatClassification, ClassificationHistory
from .threat_classifier import ThreatClassifier
from .database import init_indices, store_classification, get_recent_classifications
from typing import List

app = FastAPI(
    title="Threat Intelligence Classifier",
    description="LLM-powered security threat classification API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize classifier
classifier = ThreatClassifier()

@app.on_event("startup")
async def startup_event():
    """Initialize Elasticsearch indices on startup"""
    await init_indices()

@app.post("/classify", response_model=ThreatClassification)
async def classify_threat(log_entry: LogEntry):
    """
    Classify a log entry for security threats
    """
    try:
        # Get classification from LLM
        classification = await classifier.classify(log_entry.text)
        
        # Store the result in Elasticsearch
        await store_classification(log_entry.text, classification.dict())
        
        return classification
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history", response_model=List[ClassificationHistory])
async def get_classification_history():
    """
    Retrieve recent threat classifications
    """
    try:
        return await get_recent_classifications()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))