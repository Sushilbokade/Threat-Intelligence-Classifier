import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch
from app.threat_classifier import ThreatClassifier
from app.models import ThreatClassification

@pytest_asyncio.fixture
async def classifier():
    # Mock the OpenAI API calls
    with patch("langchain_openai.ChatOpenAI") as mock_chat:
        # Create a mock classifier and configure its chain directly
        classifier = ThreatClassifier()
        # Mock the chain's ainvoke method
        mock_chain = AsyncMock()
        mock_chain.ainvoke.side_effect = _mock_classification_response
        classifier.chain = mock_chain
        yield classifier

async def _mock_classification_response(text: str) -> ThreatClassification:
    """Mock classification response"""
    # Extract the actual text from the input dict
    input_text = text["text"] if isinstance(text, dict) else text
    
    # Return ThreatClassification objects directly
    if "malware" in input_text.lower() or "C&C" in input_text.lower() or "system32" in input_text.lower():
        return ThreatClassification(
            threat_level="CRITICAL",
            explanation="Malware detected with C&C communication",
            confidence=0.95
        )
    elif "root" in input_text.lower() or "multiple password attempts" in input_text.lower():
        return ThreatClassification(
            threat_level="HIGH",
            explanation="Unauthorized root access attempt detected",
            confidence=0.9
        )
    elif "unusual" in input_text.lower() or "multiple" in input_text.lower():
        return ThreatClassification(
            threat_level="MEDIUM",
            explanation="Unusual pattern detected",
            confidence=0.7
        )
    else:
        return ThreatClassification(
            threat_level="LOW",
            explanation="No significant threats detected",
            confidence=0.8
        )

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