@echo off
REM Setup script for Physical AI Book Backend on Windows

REM Create virtual environment
python -m venv .venv

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Upgrade pip
python -m pip install --upgrade pip

REM Install dependencies
pip install -r requirements.txt

REM Install playwright and its dependencies
playwright install

echo Setup complete! To activate the environment, run: .venv\Scripts\activate.bat
echo Then run: uvicorn backend.main:app --reload