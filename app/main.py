from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import LogEntry, ThreatClassification, ClassificationHistory
from .threat_classifier import ThreatClassifier
from .database import init_indices, store_classification, get_recent_classifications
from typing import List

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup application resources"""
    # Startup
    await init_indices()
    yield
    # Cleanup (if needed)
    pass

app = FastAPI(
    title="Threat Intelligence Classifier",
    description="LLM-powered security threat classification API",
    version="1.0.0",
    lifespan=lifespan
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

@app.post("/classify", response_model=ThreatClassification)
async def classify_threat(log_entry: LogEntry):
    """
    Classify a log entry for security threats
    """
    # Validate input
    if not log_entry.text or len(log_entry.text.strip()) == 0:
        raise HTTPException(status_code=422, detail="Log entry text cannot be empty")
    
    try:
        # Get classification from LLM
        classification = await classifier.classify(log_entry.text)
        
        # Store the result in Elasticsearch
        await store_classification(log_entry.text, classification.model_dump())
        
        return classification
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
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