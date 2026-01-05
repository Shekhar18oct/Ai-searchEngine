# SonarQube Setup Guide for AI Search Engine

This guide will help you set up SonarQube for code security and quality analysis of the AI Search Engine project.

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Local Setup](#local-setup)
- [Running Analysis Locally](#running-analysis-locally)
- [GitHub Actions Integration](#github-actions-integration)
- [Understanding Results](#understanding-results)
- [Troubleshooting](#troubleshooting)

---

## Overview

SonarQube provides:
- **Security Vulnerabilities Detection**: Identifies security hotspots and vulnerabilities
- **Code Quality Analysis**: Detects bugs, code smells, and technical debt
- **Code Coverage**: Tracks test coverage metrics
- **Security Standards**: Checks compliance with OWASP, CWE, and SANS standards
- **Continuous Monitoring**: Tracks quality trends over time

---

## Prerequisites

### Required Software
1. **Java 17 or later** (required by SonarQube)
   - Download: https://www.oracle.com/java/technologies/downloads/
   - Verify: `java -version`

2. **SonarQube Server**
   - **Option A - Docker** (Recommended):
     ```powershell
     docker run -d --name sonarqube -p 9000:9000 sonarqube:latest
     ```
   
   - **Option B - Manual Installation**:
     - Download: https://www.sonarqube.org/downloads/
     - Extract and run: `bin/windows-x86-64/StartSonar.bat`

3. **SonarScanner CLI**
   - Download: https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/
   - Extract and add to PATH
   - Verify: `sonar-scanner --version`

### Python Dependencies
```powershell
pip install coverage pytest-cov bandit pylint
```

---

## Local Setup

### Step 1: Start SonarQube Server

**Using Docker:**
```powershell
docker run -d --name sonarqube -p 9000:9000 sonarqube:latest
```

**Manual Installation:**
```powershell
cd path\to\sonarqube\bin\windows-x86-64
.\StartSonar.bat
```

### Step 2: Access SonarQube Web Interface
1. Open browser: http://localhost:9000
2. Default credentials: `admin` / `admin`
3. Change password when prompted

### Step 3: Create a Project
1. Click **"Create Project"** → **"Manually"**
2. Project Key: `ai-searchengine`
3. Display Name: `AI Search Engine`
4. Click **"Set Up"**

### Step 4: Generate Authentication Token
1. Go to **User** → **My Account** → **Security**
2. Generate Token:
   - Name: `ai-searchengine-local`
   - Type: `Project Analysis Token`
   - Project: `ai-searchengine`
3. **Copy and save the token** (you won't see it again!)

---

## Running Analysis Locally

### Quick Start
```powershell
# Basic scan
.\run_sonar_scan.ps1 -SonarToken "your-token-here"

# With coverage report generation
.\run_sonar_scan.ps1 -SonarToken "your-token-here" -GenerateCoverage

# Custom SonarQube server
.\run_sonar_scan.ps1 -SonarHost "http://your-server:9000" -SonarToken "your-token"
```

### Manual Step-by-Step Analysis

#### 1. Generate Coverage Report
```powershell
python -m pytest tests/ --cov=src --cov-report=xml:coverage.xml --cov-report=html
```

#### 2. Run Security Scanner (Bandit)
```powershell
pip install bandit
bandit -r src -f json -o bandit-report.json
```

#### 3. Run Code Quality Checker (Pylint)
```powershell
pip install pylint
pylint src --output-format=text > pylint-report.txt
```

#### 4. Run SonarQube Scanner
```powershell
sonar-scanner `
  -Dsonar.host.url=http://localhost:9000 `
  -Dsonar.login=your-token-here
```

#### 5. View Results
Open: http://localhost:9000/dashboard?id=ai-searchengine

---

## GitHub Actions Integration

### Setup GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Add the following secrets:

   - **SONAR_TOKEN**:
     - Generate in SonarQube: User → My Account → Security
     - Type: `Global Analysis Token` or `Project Analysis Token`
   
   - **SONAR_HOST_URL**:
     - For SonarCloud: `https://sonarcloud.io`
     - For self-hosted: `https://your-sonarqube-server.com`

### Workflow Configuration

The workflow (`.github/workflows/sonarqube.yml`) automatically runs on:
- Push to `main` or `develop` branches
- Pull requests (opened, synchronized, reopened)

### What the Workflow Does

1. ✅ Checks out code
2. ✅ Sets up Python environment
3. ✅ Installs dependencies
4. ✅ Runs tests with coverage
5. ✅ Runs Bandit security scanner
6. ✅ Runs Pylint code quality checker
7. ✅ Executes SonarQube analysis
8. ✅ Checks Quality Gate status
9. ✅ Uploads reports as artifacts

### Triggering Manual Workflow

```powershell
# From GitHub UI: Actions → SonarQube Security and Quality Analysis → Run workflow

# Or using GitHub CLI
gh workflow run sonarqube.yml
```

---

## Understanding Results

### Dashboard Metrics

#### Reliability (Bugs)
- **A**: No bugs
- **E**: Critical bugs present
- Target: **A** rating

#### Security (Vulnerabilities)
- Identifies security vulnerabilities
- Shows security hotspots for review
- Target: **A** rating

#### Security Review (Hotspots)
- Code that requires manual security review
- Target: **100%** reviewed

#### Maintainability (Code Smells)
- Technical debt
- Code complexity issues
- Target: **A** rating (< 5% debt ratio)

#### Coverage
- Test code coverage percentage
- Target: **> 80%**

#### Duplications
- Duplicated code blocks
- Target: **< 3%**

### Quality Gates

Default Quality Gate conditions:
- No new bugs
- No new vulnerabilities
- No new security hotspots
- Coverage on new code > 80%
- Duplication on new code < 3%

**If Quality Gate fails**: Review the issues and fix them before merging.

---

## Troubleshooting

### Issue: "sonar-scanner: command not found"
**Solution**: 
1. Download SonarScanner from https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/
2. Extract to a directory (e.g., `C:\sonar-scanner`)
3. Add to PATH: `$env:Path += ";C:\sonar-scanner\bin"`
4. Restart PowerShell

### Issue: "Unauthorized" error
**Solution**:
- Verify token is correct
- Ensure token has analysis permissions
- Check token hasn't expired

### Issue: "SonarQube server not reachable"
**Solution**:
- Verify SonarQube is running: http://localhost:9000
- Check firewall settings
- Verify host URL is correct

### Issue: Coverage report not showing
**Solution**:
1. Ensure tests are running successfully
2. Check `coverage.xml` was generated
3. Verify `sonar.python.coverage.reportPaths=coverage.xml` in `sonar-project.properties`

### Issue: Analysis takes too long
**Solution**:
- Reduce `sonar.cpd.python.minimumTokens` value
- Add more exclusions to `sonar.exclusions`
- Check server resources

### Issue: Quality Gate always fails
**Solution**:
1. Review specific failing conditions in SonarQube dashboard
2. Fix reported issues in code
3. Consider customizing Quality Gate for your needs
4. Start with fewer strict conditions initially

---

## Configuration Files

### sonar-project.properties
Main configuration file for project analysis settings. Customize:
- Project key and name
- Source and test directories
- Exclusions
- Coverage report paths
- Security scanner integrations

### run_sonar_scan.ps1
PowerShell script for local analysis automation. Parameters:
- `-SonarToken`: Authentication token
- `-SonarHost`: SonarQube server URL
- `-GenerateCoverage`: Run tests and generate coverage

### .github/workflows/sonarqube.yml
GitHub Actions workflow for automated CI/CD analysis.

---

## Best Practices

1. **Run Locally Before Committing**: Catch issues early
2. **Fix Blockers and Critical Issues First**: Prioritize security
3. **Maintain High Coverage**: Aim for > 80% code coverage
4. **Review Security Hotspots**: Don't ignore them
5. **Regular Scans**: Run on every commit/PR
6. **Monitor Trends**: Track quality metrics over time
7. **Set Realistic Quality Gates**: Start lenient, gradually improve

---

## Additional Resources

- [SonarQube Documentation](https://docs.sonarqube.org/latest/)
- [SonarQube Python Analysis](https://docs.sonarqube.org/latest/analysis/languages/python/)
- [SonarScanner CLI](https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/)
- [Quality Gates](https://docs.sonarqube.org/latest/user-guide/quality-gates/)

---

## Support

For issues or questions:
1. Check SonarQube logs: `logs/sonar.log`
2. Review GitHub Actions logs
3. Consult SonarQube community: https://community.sonarsource.com/

---

**Happy Coding with Confidence! 🚀**
