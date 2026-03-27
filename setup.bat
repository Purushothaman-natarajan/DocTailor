@echo off
title DocTailor Setup & Launcher
color 0A
echo =========================================
echo    DocTailor - Document Customization Toolkit
echo =========================================
echo.

REM --- Check for winget (Windows Package Manager) ---
where winget >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARN] winget not found. Manual installs may be needed.
    echo Install "App Installer" from Microsoft Store for automatic setup.
    echo.
)

REM --- Check for Git ---
where git >nul 2>&1
if %errorlevel% neq 0 (
    echo [SETUP] Git not found. Installing via winget...
    winget install -e --id Git.Git --accept-package-agreements --accept-source-agreements --silent
    if %errorlevel% equ 0 (
        echo Git installed successfully.
    ) else (
        echo [ERROR] Failed to install Git. Please install manually.
    )
    echo.
) else (
    echo [INFO] Git is already installed.
)

REM --- Check for Python ---
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [SETUP] Python not found. Installing via winget...
    winget install -e --id Python.Python.3.11 --accept-package-agreements --accept-source-agreements --silent
    if %errorlevel% equ 0 (
        echo Python installed successfully.
    ) else (
        echo [ERROR] Failed to install Python. Please install manually.
    )
    echo.
) else (
    echo [INFO] Python is already installed.
)

REM --- Check for pip (usually comes with Python) ---
where pip >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARN] pip not found. This may indicate Python installation issues.
    echo Please ensure Python was installed with pip enabled.
    echo.
) else (
    echo [INFO] pip is already installed.
)

REM --- Create virtual environment if it doesn't exist ---
if not exist venv (
    echo [SETUP] Creating Python virtual environment...
    python -m venv venv
    if %errorlevel% equ 0 (
        echo Virtual environment created successfully.
    ) else (
        echo [ERROR] Failed to create virtual environment.
    )
    echo.
) else (
    echo [INFO] Virtual environment already exists.
)

REM --- Activate virtual environment and install dependencies ---
echo [SETUP] Installing Python dependencies...
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment.
    pause
    exit /b 1
)

pip install -r requirements.txt
if %errorlevel% equ 0 (
    echo Dependencies installed successfully.
) else (
    echo [ERROR] Failed to install dependencies.
)
echo.

REM --- Setup complete, show options ---
echo =========================================
echo    Setup Complete! Choose an option:
echo =========================================
echo 1. Launch DocTailor Web Interface
echo 2. Run DocTailor CLI Tool
echo 3. Exit
echo.
set /p "choice=Enter your choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo [LAUNCH] Starting DocTailor Web Interface...
    echo Access the application at http://localhost:5000
    echo.
    call python backend/app.py
) else if "%choice%"=="2" (
    echo.
    echo [LAUNCH] DocTailor CLI Tool - Examples:
    echo   python generate.py --list-templates
    echo   python generate.py --list-clients
    echo   python generate.py --template document_templates/base.md --client clientA
    echo.
    echo [LAUNCH] Entering interactive CLI mode (type 'exit' to return to menu):
    echo.
    cmd /k
) else if "%choice%"=="3" (
    echo.
    echo [EXIT] Goodbye!
    exit /b 0
) else (
    echo.
    echo [ERROR] Invalid choice. Please run the script again.
    pause
    exit /b 1
)
