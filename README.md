# Threat Intelligence Classifier

An LLM-powered security threat classification system that analyzes log entries and text data for potential security threats. This system leverages GPT-4's advanced natural language processing capabilities to identify and classify potential security threats in real-time.

## Features

- **Real-time threat classification using GPT-4**
  - Intelligent analysis of log entries and security events
  - Context-aware threat detection
  - Detailed reasoning for each classification
  
- **Multi-level threat classification**
  - LOW: Normal operations or non-threatening events
  - MEDIUM: Potential security concerns requiring attention
  - HIGH: Serious security threats requiring immediate investigation
  - CRITICAL: Severe security incidents requiring immediate action
  
- **Comprehensive Analysis Factors**
  - Unauthorized access detection
  - Suspicious IP/domain reputation analysis
  - Malware indicator identification
  - Data exfiltration pattern detection
  - Protocol anomaly recognition
  - Known attack pattern matching
  - System modification monitoring
  - Privilege escalation detection

- **Advanced Integration Features**
  - RESTful API interface for easy integration
  - Elasticsearch-based persistent storage
  - Historical data tracking and analysis
  - Async operation support
  - Docker containerization support

## Prerequisites

- Python 3.8+
- Docker and Docker Compose (recommended for easy setup)
- OpenAI API key
- GCP or Azure account (for cloud deployment)

## Quick Start with Docker

The easiest way to get started is using Docker Compose:

1. Clone the repository:
   ```bash
   git clone https://github.com/Sushilbokade/Threat-Intelligence-Classifier.git
   cd Threat-Intelligence-Classifier
   ```

2. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

3. Start the application:
   ```bash
   docker compose up --build
   ```

The application will be available at http://localhost:8000, and Elasticsearch will be running at http://localhost:9200.

## Manual Setup

If you prefer to run the application without Docker:

1. Install Python 3.8+ and Elasticsearch 7.x

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables in `.env`:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ELASTICSEARCH_HOST=localhost
   ELASTICSEARCH_PORT=9200
   ELASTICSEARCH_USERNAME=elastic
   ELASTICSEARCH_PASSWORD=your_elasticsearch_password
   ```

5. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation

### POST /classify
Classify a log entry for security threats.

**Request:**
```json
{
    "text": "Your log entry or text to analyze"
}
```

**Response:**
```json
{
    "threat_level": "HIGH",
    "explanation": "Detailed analysis of the threat...",
    "confidence": 0.95
}
```

### GET /history
Retrieve recent threat classifications.

**Response:**
```json
[
    {
        "text": "Original log entry...",
        "threat_level": "HIGH",
        "explanation": "Threat analysis...",
        "confidence": 0.95,
        "timestamp": "2025-07-05T10:00:00Z"
    }
]
```

## Example Usage

### Using curl
```bash
curl -X POST "http://localhost:8000/classify" \
     -H "Content-Type: application/json" \
     -d '{"text": "Failed login attempt from IP 192.168.1.100: Invalid credentials (5th attempt)"}'
```

### Using Python
```python
import requests

response = requests.post(
    "http://localhost:8000/classify",
    json={"text": "Failed login attempt from IP 192.168.1.100: Invalid credentials (5th attempt)"}
)
result = response.json()
print(f"Threat Level: {result['threat_level']}")
print(f"Explanation: {result['explanation']}")
```

## Architecture

The system consists of several key components:

1. **API Layer** (`app/main.py`)
   - FastAPI-based RESTful API
   - Request/response handling
   - Input validation
   - Error handling

2. **Classification Engine** (`app/threat_classifier.py`)
   - LangChain integration
   - GPT-4 model configuration
   - Prompt engineering
   - Threat analysis logic

3. **Data Layer** (`app/database.py`)
   - Elasticsearch integration
   - Historical data management
   - Query operations

4. **Domain Models** (`app/models.py`)
   - Pydantic models
   - Data validation
   - Type safety

## Cloud Deployment

The project includes deployment configurations for both GCP and Azure. See `deployment/CLOUD_DEPLOYMENT.md` for detailed instructions.

## Development

### Project Structure
```
├── app/
│   ├── main.py           # FastAPI application
│   ├── models.py         # Data models
│   ├── database.py       # Database operations
│   └── threat_classifier.py  # Classification logic
├── tests/
│   ├── test_api_integration.py
│   └── test_threat_classifier.py
├── deployment/
│   ├── azure/
│   └── gcp/
└── docker-compose.yml
```

### Running Tests
```bash
pytest tests/
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Security Considerations

- API key security
- Rate limiting
- Input validation
- Error handling
- Data persistence security
- Network security

## Performance Optimization

- Elasticsearch indexing
- Caching strategies
- Async operations
- Connection pooling
- Batch processing support

## License

MIT License - See LICENSE file for details

## Acknowledgments

- OpenAI for GPT-4 API
- Elastic for Elasticsearch
- FastAPI team
- LangChain community

## Branch Structure

This project follows a structured branching strategy:

- `main` - Production-ready code
  - Contains stable, tested, and deployment-ready code
  - All code here has been thoroughly tested and reviewed
  - Direct commits are not allowed; changes come through merges

- `develop` - Main development branch
  - Contains latest delivered development changes for the next release
  - Where features are integrated and tested together
  - Source for nightly builds

- Feature Branches (`feature/*`)
  - Created for each new feature or enhancement
  - Branch from: `develop`
  - Merge back into: `develop`
  - Naming convention: `feature/feature-name`
  - Example: `feature/api-rate-limiting`

- Hotfix Branches (`hotfix/*`)
  - Created for urgent fixes to production code
  - Branch from: `main`
  - Merge back into: `main` and `develop`
  - Naming convention: `hotfix/issue-description`
  - Example: `hotfix/security-patch`

### Branch Workflow

1. Feature Development:
   ```
   git checkout develop
   git checkout -b feature/new-feature
   # Make changes
   git push -u origin feature/new-feature
   # Create PR to merge into develop
   ```

2. Hotfix Process:
   ```
   git checkout main
   git checkout -b hotfix/fix-description
   # Make urgent fixes
   git push -u origin hotfix/fix-description
   # Create PRs to merge into both main and develop
   ```

3. Release Process:
   ```
   git checkout develop
   # Ensure all tests pass
   git checkout main
   git merge develop
   git push origin main
   ```