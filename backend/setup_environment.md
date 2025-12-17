# Environment Setup Guide for RAG Chatbot Backend

This guide will help you set up your Python environment to run the RAG chatbot backend successfully, resolving all import errors and dependency issues.

## Prerequisites

- Python 3.14 or higher
- pip package manager
- Windows OS (instructions tailored for Windows)

## Step-by-Step Setup

### 1. Create Virtual Environment

First, navigate to the project root directory and create a virtual environment:

```bash
cd C:\Users\Administrator\Desktop\Book1
python -m venv venv
```

Activate the virtual environment:

```bash
# On Windows
venv\Scripts\activate
```

### 2. Upgrade pip

Ensure you have the latest pip version:

```bash
python -m pip install --upgrade pip
```

### 3. Install Core Dependencies

Install the core packages needed for the FastAPI application:

```bash
pip install fastapi uvicorn python-multipart
```

### 4. Install Missing Dependencies

Install all the packages that were causing import errors:

```bash
pip install python-dotenv
pip install beautifulsoup4
pip install playwright
pip install cohere
pip install qdrant-client
pip install requests
pip install pydantic
```

For playwright, you'll need to install the browsers as well:

```bash
playwright install
```

### 5. Configure PYTHONPATH for Windows

To resolve the module import issues, you need to make the project root available to Python. You can do this in several ways:

#### Option A: Temporary (for current session)
Run this command in your activated virtual environment before running the application:

```bash
# On Windows Command Prompt
set PYTHONPATH=%PYTHONPATH%;C:\Users\Administrator\Desktop\Book1

# On Windows PowerShell
$env:PYTHONPATH += ";C:\Users\Administrator\Desktop\Book1"
```

#### Option B: Permanent (recommended)
Add the project root directory to your system's PYTHONPATH environment variable:

1. Open System Properties → Advanced → Environment Variables
2. Under "System Variables" (or "User Variables"), find and select "PYTHONPATH"
3. If it doesn't exist, create a new environment variable named "PYTHONPATH"
4. Add the path: `C:\Users\Administrator\Desktop\Book1`
5. If PYTHONPATH already exists, append the path using a semicolon separator

### 6. Alternative: Install Package in Development Mode

Instead of configuring PYTHONPATH, you can install the project as an editable package:

```bash
# From the project root directory (Book1/)
pip install -e .
```

You'll need to create a `setup.py` or `pyproject.toml` file for this to work. Here's a minimal `setup.py`:

```python
from setuptools import setup, find_packages

setup(
    name="physical-ai-book-backend",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "python-dotenv",
        "beautifulsoup4",
        "playwright",
        "cohere",
        "qdrant-client",
        "requests",
        "pydantic",
    ],
)
```

### 7. Run the Application

Once everything is set up, you should be able to run the application:

```bash
# From the project root directory
uvicorn backend.main:app --reload
```

### 8. Verify Everything Works

Navigate to `http://127.0.0.1:8000/docs` in your browser to verify that the FastAPI documentation is accessible.

## Troubleshooting

### If you still get ModuleNotFoundError

1. Verify that your virtual environment is activated
2. Check that the PYTHONPATH includes your project root directory
3. Verify that all packages are installed:
   ```bash
   pip list
   ```

### If Cohere import warnings persist

The warnings with Python 3.14 may be due to version compatibility. Try installing the latest version:

```bash
pip install --upgrade cohere
```

### If the server won't start

1. Check that all dependencies are installed
2. Verify the main.py file exists in the backend directory
3. Check that the app variable exists in main.py and is accessible

## Requirements File (Optional)

For easier dependency management, create a `requirements.txt` file in the project root:

```txt
fastapi>=0.68.0
uvicorn[standard]>=0.15.0
python-dotenv>=0.19.0
beautifulsoup4>=4.10.0
playwright>=1.15.0
cohere>=3.0.0
qdrant-client>=1.0.0
requests>=2.25.0
pydantic>=1.8.0
```

Then install all dependencies at once:

```bash
pip install -r requirements.txt
```

## Next Steps

Once the environment is set up and the application runs without errors, you can:

1. Begin developing new features
2. Run tests to verify functionality
3. Connect to your Qdrant instance
4. Test the RAG functionality