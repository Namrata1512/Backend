# Backend Developer Technical Assessment

A complete data pipeline solution with Flask mock server, FastAPI ingestion service, and PostgreSQL database orchestrated with Docker Compose.

## Architecture

```
Flask (Port 5000) → FastAPI (Port 8000) → PostgreSQL (Port 5432)
     JSON Data         Data Pipeline         Database Storage
```

## Prerequisites

- Docker Desktop (running)
- Python 3.10+
- Git

Verify Docker installation:
```bash
docker --version
docker-compose --version
```

## Project Structure

```
project-root/
├── docker-compose.yml
├── README.md
├── mock-server/
│   ├── app.py
│   ├── data/
│   │   └── customers.json (21 customers)
│   ├── Dockerfile
│   └── requirements.txt
└── pipeline-service/
    ├── main.py
    ├── models/
    │   └── customer.py
    ├── services/
    │   └── ingestion.py
    ├── database.py
    ├── Dockerfile
    └── requirements.txt
```

## Quick Start

### 1. Setup Directory Structure

Create the project folders:
```bash
mkdir -p project-root/mock-server/data
mkdir -p project-root/pipeline-service/models
mkdir -p project-root/pipeline-service/services
cd project-root
```

### 2. Create Files

Copy all the provided files into their respective directories according to the project structure above.

### 3. Start All Services

```bash
docker-compose up -d
```

Wait for all services to start (approximately 30 seconds). Check status:
```bash
docker-compose ps
```

### 4. Test the Pipeline

**Test Flask Mock Server:**
```bash
# Health check
curl http://localhost:5000/api/health

# Get paginated customers
curl "http://localhost:5000/api/customers?page=1&limit=5"

# Get single customer
curl http://localhost:5000/api/customers/CUST001
```

**Test FastAPI Pipeline:**
```bash
# Health check
curl http://localhost:8000/api/health

# Ingest data from Flask into PostgreSQL
iwr "http://localhost:8000/api/ingest" -Method POST

# Get customers from database
curl "http://localhost:8000/api/customers?page=1&limit=5"

# Get single customer from database
curl http://localhost:8000/api/customers/CUST001
```

## API Endpoints

### Flask Mock Server (Port 5000)

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/api/health` | GET | Health check | None |
| `/api/customers` | GET | Get paginated customers | `page`, `limit` |
| `/api/customers/{id}` | GET | Get single customer | `id` (path) |

**Example Response:**
```json
{
  "data": [...],
  "total": 21,
  "page": 1,
  "limit": 10
}
```

### FastAPI Pipeline (Port 8000)

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/api/health` | GET | Health check | None |
| `/api/ingest` | POST | Ingest data from Flask | None |
| `/api/customers` | GET | Get paginated customers | `page`, `limit` |
| `/api/customers/{id}` | GET | Get single customer | `id` (path) |

**Ingestion Response:**
```json
{
  "status": "success",
  "records_processed": 21
}
```

## Database Schema

**Table: customers**

| Column | Type | Constraints |
|--------|------|-------------|
| customer_id | VARCHAR(50) | PRIMARY KEY |
| first_name | VARCHAR(100) | NOT NULL |
| last_name | VARCHAR(100) | NOT NULL |
| email | VARCHAR(255) | NOT NULL |
| phone | VARCHAR(20) | - |
| address | TEXT | - |
| date_of_birth | DATE | - |
| account_balance | DECIMAL(15,2) | - |
| created_at | TIMESTAMP | - |

## Features

✅ Flask mock server with JSON data source
✅ Pagination support on both services
✅ FastAPI automatic pagination handling
✅ Upsert logic (insert or update on conflict)
✅ SQLAlchemy ORM models
✅ Error handling with proper HTTP status codes
✅ Health check endpoints
✅ Docker orchestration with compose
✅ Environment variable configuration
✅ No hardcoded credentials
✅ Complete documentation

## Advanced Usage

### Accessing PostgreSQL Database

```bash
docker exec -it customer_db psql -U postgres -d customer_db
```

Then run SQL queries:
```sql
-- View all customers
SELECT * FROM customers;

-- Count customers
SELECT COUNT(*) FROM customers;

-- Find specific customer
SELECT * FROM customers WHERE customer_id = 'CUST001';
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f mock-server
docker-compose logs -f pipeline-service
docker-compose logs -f postgres
```

### Restart Services

```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart pipeline-service
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (clears database)
docker-compose down -v
```

## Troubleshooting

**Issue: Services won't start**
- Ensure Docker Desktop is running
- Check port availability (5000, 8000, 5432)
- Run `docker-compose down -v` and try again

**Issue: Connection refused**
- Wait 30-60 seconds after `docker-compose up`
- Check service status: `docker-compose ps`
- View logs: `docker-compose logs -f`

**Issue: Ingestion fails**
- Ensure Flask service is running: `curl http://localhost:5000/api/health`
- Check PostgreSQL is ready: `docker-compose logs postgres`
- Retry ingestion after services stabilize

**Issue: Database connection errors**
- Verify DATABASE_URL environment variable
- Check PostgreSQL container is healthy
- Ensure database `customer_db` exists

## Development

### Rebuild Services

After code changes:
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Add More Customers

Edit `mock-server/data/customers.json` and add more customer objects, then restart:
```bash
docker-compose restart mock-server
```

## Evaluation Checklist

- [x] All 3 services start with `docker-compose up`
- [x] Flask serves data with pagination
- [x] FastAPI ingests data successfully
- [x] All API endpoints work correctly
- [x] README with comprehensive setup instructions
- [x] No hardcoded credentials (environment variables)
- [x] Proper error handling (404, 500)
- [x] SQLAlchemy models implemented
- [x] Upsert logic on conflict
- [x] Clean project structure
- [x] Complete documentation


## License

This project is created for educational and assessment purposes.

---

**Author:** Namrata R Gachchi  
**Date:** January 2026  
**Assessment:** Backend Developer Technical Assessment