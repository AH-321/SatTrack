$repoURL = "https://github.com/OptiByte/SatTrack"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Git is not installed. Would you like to install Git now? (Y/N)" -ForegroundColor Yellow
    $response = Read-Host
    if ($response -eq "Y") {
        winget install git
    } else {
        Write-Host "Git is required to clone the SatTrack repository. You can also manually download the repository from $repoURL. Exiting." -ForegroundColor Red
        exit 1
}  
if (-not (Test-Path -Path "SatTrack")) {
    $response = Read-Host "Enter the directory where you want to clone the SatTrack repository (or press Enter to clone in the current directory)"
    if ($response -ne "") {
        git clone $repoURL $response
    } else {
        git clone $repoURL
    }
} else {
    Write-Host "SatTrack repository already exists. Pulling latest changes..." -ForegroundColor Green
    Set-Location -Path "SatTrack"
    git pull
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python is not installed. Would you like to install Python now? (Y/N)" -ForegroundColor Yellow
    $response = Read-Host
    if ($response -eq "Y") {
        winget install python
    } else {
        Write-Host "Python is required to run SatTrack. Exiting." -ForegroundColor Red
        exit 1
    }
}

if (-not (Test-Path -Path "SatTrack\venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Green
    python -m venv SatTrack\venv
} else {
    Write-Host "Virtual environment already exists." -ForegroundColor Green
}
Write-Host "Activating virtual environment..." -ForegroundColor Green
& "SatTrack\venv\Scripts\Activate.ps1"
Write-Host "Installing required Python packages..." -ForegroundColor Green
pip install -r SatTrack\requirements.txt

Write-Host "Setup complete! You can now run SatTrack using the command 'python SatTrack\main.py'." -ForegroundColor Green