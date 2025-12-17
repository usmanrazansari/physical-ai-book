# Running the Physical AI Book Backend

This guide provides the correct commands to run the backend application in different modes.

## Prerequisites

- Python 3.11.7 installed
- The project already has a working virtual environment at `backend/.venv/`

## Understanding the Virtual Environment

The virtual environment is already created at `backend/.venv/`. You don't need to recreate it unless specifically needed.

## Running the Backend

### Option 1: Direct Execution (Recommended)
Use this method to run commands without activating the virtual environment:

```bash
# Run the ASGI server (FastAPI)
backend\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

# Run the CLI application
backend\.venv\Scripts\python.exe backend/main.py --mode full

# Run the CLI with different modes
backend\.venv\Scripts\python.exe backend/main.py --mode crawl
backend\.venv\Scripts\python.exe backend/main.py --mode process
backend\.venv\Scripts\python.exe backend/main.py --mode embed
backend\.venv\Scripts\python.exe backend/main.py --mode store
```

### Option 2: Activate Virtual Environment
Use this method if you plan to run multiple commands:

```bash
# On Windows Command Prompt
backend\.venv\Scripts\activate.bat

# On Windows PowerShell
backend\.venv\Scripts\Activate.ps1

# After activation, you can run commands directly:
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
python backend/main.py --mode full
```

## Troubleshooting Common Issues

### Issue: Permission Denied Error
If you encounter permission errors, make sure you're running from the project root directory:
```bash
cd C:\Users\Administrator\Desktop\Book1
backend\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

### Issue: Module Not Found
If you get import errors, make sure you're using the virtual environment's Python:
```bash
# Always use the virtual environment's Python
backend\.venv\Scripts\python.exe -c "from backend.main import app; print('Import successful')"
```

### Issue: Port Already in Use
If you get a port binding error, use a different port:
```bash
backend\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8001
```

## Checking Application Status

Once the server is running, you can check these endpoints:

- `http://127.0.0.1:8000/status` - Basic status check
- `http://127.0.0.1:8000/health` - Health check
- `http://127.0.0.1:8000/config` - Configuration check
- `http://127.0.0.1:8000/docs` - Interactive API documentation (Swagger UI)

## Environment Variables

Make sure your `.env` file in the project root contains the required variables:
```
QDRANT_API_KEY=your_key_here
QDRANT_URL=your_url_here
COHERE_API_KEY=your_key_here
```

## Verifying Everything Works

Run these commands to verify the backend is properly configured:

```bash
# Test import
backend\.venv\Scripts\python.exe -c "from backend.main import app, main; print('All imports successful')"

# Test CLI help
backend\.venv\Scripts\python.exe backend/main.py --help

# Test server startup (will start and then you can stop with Ctrl+C)
backend\.venv\Scripts\python.exe -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```