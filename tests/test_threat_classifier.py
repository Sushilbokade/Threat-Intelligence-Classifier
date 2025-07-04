import pytest
from app.threat_classifier import ThreatClassifier
from app.models import ThreatClassification
import os

@pytest.fixture
def classifier():
    return ThreatClassifier()

@pytest.mark.asyncio
async def test_classify_high_threat(classifier):
    """Test classification of a high-threat log entry"""
    log_entry = "Failed root login attempt from unknown IP 185.234.123.45 with multiple password attempts"
    result = await classifier.classify(log_entry)
    
    assert isinstance(result, ThreatClassification)
    assert result.threat_level == "HIGH"
    assert result.confidence >= 0.8
    assert "unauthorized" in result.explanation.lower()

@pytest.mark.asyncio
async def test_classify_low_threat(classifier):
    """Test classification of a low-threat log entry"""
    log_entry = "User logged in successfully from internal IP 192.168.1.100"
    result = await classifier.classify(log_entry)
    
    assert isinstance(result, ThreatClassification)
    assert result.threat_level == "LOW"
    assert result.confidence >= 0.8

@pytest.mark.asyncio
async def test_classify_medium_threat(classifier):
    """Test classification of a medium-threat log entry"""
    log_entry = "Unusual file access pattern detected: user accessing multiple sensitive files in quick succession"
    result = await classifier.classify(log_entry)
    
    assert isinstance(result, ThreatClassification)
    assert result.threat_level == "MEDIUM"
    assert result.confidence >= 0.7

@pytest.mark.asyncio
async def test_classify_critical_threat(classifier):
    """Test classification of a critical-threat log entry"""
    log_entry = "Detected malware signature in system32, multiple encrypted connections to known C&C servers"
    result = await classifier.classify(log_entry)
    
    assert isinstance(result, ThreatClassification)
    assert result.threat_level == "CRITICAL"
    assert result.confidence >= 0.9