from setuptools import setup, find_packages

setup(
    name="physical-ai-book-backend",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn[standard]>=0.15.0",
        "python-dotenv>=0.19.0",
        "beautifulsoup4>=4.10.0",
        "playwright>=1.15.0",
        "cohere>=3.0.0",
        "qdrant-client>=1.0.0",
        "requests>=2.25.0",
        "pydantic>=1.8.0",
        "asyncio",
        "python-multipart",
    ],
    author="AI Development Team",
    author_email="dev@example.com",
    description="RAG Chatbot Backend for Physical AI Book",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/physical-ai-book",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.14",
    entry_points={
        "console_scripts": [
            "physical-ai-book-backend=backend.main:main",
        ],
    },
)