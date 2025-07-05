from elasticsearch import AsyncElasticsearch, NotFoundError
from datetime import datetime
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

def get_elasticsearch_config():
    """Get Elasticsearch configuration from environment variables"""
    host = os.getenv("ELASTICSEARCH_HOST", "http://localhost:9200")
    parsed = urlparse(host)
    
    # Ensure the URL has all required components
    if not parsed.scheme or not parsed.hostname:
        # Default to http://localhost:9200 if not properly configured
        return "http://localhost:9200"
    
    # Add port if not specified
    if not parsed.port:
        host = f"{parsed.scheme}://{parsed.hostname}:9200"
    
    return host

# Initialize Elasticsearch client with basic_auth instead of http_auth
es = AsyncElasticsearch(
    hosts=[get_elasticsearch_config()],
    basic_auth=(
        os.getenv("ELASTICSEARCH_USER", "elastic"),
        os.getenv("ELASTICSEARCH_PASSWORD", "changeme")
    )
)

async def init_indices():
    """Initialize required Elasticsearch indices"""
    try:
        # Create the threat classifications index if it doesn't exist
        await es.indices.create(
            index="threat_classifications",
            mappings={
                "properties": {
                    "text": {"type": "text"},
                    "threat_level": {"type": "keyword"},
                    "explanation": {"type": "text"},
                    "confidence": {"type": "float"},
                    "timestamp": {"type": "date"}
                }
            },
            ignore=400  # Ignore 400 error (index already exists)
        )
    except Exception as e:
        print(f"Error initializing indices: {str(e)}")

async def store_classification(text: str, classification: dict):
    """Store a threat classification result"""
    doc = {
        **classification,
        "text": text,
        "timestamp": datetime.utcnow().isoformat()
    }
    try:
        await es.index(index="threat_classifications", document=doc)
        return True
    except Exception as e:
        print(f"Error storing classification: {str(e)}")
        return False

async def get_recent_classifications(limit: int = 100):
    """Retrieve recent classifications"""
    try:
        result = await es.search(
            index="threat_classifications",
            sort=[{"timestamp": "desc"}],
            size=limit
        )
        return [hit["_source"] for hit in result["hits"]["hits"]]
    except NotFoundError:
        return []
    except Exception as e:
        print(f"Error retrieving classifications: {str(e)}")
        return []