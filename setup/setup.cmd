@echo off
REM ===============================================
REM Setup Script for App
REM ===============================================

REM -----------------------------------------------
REM Determine directories
REM -----------------------------------------------
REM %~dp0 = directory of this script (always ends with \)
set "SCRIPT_DIR=%~dp0"

REM ROOT_DIR = two levels up from script location (where requirements.txt lives)
set "ROOT_DIR=%SCRIPT_DIR%\.."

REM APP_DIR = your app folder (relative to ROOT_DIR)
set "APP_DIR=%ROOT_DIR%\app"

REM VENV_DIR = .venv virtual environment
set "VENV_DIR=%ROOT_DIR%\.venv"

REM Ensure APP_DIR exists
if not exist "%APP_DIR%" mkdir "%APP_DIR%"


REM -----------------------------------------------
REM Create .venv if it doesn't exist
REM -----------------------------------------------
if not exist "%VENV_DIR%" (
    echo Creating virtual environment in %VENV_DIR% ...
    python -m venv "%VENV_DIR%"
) else (
    echo Virtual environment already exists.
)

REM -----------------------------------------------
REM Activate the venv
REM -----------------------------------------------
call "%VENV_DIR%\Scripts\activate.bat"

REM -----------------------------------------------
REM Install requirements into the venv
REM -----------------------------------------------
if not exist "%ROOT_DIR%\requirements.txt" (
    echo ERROR: requirements.txt not found in %ROOT_DIR%
    exit /b 1
)

echo Installing Python requirements into .venv ...
python -m pip install --upgrade pip
pip install -r "%ROOT_DIR%\requirements.txt"
echo:

REM Debug info (optional)
echo SCRIPT_DIR=%SCRIPT_DIR%
echo ROOT_DIR=%ROOT_DIR%
echo APP_DIR=%APP_DIR%
echo:

REM -----------------------------------------------
REM Create .env if it doesn't exist
REM -----------------------------------------------
setlocal EnableDelayedExpansion
if not exist "%APP_DIR%\.env" (
    echo .env file not found — please enter your WorldcatMetadataAPI credentials:

    set /p APIKey="API Key: "
    set /p APISecret="API Secret: "
    set /p APIScopes="API Scopes: "

    REM Write .env file line by line
    echo API_KEY=!APIKey!> "%APP_DIR%\.env"
    echo API_SECRET=!APISecret!>> "%APP_DIR%\.env"
    echo API_SCOPES=!APIScopes!>> "%APP_DIR%\.env"

    echo Writing API credentials to .env ...
    echo:
) else (
    echo .env file already exists — skipping
    echo:
)

endLocal
echo:

echo Now you can close this window and run main.cmd!
pause