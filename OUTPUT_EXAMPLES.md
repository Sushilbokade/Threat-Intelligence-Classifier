# Threat Intelligence Classifier: Output Examples

This document provides real-world examples of different security logs and how the Threat Intelligence Classifier analyzes and classifies them. Each example includes the input log, the system's analysis, and explanation of why it was classified that way.

## 1. Authentication Attempts

### Example 1: Failed Login Attempts

**Input Log:**
```
Jul 5 10:15:23 server sshd[12345]: Failed password for root from 192.168.1.100 port 43210 ssh2
Jul 5 10:15:25 server sshd[12345]: Failed password for root from 192.168.1.100 port 43210 ssh2
Jul 5 10:15:27 server sshd[12345]: Failed password for root from 192.168.1.100 port 43210 ssh2
```

**System Output:**
```json
{
    "threat_level": "HIGH",
    "explanation": "Multiple failed login attempts for root user detected from the same IP address within a short time period. This pattern suggests a potential brute force attack attempting to gain unauthorized root access.",
    "confidence": 0.95,
    "recommended_action": "Investigate immediately. Consider blocking the IP address and reviewing SSH security settings.",
    "timestamp": "2025-07-05T10:15:27Z"
}
```

### Example 2: Successful Login from Known IP

**Input Log:**
```
Jul 5 09:00:01 server sshd[12346]: Accepted password for user john from 10.0.0.50 port 49123 ssh2
```

**System Output:**
```json
{
    "threat_level": "LOW",
    "explanation": "Successful authentication from an internal IP address (10.0.0.x range) using a regular user account. This appears to be normal business operation.",
    "confidence": 0.92,
    "recommended_action": "No immediate action required. Part of regular monitoring.",
    "timestamp": "2025-07-05T09:00:01Z"
}
```

## 2. Web Application Security

### Example 1: SQL Injection Attempt

**Input Log:**
```
Jul 5 11:23:45 webapp-01 nginx: 192.168.1.50 - - [05/Jul/2025:11:23:45 +0000] "GET /users?id=1' OR '1'='1 HTTP/1.1" 403 287 "-" "Mozilla/5.0"
```

**System Output:**
```json
{
    "threat_level": "CRITICAL",
    "explanation": "Detected SQL injection attempt in URL parameters. The request contains classic SQL injection pattern ('1'='1') targeting the users endpoint.",
    "confidence": 0.98,
    "recommended_action": "Immediate investigation required. Block source IP and review application logs for any successful injections.",
    "timestamp": "2025-07-05T11:23:45Z"
}
```

### Example 2: File Upload Attempt

**Input Log:**
```
Jul 5 14:12:33 webapp-01 nginx: 10.0.0.15 - - [05/Jul/2025:14:12:33 +0000] "POST /upload HTTP/1.1" 200 157 "-" "Mozilla/5.0" filename="document.pdf"
```

**System Output:**
```json
{
    "threat_level": "LOW",
    "explanation": "File upload from internal network with allowed file type (PDF). Request follows expected pattern for legitimate file uploads.",
    "confidence": 0.89,
    "recommended_action": "Standard monitoring. Verify file scanning system is operational.",
    "timestamp": "2025-07-05T14:12:33Z"
}
```

## 3. Network Security

### Example 1: Port Scanning Detection

**Input Log:**
```
Jul 5 03:15:00 firewall kernel: [TCP] Scan from 45.123.45.67: 80,443,22,21,3306,5432 in last 60 seconds
```

**System Output:**
```json
{
    "threat_level": "HIGH",
    "explanation": "Detected systematic port scanning activity from external IP. Multiple common service ports (HTTP, SSH, FTP, databases) were probed in rapid succession.",
    "confidence": 0.97,
    "recommended_action": "Block IP immediately. Review firewall rules and investigate if any ports were successfully accessed.",
    "timestamp": "2025-07-05T03:15:00Z"
}
```

### Example 2: Unusual Data Transfer

**Input Log:**
```
Jul 5 02:45:12 firewall kernel: [NetFlow] Large outbound transfer: src=192.168.1.25 dst=203.0.113.100 bytes=1500000000
```

**System Output:**
```json
{
    "threat_level": "MEDIUM",
    "explanation": "Large data transfer (1.5GB) detected to external IP during non-business hours. While this could be legitimate backup activity, the timing and destination warrant investigation.",
    "confidence": 0.85,
    "recommended_action": "Review within next 4 hours. Check if the destination IP is an approved service and verify the source machine's regular patterns.",
    "timestamp": "2025-07-05T02:45:12Z"
}
```

## 4. System Changes

### Example 1: Privilege Escalation

**Input Log:**
```
Jul 5 15:30:45 server sudo: user bob : TTY=pts/0 ; PWD=/home/bob ; USER=root ; COMMAND=/bin/bash
```

**System Output:**
```json
{
    "threat_level": "MEDIUM",
    "explanation": "User 'bob' escalated to root privileges. While sudo usage is normal, monitoring of root activities is important for security.",
    "confidence": 0.88,
    "recommended_action": "Verify if user 'bob' has appropriate sudo permissions. Review commands executed during root session.",
    "timestamp": "2025-07-05T15:30:45Z"
}
```

### Example 2: Critical File Modification

**Input Log:**
```
Jul 5 16:20:33 server audit[12347]: path="/etc/passwd" pid=12347 uid=0 old_ver=5.6 new_ver=5.7
```

**System Output:**
```json
{
    "threat_level": "CRITICAL",
    "explanation": "Modification detected to critical system file (/etc/passwd). Changes to this file could indicate attempt to create unauthorized users or modify system access.",
    "confidence": 0.99,
    "recommended_action": "Immediate investigation required. Compare file changes and verify all modifications are authorized.",
    "timestamp": "2025-07-05T16:20:33Z"
}
```

## 5. Malware Detection

### Example 1: Suspicious Process

**Input Log:**
```
Jul 5 22:10:15 server kernel: Suspicious process 'cryptominer.exe' accessing multiple CPU cores, high memory usage
```

**System Output:**
```json
{
    "threat_level": "CRITICAL",
    "explanation": "Detected process with name suggesting cryptocurrency mining activity. High resource usage pattern matches known cryptojacking behavior.",
    "confidence": 0.96,
    "recommended_action": "Immediate containment required. Terminate process, isolate machine, and initiate malware scan.",
    "timestamp": "2025-07-05T22:10:15Z"
}
```

### Example 2: Command & Control Traffic

**Input Log:**
```
Jul 5 20:45:33 firewall snort[12348]: [1:2024897:2] ET TROJAN Observed DNS Query to Known C2 Domain
```

**System Output:**
```json
{
    "threat_level": "CRITICAL",
    "explanation": "Network traffic attempting to contact known malware command & control server through DNS query. This indicates active malware infection attempting to communicate with control infrastructure.",
    "confidence": 0.99,
    "recommended_action": "Immediate isolation of affected system. Block DNS query, initiate incident response procedures.",
    "timestamp": "2025-07-05T20:45:33Z"
}
```

## 6. Compliance and Audit Events

### Example 1: PCI DSS Compliance Event

**Input Log:**
```
Jul 5 13:45:22 payment-server audit: User 'processor' accessed card data file /var/data/transactions.db, read operation, encryption=YES
```

**System Output:**
```json
{
    "threat_level": "MEDIUM",
    "explanation": "Access to payment card data detected. While the user has appropriate permissions and encryption is enabled, PCI DSS requires monitoring of all access to cardholder data.",
    "confidence": 0.92,
    "recommended_action": "Log for compliance audit. Verify user 'processor' is still authorized for card data access.",
    "timestamp": "2025-07-05T13:45:22Z",
    "compliance_flags": {
        "pci_dss": ["10.2.1", "10.2.7"],
        "requires_audit": true,
        "data_sensitivity": "HIGH"
    }
}
```

### Example 2: HIPAA Compliance Alert

**Input Log:**
```
Jul 5 09:15:33 medical-records-db audit: Bulk export of patient records (count: 1000+) by user 'researcher' to external drive
```

**System Output:**
```json
{
    "threat_level": "HIGH",
    "explanation": "Large-scale PHI data export detected. While user has researcher privileges, the volume and destination (external drive) require immediate review for HIPAA compliance.",
    "confidence": 0.95,
    "recommended_action": "Immediate review required. Verify IRB approval and data export authorization. Ensure DLP policies are enforced.",
    "timestamp": "2025-07-05T09:15:33Z",
    "compliance_flags": {
        "hipaa": ["164.308(a)(1)", "164.312(b)"],
        "requires_audit": true,
        "breach_notification_required": "ASSESS",
        "data_sensitivity": "CRITICAL"
    }
}
```

## 7. Tool Integration Examples

### Example 1: Integration with Wazuh

**Input Log (Wazuh Alert):**
```json
{
    "rule": {
        "level": 12,
        "description": "Multiple authentication failures followed by successful access",
        "id": "5710"
    },
    "agent": {
        "name": "windows-server-01",
        "id": "001"
    },
    "data": {
        "win": {
            "eventdata": {
                "targetUserName": "administrator",
                "ipAddress": "192.168.1.155",
                "logonType": "3"
            }
        }
    }
}
```

**System Output:**
```json
{
    "threat_level": "HIGH",
    "explanation": "Pattern suggests successful brute force attack. Multiple failed logins followed by successful remote logon (type 3) to administrator account.",
    "confidence": 0.97,
    "recommended_action": "Immediate investigation required. Lock account, review source IP, check for data exfiltration.",
    "timestamp": "2025-07-05T15:22:33Z",
    "wazuh_enrichment": {
        "related_rules": ["5710", "5711", "5712"],
        "agent_score": "HIGH_RISK",
        "mitre_tactics": ["TA0001", "TA0003"],
        "mitre_techniques": ["T1110", "T1078"]
    }
}
```

### Example 2: Integration with Elasticsearch SIEM

**Input (Elasticsearch Alert):**
```json
{
    "@timestamp": "2025-07-05T16:30:45Z",
    "event": {
        "category": "network",
        "type": "connection",
        "severity": 2
    },
    "source": {
        "ip": "192.168.1.100",
        "port": 45123
    },
    "destination": {
        "ip": "203.0.113.45",
        "port": 445
    },
    "network": {
        "protocol": "smb",
        "bytes": 1548576
    }
}
```

**System Output:**
```json
{
    "threat_level": "CRITICAL",
    "explanation": "Large data transfer detected over SMB protocol to external IP. This matches patterns of data exfiltration, particularly concerning given the use of SMB protocol to an external destination.",
    "confidence": 0.98,
    "recommended_action": "Immediate blocking required. Isolate source system, terminate SMB connection, initiate incident response.",
    "timestamp": "2025-07-05T16:30:45Z",
    "elastic_enrichment": {
        "risk_score": 95,
        "rule_categories": ["exfiltration", "lateral_movement"],
        "indicator_match": {
            "ip_reputation": "malicious",
            "known_threat_feeds": ["emerging_threats", "abuse_ch"]
        },
        "related_alerts": ["SMB-001", "DATA-EX-002"]
    }
}
```

## 8. Custom Integration Outputs

### Example 1: ServiceNow Incident Creation

**System Output:**
```json
{
    "threat_level": "HIGH",
    "explanation": "Multiple failed login attempts detected from external IP",
    "confidence": 0.94,
    "servicenow_incident": {
        "number": "INC0010234",
        "category": "security",
        "urgency": "high",
        "impact": "high",
        "priority": 1,
        "assignment_group": "Security Team",
        "short_description": "Potential Brute Force Attack Detected",
        "description": "Multiple failed login attempts from IP 192.168.1.100 targeting root account",
        "cmdb_ci": "Linux-Prod-01",
        "work_notes": "Automated response: IP blocked, account locked for review"
    }
}
```

### Example 2: Jira Security Issue Creation

**System Output:**
```json
{
    "threat_level": "CRITICAL",
    "explanation": "SQL injection attempt detected in production web application",
    "confidence": 0.96,
    "jira_issue": {
        "key": "SEC-1234",
        "project": "Security",
        "issue_type": "Security Incident",
        "priority": "Highest",
        "labels": ["sql-injection", "production", "immediate-response"],
        "components": ["Web Application", "Database"],
        "assignee": "security-team",
        "description": "SQL injection attempt detected:\n- Source IP: 192.168.1.50\n- Target: /users endpoint\n- Pattern: '1'='1\n\nAutomatic actions taken:\n1. IP blocked\n2. WAF rules updated\n3. Database queries logged",
        "custom_fields": {
            "security_severity": "Critical",
            "affected_systems": ["web-prod-01", "db-prod-01"],
            "compliance_impact": ["PCI-DSS", "SOC2"]
        }
    }
}
```

## 9. Automated Response Examples

### Example 1: Firewall Rule Update

**Input Log:**
```
Jul 5 17:45:22 firewall kernel: Multiple connection attempts from 192.168.1.200 to restricted ports (3389,22,3306)
```

**System Output:**
```json
{
    "threat_level": "HIGH",
    "explanation": "Pattern indicates port scanning behavior targeting critical services (RDP, SSH, MySQL)",
    "confidence": 0.93,
    "automated_response": {
        "action": "block_ip",
        "target": "192.168.1.200",
        "firewall_rules": [
            {
                "rule_id": "AUTO-BLOCK-1234",
                "action": "DROP",
                "source_ip": "192.168.1.200",
                "direction": "IN",
                "duration": "24h",
                "reason": "Automated block - Port scanning detected"
            }
        ],
        "notifications_sent": [
            {
                "channel": "slack",
                "status": "delivered",
                "timestamp": "2025-07-05T17:45:23Z"
            },
            {
                "channel": "email",
                "recipient": "security-team@company.com",
                "status": "delivered",
                "timestamp": "2025-07-05T17:45:24Z"
            }
        ]
    }
}
```

### Example 2: Account Lockdown

**Input Log:**
```
Jul 5 18:10:15 auth-server audit: User 'admin' accessed sensitive data from unusual IP 203.0.113.100
```

**System Output:**
```json
{
    "threat_level": "CRITICAL",
    "explanation": "Admin account accessed sensitive data from unrecognized IP outside normal business hours",
    "confidence": 0.97,
    "automated_response": {
        "action": "account_lockdown",
        "target_user": "admin",
        "actions_taken": [
            {
                "action": "disable_account",
                "status": "success",
                "timestamp": "2025-07-05T18:10:16Z"
            },
            {
                "action": "revoke_sessions",
                "status": "success",
                "count": 3,
                "timestamp": "2025-07-05T18:10:17Z"
            },
            {
                "action": "enable_2fa",
                "status": "pending",
                "requires_approval": true
            }
        ],
        "incident_details": {
            "incident_id": "SEC-20250705-001",
            "severity": "CRITICAL",
            "handler": "AutoResponse-v2.1",
            "recovery_process": "Requires security team approval and identity verification"
        }
    }
}
```

# Threat Intelligence Classifier Output Examples

## Example Classifications

### High Threat Example
```json
{
    "text": "Failed root login attempt from unknown IP 185.234.123.45 with multiple password attempts",
    "threat_level": "HIGH",
    "explanation": "Unauthorized root access attempt detected with multiple failed password attempts from an unknown IP address",
    "confidence": 0.9,
    "timestamp": "2025-07-05T10:00:00Z"
}
```

### Critical Threat Example
```json
{
    "text": "Detected malware signature in system32, multiple encrypted connections to known C&C servers",
    "threat_level": "CRITICAL",
    "explanation": "Malware detected with Command & Control (C&C) communication - indicating active malware infection",
    "confidence": 0.95,
    "timestamp": "2025-07-05T10:01:00Z"
}
```

### Medium Threat Example
```json
{
    "text": "Unusual file access pattern detected: user accessing multiple sensitive files in quick succession",
    "threat_level": "MEDIUM",
    "explanation": "Unusual pattern of rapid sensitive file access may indicate data exfiltration attempt",
    "confidence": 0.7,
    "timestamp": "2025-07-05T10:02:00Z"
}
```

### Low Threat Example
```json
{
    "text": "User logged in successfully from internal IP 192.168.1.100",
    "threat_level": "LOW",
    "explanation": "Normal user login activity from internal network",
    "confidence": 0.8,
    "timestamp": "2025-07-05T10:03:00Z"
}
```

## Customization Guide

### 1. Security Focus Configuration

The system supports different security focuses that can be configured when initializing the classifier:

```python
# General security focus (default)
classifier = ThreatClassifier()

# Web application security focus
classifier = ThreatClassifier(security_focus="web")
```

### 2. Customizing Analysis Factors

You can modify the threat analysis factors in `app/threat_classifier.py`:

#### General Security Focus
- Unauthorized access attempts
- Suspicious IP addresses/domains
- Malware indicators
- Data exfiltration attempts
- Protocol anomalies
- Known attack patterns
- System modification attempts
- Privilege escalation indicators

#### Web Security Focus
- SQL Injection attempts
- Cross-Site Scripting (XSS)
- Cross-Site Request Forgery (CSRF)
- File upload attempts
- Authentication bypass attempts
- Path traversal
- API abuse patterns
- Session manipulation
- Known web vulnerabilities
- Unauthorized endpoint access

### 3. Environment Configuration

Create a `.env` file with your specific settings:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4  # or gpt-3.5-turbo

# Elasticsearch Configuration
ELASTICSEARCH_HOST=your_es_host
ELASTICSEARCH_PORT=9200
ELASTICSEARCH_USERNAME=elastic
ELASTICSEARCH_PASSWORD=your_password

# Application Configuration
LOG_LEVEL=INFO
BATCH_SIZE=10
CACHE_TTL=3600
MAX_RETRIES=3
```

### 4. Custom Classification Rules

You can extend the classification logic by modifying the prompt templates in `threat_classifier.py`:

1. Create a new template for your specific needs:
```python
CUSTOM_TEMPLATE = """
Analyze the following data for {specific_focus} security threats:

{text}

Classify the threat level as one of: LOW, MEDIUM, HIGH, CRITICAL
Consider these domain-specific factors:
- Factor 1
- Factor 2
- Factor 3
{format_instructions}
"""
```

2. Add your template to the classifier:
```python
class ThreatClassifier:
    def __init__(self, security_focus="general"):
        templates = {
            "general": THREAT_CLASSIFICATION_TEMPLATE,
            "web": WEB_SECURITY_TEMPLATE,
            "custom": CUSTOM_TEMPLATE
        }
        self.prompt = PromptTemplate(
            template=templates.get(security_focus, THREAT_CLASSIFICATION_TEMPLATE),
            input_variables=["text"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )
```

## Setup Steps

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key
   - Configure Elasticsearch connection

4. Start Elasticsearch:
```bash
# Using Docker
docker-compose up elasticsearch
```

5. Initialize the application:
```bash
uvicorn app.main:app --reload
```

6. Verify setup with test cases:
```bash
pytest tests/
```

## Testing and Validation

The system includes comprehensive test cases in `tests/test_threat_classifier.py` and `tests/test_api_integration.py`:

1. Classification accuracy tests
2. API endpoint validation
3. Error handling verification
4. Edge case testing

Example test output:
```
============================= test session starts ==============================
collecting ... collected 8 items

tests/test_api_integration.py ....                                     [ 50%]
tests/test_threat_classifier.py ....                                   [100%]

============================== 8 passed in 2.34s ==============================
```

## Common Usage Patterns

1. Real-time log analysis:
```python
import requests

def analyze_log(log_entry):
    response = requests.post(
        "http://localhost:8000/classify",
        json={"text": log_entry}
    )
    return response.json()

# Example usage
result = analyze_log("Failed root login attempt from unknown IP")
print(f"Threat Level: {result['threat_level']}")
print(f"Explanation: {result['explanation']}")
```

2. Batch processing:
```python
async def process_logs(logs):
    results = []
    async with aiohttp.ClientSession() as session:
        for log in logs:
            async with session.post(
                "http://localhost:8000/classify",
                json={"text": log}
            ) as response:
                results.append(await response.json())
    return results
```

3. Historical analysis:
```python
def get_threat_history():
    response = requests.get("http://localhost:8000/history")
    return response.json()
```