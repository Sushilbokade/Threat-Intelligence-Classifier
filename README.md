# Threat Intelligence Classifier

An LLM-powered security threat classification system that analyzes log entries and text data for potential security threats.

## Features

- Real-time threat classification using GPT-4
- Configurable threat levels (LOW, MEDIUM, HIGH, CRITICAL)
- Detailed explanations for each classification
- Historical classification storage and retrieval
- RESTful API interface
- Elasticsearch integration for persistent storage

## Prerequisites

- Python 3.8+
- Elasticsearch 7.x or higher
- OpenAI API key
- GCP or Azure account (for cloud deployment)

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables:
   Create a `.env` file with the following:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ELASTICSEARCH_HOST=localhost
   ELASTICSEARCH_PORT=9200
   ELASTICSEARCH_USERNAME=elastic
   ELASTICSEARCH_PASSWORD=your_elasticsearch_password
   ```

## Running the Application

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST /classify
Classify a log entry for security threats.

Request body:
```json
{
    "text": "Your log entry or text to analyze"
}
```

### GET /history
Retrieve recent threat classifications.

## Example Usage

```bash
curl -X POST "http://localhost:8000/classify" \
     -H "Content-Type: application/json" \
     -d '{"text": "Failed login attempt from IP 192.168.1.100: Invalid credentials (5th attempt)"}'
```

## Development

The project uses:
- FastAPI for the web framework
- LangChain for LLM integration
- Elasticsearch for data persistence
- Pydantic for data validation

## License

MIT License