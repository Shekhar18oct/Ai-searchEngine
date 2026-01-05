# SonarQube Analysis Script
# This script runs SonarQube scanner locally for the AI Search Engine project

param(
    [string]$SonarHost = "http://localhost:9000",
    [string]$SonarToken = "",
    [switch]$GenerateCoverage = $false
)

Write-Host "=== SonarQube Analysis for AI Search Engine ===" -ForegroundColor Cyan

# Check if sonar-scanner is installed
$sonarScanner = Get-Command sonar-scanner -ErrorAction SilentlyContinue
if (-not $sonarScanner) {
    Write-Host "ERROR: sonar-scanner is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please download from: https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/" -ForegroundColor Yellow
    exit 1
}

# Check if SonarQube token is provided
if ([string]::IsNullOrWhiteSpace($SonarToken)) {
    Write-Host "WARNING: No SonarQube token provided" -ForegroundColor Yellow
    Write-Host "You can generate a token in SonarQube: User > My Account > Security" -ForegroundColor Yellow
    Write-Host "Usage: .\run_sonar_scan.ps1 -SonarToken 'your-token-here'" -ForegroundColor Yellow
    $continue = Read-Host "Continue without token? (y/n)"
    if ($continue -ne 'y') {
        exit 0
    }
}

# Optional: Generate coverage report
if ($GenerateCoverage) {
    Write-Host "`nGenerating test coverage report..." -ForegroundColor Cyan
    
    # Install coverage if not already installed
    pip install coverage pytest-cov | Out-Null
    
    # Run tests with coverage
    python -m pytest tests/ --cov=src --cov-report=xml:coverage.xml --cov-report=html
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Coverage report generated successfully" -ForegroundColor Green
    } else {
        Write-Host "Warning: Coverage generation failed" -ForegroundColor Yellow
    }
}

# Optional: Run Bandit security scanner
Write-Host "`nRunning Bandit security scanner..." -ForegroundColor Cyan
pip install bandit | Out-Null
bandit -r src -f json -o bandit-report.json
if ($LASTEXITCODE -eq 0) {
    Write-Host "Bandit security scan completed" -ForegroundColor Green
}

# Optional: Run Pylint
Write-Host "`nRunning Pylint code quality checker..." -ForegroundColor Cyan
pip install pylint | Out-Null
pylint src --output-format=text | Out-File -FilePath pylint-report.txt -Encoding UTF8
Write-Host "Pylint analysis completed" -ForegroundColor Green

# Build SonarQube scanner command
Write-Host "`nStarting SonarQube analysis..." -ForegroundColor Cyan

$sonarArgs = @(
    "-Dsonar.host.url=$SonarHost"
)

if (-not [string]::IsNullOrWhiteSpace($SonarToken)) {
    $sonarArgs += "-Dsonar.login=$SonarToken"
}

# Run SonarQube scanner
& sonar-scanner $sonarArgs

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n=== SonarQube Analysis Completed Successfully ===" -ForegroundColor Green
    Write-Host "View results at: $SonarHost/dashboard?id=ai-searchengine" -ForegroundColor Cyan
} else {
    Write-Host "`n=== SonarQube Analysis Failed ===" -ForegroundColor Red
    exit 1
}
