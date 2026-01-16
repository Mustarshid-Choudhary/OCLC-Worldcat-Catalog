@echo off
REM ===============================================
REM Run Python script from CMD
REM ===============================================

REM Optional: Set project root (script directory)
set "APP_DIR=%~dp0"
set "ROOT_DIR=%APP_DIR%.."

REM Path to .venv
set "VENV_DIR=%ROOT_DIR%\.venv"

REM Activate the virtual environment
call "%VENV_DIR%\Scripts\activate.bat"

REM Optional: Set Python path if needed
REM set "PYTHON=C:\Path\To\Python39\python.exe"

REM Run the Python script
python "%APP_DIR%\src\runScript.py"