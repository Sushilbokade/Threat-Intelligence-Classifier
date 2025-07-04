#!/usr/bin/env python3
import os
import sys
import subprocess
import requests
import time
from typing import Dict, List
import pytest
from dotenv import load_dotenv

def load_environment(cloud_provider: str) -> Dict[str, str]:
    """Load environment variables based on cloud provider"""
    if cloud_provider.lower() == 'gcp':
        load_dotenv('deployment/gcp/.env.gcp')
    elif cloud_provider.lower() == 'azure':
        load_dotenv('deployment/azure/.env.azure')
    else:
        raise ValueError("Cloud provider must be either 'gcp' or 'azure'")

def check_prerequisites() -> List[str]:
    """Check if all required tools and configurations are present"""
    missing = []
    
    # Check Python packages
    required_packages = [
        'fastapi', 'uvicorn', 'langchain', 'elasticsearch',
        'python-dotenv', 'pytest', 'requests'
    ]
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(f"Python package: {package}")
    
    # Check environment variables
    required_env_vars = [
        'OPENAI_API_KEY',
        'ELASTICSEARCH_HOST',
        'ELASTICSEARCH_PASSWORD'
    ]
    
    for var in required_env_vars:
        if not os.getenv(var):
            missing.append(f"Environment variable: {var}")
    
    return missing

def run_tests() -> bool:
    """Run the test suite"""
    result = pytest.main([
        'tests/',
        '-v',
        '--junit-xml=test-results.xml',
        '--cov=app',
        '--cov-report=html'
    ])
    return result == 0

def test_api_endpoints(base_url: str = "http://localhost:8000") -> bool:
    """Test API endpoints"""
    try:
        # Test classification endpoint
        test_data = {
            "text": "Test log entry for deployment validation"
        }
        response = requests.post(f"{base_url}/classify", json=test_data)
        assert response.status_code == 200
        result = response.json()
        assert "threat_level" in result
        assert "explanation" in result
        assert "confidence" in result
        
        # Test history endpoint
        response = requests.get(f"{base_url}/history")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        
        return True
    except Exception as e:
        print(f"API test failed: {str(e)}")
        return False

def main():
    if len(sys.argv) != 2 or sys.argv[1].lower() not in ['gcp', 'azure']:
        print("Usage: python test-deployment.py <gcp|azure>")
        sys.exit(1)
    
    cloud_provider = sys.argv[1].lower()
    print(f"Testing deployment for {cloud_provider.upper()}...")
    
    # Load environment
    try:
        load_environment(cloud_provider)
    except Exception as e:
        print(f"Failed to load environment: {str(e)}")
        sys.exit(1)
    
    # Check prerequisites
    print("Checking prerequisites...")
    missing = check_prerequisites()
    if missing:
        print("Missing requirements:")
        for item in missing:
            print(f"  - {item}")
        sys.exit(1)
    
    # Run tests
    print("Running test suite...")
    if not run_tests():
        print("Test suite failed")
        sys.exit(1)
    
    # Start the application
    print("Starting application for endpoint testing...")
    app_process = subprocess.Popen(
        ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for app to start
    time.sleep(5)
    
    # Test endpoints
    print("Testing API endpoints...")
    if not test_api_endpoints():
        print("API endpoint tests failed")
        app_process.terminate()
        sys.exit(1)
    
    # Clean up
    app_process.terminate()
    print(f"Deployment testing for {cloud_provider.upper()} completed successfully!")

if __name__ == "__main__":
    main()