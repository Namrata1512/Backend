from fastapi import FastAPI, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from database import get_db, init_db
from models.customer import Customer
from services.ingestion import ingest_customers_from_flask
import os

app = FastAPI(title="Customer Data Pipeline")

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "fastapi-pipeline"}

@app.post("/api/ingest")
async def ingest_data():
    """Ingest customer data from Flask mock server"""
    try:
        mock_server_url = os.getenv("MOCK_SERVER_URL", "http://mock-server:5000")
        records_processed = ingest_customers_from_flask(mock_server_url)
        
        return {
            "status": "success",
            "records_processed": records_processed
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

@app.get("/api/customers")
async def get_customers(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get paginated list of customers from database"""
    try:
        # Calculate offset
        offset = (page - 1) * limit
        
        # Get total count
        total = db.query(Customer).count()
        
        # Get paginated customers
        customers = db.query(Customer).offset(offset).limit(limit).all()
        
        # Convert to dict
        customer_list = [
            {
                "customer_id": c.customer_id,
                "first_name": c.first_name,
                "last_name": c.last_name,
                "email": c.email,
                "phone": c.phone,
                "address": c.address,
                "date_of_birth": c.date_of_birth.isoformat() if c.date_of_birth else None,
                "account_balance": float(c.account_balance) if c.account_balance else 0.0,
                "created_at": c.created_at.isoformat() if c.created_at else None
            }
            for c in customers
        ]
        
        return {
            "data": customer_list,
            "total": total,
            "page": page,
            "limit": limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/api/customers/{customer_id}")
async def get_customer(customer_id: str, db: Session = Depends(get_db)):
    """Get single customer by ID"""
    try:
        customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
        
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        return {
            "data": {
                "customer_id": customer.customer_id,
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "email": customer.email,
                "phone": customer.phone,
                "address": customer.address,
                "date_of_birth": customer.date_of_birth.isoformat() if customer.date_of_birth else None,
                "account_balance": float(customer.account_balance) if customer.account_balance else 0.0,
                "created_at": customer.created_at.isoformat() if customer.created_at else None
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)