#!/usr/bin/env python3
import asyncio
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import RequestError
import os
from dotenv import load_dotenv
import sys
import json

# Elasticsearch index mappings
THREAT_CLASSIFICATIONS_MAPPING = {
    "mappings": {
        "properties": {
            "text": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                }
            },
            "threat_level": {
                "type": "keyword"
            },
            "explanation": {
                "type": "text"
            },
            "confidence": {
                "type": "float"
            },
            "timestamp": {
                "type": "date"
            }
        }
    },
    "settings": {
        "number_of_shards": 3,
        "number_of_replicas": 2,
        "refresh_interval": "1s"
    }
}

async def init_elasticsearch(host: str, port: int, username: str, password: str):
    """Initialize Elasticsearch with proper mappings"""
    client = AsyncElasticsearch(
        hosts=[f"http://{host}:{port}"],
        http_auth=(username, password)
    )

    try:
        # Check if Elasticsearch is responsive
        if not await client.ping():
            print("Failed to connect to Elasticsearch")
            return False

        # Create index with mapping
        try:
            await client.indices.create(
                index="threat_classifications",
                body=THREAT_CLASSIFICATIONS_MAPPING
            )
            print("Created threat_classifications index with mapping")
        except RequestError as e:
            if "resource_already_exists_exception" in str(e):
                print("Index already exists, updating mapping...")
                await client.indices.put_mapping(
                    index="threat_classifications",
                    body=THREAT_CLASSIFICATIONS_MAPPING["mappings"]
                )
            else:
                raise

        # Create test document
        test_doc = {
            "text": "Test initialization log entry",
            "threat_level": "LOW",
            "explanation": "This is a test document",
            "confidence": 1.0,
            "timestamp": "2025-07-05T00:00:00Z"
        }

        await client.index(
            index="threat_classifications",
            document=test_doc,
            refresh=True
        )

        # Verify the document was created
        result = await client.search(
            index="threat_classifications",
            body={
                "query": {
                    "match": {
                        "text": "Test initialization"
                    }
                }
            }
        )

        if result["hits"]["total"]["value"] > 0:
            print("Successfully verified index creation and document insertion")
        else:
            print("Failed to verify document insertion")
            return False

        return True

    except Exception as e:
        print(f"Error initializing Elasticsearch: {str(e)}")
        return False
    finally:
        await client.close()

async def create_index_template():
    """Create index template for future indices"""
    client = AsyncElasticsearch(
        hosts=[f"http://{os.getenv('ELASTICSEARCH_HOST')}:{os.getenv('ELASTICSEARCH_PORT')}"],
        http_auth=(os.getenv('ELASTICSEARCH_USERNAME'), os.getenv('ELASTICSEARCH_PASSWORD'))
    )

    template = {
        "index_patterns": ["threat_classifications-*"],
        "template": THREAT_CLASSIFICATIONS_MAPPING,
        "priority": 1
    }

    try:
        await client.indices.put_index_template(
            name="threat_classifications_template",
            body=template
        )
        print("Successfully created index template")
        return True
    except Exception as e:
        print(f"Error creating index template: {str(e)}")
        return False
    finally:
        await client.close()

def load_cloud_config(provider: str):
    """Load cloud-specific configuration"""
    if provider.lower() == 'gcp':
        env_file = 'deployment/gcp/.env.gcp'
    elif provider.lower() == 'azure':
        env_file = 'deployment/azure/.env.azure'
    else:
        raise ValueError("Provider must be either 'gcp' or 'azure'")
    
    load_dotenv(env_file)

async def main():
    if len(sys.argv) != 2 or sys.argv[1].lower() not in ['gcp', 'azure', 'local']:
        print("Usage: python init_database.py <gcp|azure|local>")
        sys.exit(1)

    provider = sys.argv[1].lower()
    if provider != 'local':
        load_cloud_config(provider)
    else:
        load_dotenv()

    host = os.getenv('ELASTICSEARCH_HOST')
    port = int(os.getenv('ELASTICSEARCH_PORT', 9200))
    username = os.getenv('ELASTICSEARCH_USERNAME')
    password = os.getenv('ELASTICSEARCH_PASSWORD')

    if not all([host, port, username, password]):
        print("Missing required environment variables")
        sys.exit(1)

    print(f"Initializing Elasticsearch for {provider.upper()}...")
    success = await init_elasticsearch(host, port, username, password)
    if success:
        print("Elasticsearch initialization completed successfully")
        if await create_index_template():
            print("Index template created successfully")
    else:
        print("Elasticsearch initialization failed")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())