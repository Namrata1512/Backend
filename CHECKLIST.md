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
- [ ] All services start: `docker-compose up -d`
- [ ] Flask endpoints work
- [ ] FastAPI endpoints work
- [ ] Data ingestion successful
- [ ] Database contains data
- [ ] No hardcoded credentials
- [ ] All tests pass: `.\test-all.ps1`

## Submission
- [ ] Code pushed to GitHub
- [ ] Repository is public
- [ ] README is clear and complete
- [ ] Email GitHub link to assessment provider