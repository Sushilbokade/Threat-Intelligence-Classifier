import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
from app.main import app
from app.models import ThreatClassification
import asyncio
import nest_asyncio
from datetime import datetime

# Enable nested event loops
nest_asyncio.apply()

@pytest_asyncio.fixture
async def mock_es():
    """Mock Elasticsearch client"""
    mock = AsyncMock()
    mock.indices.create = AsyncMock()
    mock.indices.delete = AsyncMock()
    mock.index = AsyncMock()
    mock.search = AsyncMock(return_value={
        "hits": {
            "hits": [
                {
                    "_source": {
                        "text": "Test log entry",
                        "threat_level": "HIGH",
                        "explanation": "Test explanation",
                        "confidence": 0.9,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                }
            ]
        }
    })
    return mock

@pytest_asyncio.fixture
async def test_client(mock_es):
    """Create a test client with mocked dependencies"""
    with patch("app.main.classifier") as mock_classifier, \
         patch("app.database.es", mock_es), \
         patch("app.main.store_classification") as mock_store:
        
        mock_classifier.classify = AsyncMock()
        mock_classifier.classify.side_effect = _mock_classify
        mock_store.return_value = None
        
        with TestClient(app) as client:
            yield client

async def _mock_classify(text: str) -> ThreatClassification:
    """Mock classification logic"""
    if not text:
        raise ValueError("Text cannot be empty")
        
    if "root" in text.lower():
        return ThreatClassification(threat_level="HIGH", explanation="Unauthorized root access attempt detected", confidence=0.9)
    elif "multiple failed" in text.lower():
        return ThreatClassification(threat_level="MEDIUM", explanation="Multiple failed attempts detected", confidence=0.7)
    else:
        return ThreatClassification(threat_level="LOW", explanation="No significant threats detected", confidence=0.8)

@pytest.mark.asyncio
async def test_classify_endpoint(test_client):
    """Test the /classify endpoint with various log entries"""
    test_cases = [
        {
            "text": "Failed root login attempt from unknown IP 185.234.123.45",
            "expected_level": "HIGH"
        },
        {
            "text": "System update completed successfully",
            "expected_level": "LOW"
        },
        {
            "text": "Multiple failed login attempts detected from IP range 192.168.1.0/24",
            "expected_level": "MEDIUM"
        }
    ]
    
    for case in test_cases:
        response = test_client.post("/classify", json={"text": case["text"]})
        assert response.status_code == 200
        result = response.json()
        assert result["threat_level"] == case["expected_level"]
        assert "explanation" in result
        assert "confidence" in result

@pytest.mark.asyncio
async def test_history_endpoint(test_client):
    """Test the /history endpoint"""
    response = test_client.get("/history")
    assert response.status_code == 200
    history = response.json()
    assert isinstance(history, list)
    assert len(history) > 0
    assert "threat_level" in history[0]
    assert "explanation" in history[0]
    assert "confidence" in history[0]
    assert "timestamp" in history[0]

@pytest.mark.asyncio
async def test_error_handling(test_client):
    """Test API error handling"""
    # Test empty input
    response = test_client.post("/classify", json={"text": ""})
    assert response.status_code == 422
    
    # Test missing text field
    response = test_client.post("/classify", json={})
    assert response.status_code == 422
    
    # Test invalid JSON using content parameter instead of data
    response = test_client.post("/classify", content=b"invalid json")
    assert response.status_code == 422