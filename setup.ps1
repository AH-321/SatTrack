$repoURL = "https://github.com/OptiByte/SatTrack"

# Check if git is installed
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "Git is not installed. Please install Git to continue." -ForegroundColor Red
    exit 1
}  
if (-not (Test-Path -Path "SatTrack")) {
    Write-Host "Cloning SatTrack repository..." -ForegroundColor Green
    git clone $repoURL
} else {
    Write-Host "SatTrack repository already exists. Pulling latest changes..." -ForegroundColor Green
    Set-Location -Path "SatTrack"
    git pull
}

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python is not installed. Please install Python to continue." -ForegroundColor Red
    exit 1
}
