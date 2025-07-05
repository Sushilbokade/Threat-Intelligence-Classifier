# Threat Intelligence Classifier: Usage Guide

## Table of Contents
1. [Overview](#overview)
2. [Installation & Setup](#installation--setup)
3. [Usage Examples](#usage-examples)
4. [Integration Examples](#integration-examples)
5. [Customization Guide](#customization-guide)
6. [Alert Configuration](#alert-configuration)

## Overview

The Threat Intelligence Classifier is a sophisticated security monitoring system that uses AI to analyze and classify potential security threats in real-time. Think of it as a smart security guard for your systems that can:
- Monitor logs and detect threats
- Classify threats into different severity levels
- Send alerts through multiple channels
- Integrate with existing security tools
- Provide detailed explanations of detected threats

### Threat Levels Explained

1. **LOW**: Normal activity
   - Example: "Regular user login from known IP"
   - Action: Log for routine review

2. **MEDIUM**: Suspicious activity
   - Example: "Multiple failed login attempts"
   - Action: Review within 24 hours

3. **HIGH**: Serious security concern
   - Example: "Unauthorized root access attempt"
   - Action: Investigate within 1 hour

4. **CRITICAL**: Immediate threat
   - Example: "Detected malware with C&C communication"
   - Action: Immediate response required

## Installation & Setup

### Quick Start (Docker)

1. Clone the repository:
```bash
git clone <repository-url>
cd threat-intelligence-classifier
```

2. Create .env file:
```env
OPENAI_API_KEY=your_key_here
ELASTICSEARCH_HOST=elasticsearch
ELASTICSEARCH_USER=elastic
ELASTICSEARCH_PASSWORD=changeme
```

3. Start with Docker Compose:
```bash
docker compose up -d
```

### Manual Setup

1. System Requirements:
   - Python 3.8+
   - Elasticsearch 7.x
   - OpenAI API access

2. Install Dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure Environment:
   - Set up environment variables
   - Initialize Elasticsearch indices
   - Start the FastAPI server

## Usage Examples

### 1. Basic Log Analysis

```python
import requests

# Single log analysis
response = requests.post(
    "http://localhost:8000/classify",
    json={
        "text": "Failed login attempt from IP 192.168.1.100"
    }
)
result = response.json()
print(f"Threat Level: {result['threat_level']}")
print(f"Explanation: {result['explanation']}")
```

### 2. Real-time Log Monitoring

```python
import asyncio
from app.threat_classifier import ThreatClassifier
from app.integrations.alert_manager import AlertManager

async def monitor_log_file(filename: str):
    classifier = ThreatClassifier()
    alert_manager = AlertManager({
        "slack": {"webhook_url": "your-webhook-url"},
        "email": {
            "smtp_server": "smtp.company.com",
            "from_addr": "security@company.com",
            "to_addrs": ["security-team@company.com"]
        }
    })
    
    position = 0
    while True:
        with open(filename, 'r') as f:
            f.seek(position)
            new_lines = f.readlines()
            position = f.tell()
            
            for line in new_lines:
                classification = await classifier.classify(line)
                await alert_manager.process_classification(classification, line)
        
        await asyncio.sleep(1)
```

### 3. Web Application Security

```python
from fastapi import FastAPI
from app.integrations.web_monitor import WebSecurityMonitor

app = FastAPI()

# Add security monitoring
app.add_middleware(
    WebSecurityMonitor,
    alert_config={
        "slack": {"webhook_url": "your-webhook-url"}
    },
    excluded_paths=["/health", "/docs"]
)

# Your API endpoints
@app.post("/api/data")
async def handle_data(data: dict):
    return {"status": "processed"}
```

## Integration Examples

### 1. SIEM Integration

```python
async def enhance_siem_alerts(alert_data: dict):
    classifier = ThreatClassifier()
    
    log_entry = f"""
    Source: {alert_data['source']}
    Event ID: {alert_data['event_id']}
    Description: {alert_data['description']}
    Raw Data: {alert_data['raw_data']}
    """
    
    classification = await classifier.classify(log_entry)
    
    return {
        **alert_data,
        "ai_analysis": classification.dict()
    }
```

### 2. Windows Event Log Monitoring

```python
import win32evtlog

async def monitor_windows_events():
    classifier = ThreatClassifier()
    alert_manager = AlertManager(config)
    
    server = 'localhost'
    logtype = 'Security'
    hand = win32evtlog.OpenEventLog(server, logtype)
    
    while True:
        events = win32evtlog.ReadEventLog(
            hand,
            win32evtlog.EVENTLOG_BACKWARDS_READ|
            win32evtlog.EVENTLOG_SEQUENTIAL_READ,
            0
        )
        
        for event in events:
            log_entry = format_windows_event(event)
            classification = await classifier.classify(log_entry)
            await alert_manager.process_classification(
                classification, 
                log_entry
            )
```

## Customization Guide

### 1. Custom Threat Detection Rules

You can customize the threat analysis by modifying the prompt templates for specific security domains:

#### Database Security Template:
```python
DB_SECURITY_TEMPLATE = """
Analyze the following database log for threats:

{text}

Consider:
- SQL injection attempts
- Unauthorized table access
- Mass data retrieval
- Schema modifications
- Privilege escalation
- Unusual query patterns

Classify as: LOW, MEDIUM, HIGH, CRITICAL
{format_instructions}
"""
```

#### Network Security Template:
```python
NETWORK_SECURITY_TEMPLATE = """
Analyze the following network traffic:

{text}

Consider:
- Port scanning
- DDoS patterns
- Protocol anomalies
- Known malicious IPs
- Data exfiltration
- C&C communication

Classify as: LOW, MEDIUM, HIGH, CRITICAL
{format_instructions}
"""
```

### 2. Alert Configuration

Configure different alert channels based on your needs:

```python
alert_config = {
    "slack": {
        "webhook_url": "your-webhook-url"
    },
    "email": {
        "smtp_server": "smtp.company.com",
        "from_addr": "security@company.com",
        "to_addrs": ["team@company.com"],
        "username": "security@company.com",
        "password": "app-specific-password"
    },
    "webhook": {
        "url": "http://your-siem/api/incidents"
    }
}
```

### 3. Custom Monitoring Rules

You can add custom pattern matching for specific threats:

```python
attack_patterns = {
    "sql_injection": r"(?i)(union.*select|'.*=')",
    "xss": r"(?i)(<script>|javascript:)",
    "path_traversal": r"(?i)(\.\.\/|\.\.\\)",
    "shell_injection": r"(?i)(&.*\||;.*\|)",
    # Add your custom patterns
}
```

## Alert Configuration

### Slack Alerts

Slack alerts include:
- Threat level with appropriate emoji
- Detailed explanation
- Confidence score
- Recommended actions
- Original log entry

### Email Alerts

Email alerts provide:
- Severity in subject line
- Full threat analysis
- Raw log data
- Action recommendations
- Confidence metrics

### Webhook Integration

Webhook payloads include:
- Complete classification
- Raw log data
- Timestamp
- Unique incident ID
- System metadata

This guide provides practical examples and implementation details for the Threat Intelligence Classifier. For technical details about the system architecture and components, please refer to TECHNICAL.md.