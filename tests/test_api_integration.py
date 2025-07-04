import pytest
from fastapi.testclient import TestClient
from app.main import app
import json
from datetime import datetime, timedelta

client = TestClient(app)

def test_classify_endpoint():
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
        response = client.post(
            "/classify",
            json={"text": case["text"]}
        )
        
        assert response.status_code == 200
        result = response.json()
        assert result["threat_level"] in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        assert result["confidence"] >= 0.0 and result["confidence"] <= 1.0
        assert len(result["explanation"]) > 0
        if case["expected_level"]:
            assert result["threat_level"] == case["expected_level"]

def test_history_endpoint():
    """Test the /history endpoint"""
    # First, create some classifications
    test_logs = [
        "Failed login attempt from IP 10.0.0.1",
        "System crash detected",
        "New user account created"
    ]
    
    for log in test_logs:
        client.post("/classify", json={"text": log})
    
    # Now test the history endpoint
    response = client.get("/history")
    assert response.status_code == 200
    history = response.json()
    
    assert isinstance(history, list)
    assert len(history) > 0
    
    # Verify the structure of history items
    for item in history:
        assert "text" in item
        assert "threat_level" in item
        assert "explanation" in item
        assert "confidence" in item
        assert "timestamp" in item
        
        # Verify timestamp is recent
        timestamp = datetime.fromisoformat(item["timestamp"].replace("Z", "+00:00"))
        assert datetime.utcnow() - timestamp < timedelta(minutes=5)

def test_error_handling():
    """Test API error handling"""
    # Test empty input
    response = client.post("/classify", json={"text": ""})
    assert response.status_code == 422
    
    # Test missing text field
    response = client.post("/classify", json={})
    assert response.status_code == 422
    
    # Test invalid JSON
    response = client.post(
        "/classify",
        headers={"Content-Type": "application/json"},
        data="invalid json"
    )
    assert response.status_code == 422