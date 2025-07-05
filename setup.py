from setuptools import setup, find_packages

setup(
    name="threat-classifier",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "langchain-openai",
        "fastapi",
        "elasticsearch",
        "python-dotenv",
        "uvicorn",
        "pydantic",
        "requests",
        "python-jose",
        "python-multipart",
        "aiohttp",
    ],
    extras_require={
        "test": [
            "pytest",
            "pytest-asyncio",
            "nest-asyncio",
            "httpx"
        ]
    }
)