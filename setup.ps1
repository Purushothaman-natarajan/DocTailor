# DocTailor Setup & Launcher (PowerShell Version)
Write-Host "=========================================" -ForegroundColor Green
Write-Host "    DocTailor - Document Customization Toolkit" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

# --- Check for winget (Windows Package Manager) ---
if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
    Write-Warning "[WARN] winget not found. Manual installs may be needed."
    Write-Host "Install 'App Installer' from Microsoft Store for automatic setup."
    Write-Host ""
}

# --- Check for Git ---
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "[SETUP] Git not found. Installing via winget..." -ForegroundColor Yellow
    winget install -e --id Git.Git --accept-package-agreements --accept-source-agreements --silent
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Git installed successfully." -ForegroundColor Green
    } else {
        Write-Error "[ERROR] Failed to install Git. Please install manually."
    }
    Write-Host ""
} else {
    Write-Host "[INFO] Git is already installed." -ForegroundColor Green
}

# --- Check for Python ---
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "[SETUP] Python not found. Installing via winget..." -ForegroundColor Yellow
    winget install -e --id Python.Python.3.11 --accept-package-agreements --accept-source-agreements --silent
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Python installed successfully." -ForegroundColor Green
    } else {
        Write-Error "[ERROR] Failed to install Python. Please install manually."
    }
    Write-Host ""
} else {
    Write-Host "[INFO] Python is already installed." -ForegroundColor Green
}

# --- Check for pip ---
if (-not (Get-Command pip -ErrorAction SilentlyContinue)) {
    Write-Warning "[WARN] pip not found. This may indicate Python installation issues."
    Write-Host "Please ensure Python was installed with pip enabled."
    Write-Host ""
} else {
    Write-Host "[INFO] pip is already installed." -ForegroundColor Green
}

# --- Create virtual environment if it doesn't exist ---
if (-not (Test-Path "venv")) {
    Write-Host "[SETUP] Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Virtual environment created successfully." -ForegroundColor Green
    } else {
        Write-Error "[ERROR] Failed to create virtual environment."
    }
    Write-Host ""
} else {
    Write-Host "[INFO] Virtual environment already exists." -ForegroundColor Green
}

# --- Activate virtual environment and install dependencies ---
Write-Host "[SETUP] Installing Python dependencies..." -ForegroundColor Yellow
& venv\Scripts\Activate.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Error "[ERROR] Failed to activate virtual environment."
    Pause
    exit 1
}

pip install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "Dependencies installed successfully." -ForegroundColor Green
} else {
    Write-Error "[ERROR] Failed to install dependencies."
}
Write-Host ""

# --- Setup complete, show options ---
Write-Host "=========================================" -ForegroundColor Green
Write-Host "    Setup Complete! Choose an option:" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host "1. Launch DocTailor Web Interface"
Write-Host "2. Run DocTailor CLI Tool"
Write-Host "3. Exit"
Write-Host ""
$choice = Read-Host "Enter your choice (1-3)"

if ($choice -eq "1") {
    Write-Host ""
    Write-Host "[LAUNCH] Starting DocTailor Web Interface..." -ForegroundColor Green
    Write-Host "Access the application at http://localhost:5000" -ForegroundColor Cyan
    Write-Host ""
    python backend/app.py
} elseif ($choice -eq "2") {
    Write-Host ""
    Write-Host "[LAUNCH] DocTailor CLI Tool - Examples:" -ForegroundColor Green
    Write-Host "  python generate.py --list-templates"
    Write-Host "  python generate.py --list-clients"
    Write-Host "  python generate.py --template document_templates/base.md --client clientA"
    Write-Host ""
    Write-Host "[LAUNCH] Entering interactive CLI mode (type 'exit' to return to menu):" -ForegroundColor Green
    Write-Host ""
    # Start interactive PowerShell session
    Start-Process powershell.exe -ArgumentList "-NoExit"
} elseif ($choice -eq "3") {
    Write-Host ""
    Write-Host "[EXIT] Goodbye!" -ForegroundColor Green
    exit 0
} else {
    Write-Host ""
    Write-Host "[ERROR] Invalid choice. Please run the script again." -ForegroundColor Red
    Pause
    exit 1
}