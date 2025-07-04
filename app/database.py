from elasticsearch import AsyncElasticsearch
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Construct proper Elasticsearch URL
es_host = os.getenv('ELASTICSEARCH_HOST', 'localhost')
es_port = os.getenv('ELASTICSEARCH_PORT', '9200')
es_user = os.getenv('ELASTICSEARCH_USERNAME')
es_pass = os.getenv('ELASTICSEARCH_PASSWORD')

# Create Elasticsearch client with proper URL formatting
es = AsyncElasticsearch(
    [f"http://{es_host}:{es_port}"],
    http_auth=(es_user, es_pass) if es_user and es_pass else None
)

async def init_indices():
    """Initialize required Elasticsearch indices"""
    try:
        if not await es.indices.exists(index="threat_classifications"):
            mapping = {
                "mappings": {
                    "properties": {
                        "text": {"type": "text"},
                        "threat_level": {"type": "keyword"},
                        "explanation": {"type": "text"},
                        "confidence": {"type": "float"},
                        "timestamp": {"type": "date"}
                    }
                }
            }
            await es.indices.create(index="threat_classifications", body=mapping)
            return True
    except Exception as e:
        print(f"Error initializing indices: {str(e)}")
        return False

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
            body={
                "query": {"match_all": {}},
                "sort": [{"timestamp": "desc"}],
                "size": limit
            }
        )
        return [hit["_source"] for hit in result["hits"]["hits"]]
    except Exception as e:
        print(f"Error retrieving classifications: {str(e)}")
        return []