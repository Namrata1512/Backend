# Pre-Submission Checklist

## Files Required
- [x] docker-compose.yml
- [x] README.md
- [x] .gitignore
- [x] mock-server/Dockerfile
- [x] mock-server/app.py
- [x] mock-server/requirements.txt
- [x] mock-server/data/customers.json
- [x] pipeline-service/Dockerfile
- [x] pipeline-service/main.py
- [x] pipeline-service/database.py
- [x] pipeline-service/requirements.txt
- [x] pipeline-service/models/__init__.py
- [x] pipeline-service/models/customer.py
- [x] pipeline-service/services/__init__.py
- [x] pipeline-service/services/ingestion.py

## Verification Steps
- [x] All services start: `docker-compose up -d`
- [x] Flask endpoints work
- [x] FastAPI endpoints work
- [x] Data ingestion successful
- [x] Database contains data
- [x] No hardcoded credentials
- [x] All tests pass: `.\test-all.ps1`

## Submission
- [x] Code pushed to GitHub
- [x] Repository is public
- [x] README is clear and complete
- [x] Email GitHub link to assessment provider
