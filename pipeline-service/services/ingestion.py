import requests
from datetime import datetime
from decimal import Decimal
from sqlalchemy.dialects.postgresql import insert
from database import SessionLocal
from models.customer import Customer

def ingest_customers_from_flask(mock_server_url: str) -> int:
    """
    Fetch all customers from Flask API with pagination and upsert into PostgreSQL
    
    Args:
        mock_server_url: Base URL of the Flask mock server
        
    Returns:
        Total number of records processed
    """
    db = SessionLocal()
    total_records = 0
    page = 1
    limit = 10
    
    try:
        while True:
            # Fetch data from Flask API
            response = requests.get(
                f"{mock_server_url}/api/customers",
                params={"page": page, "limit": limit},
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            customers = data.get("data", [])
            
            if not customers:
                break
            
            # Upsert customers into database
            for customer_data in customers:
                # Parse date fields
                date_of_birth = None
                if customer_data.get("date_of_birth"):
                    try:
                        date_of_birth = datetime.strptime(
                            customer_data["date_of_birth"], 
                            "%Y-%m-%d"
                        ).date()
                    except ValueError:
                        pass
                
                created_at = None
                if customer_data.get("created_at"):
                    try:
                        created_at = datetime.fromisoformat(
                            customer_data["created_at"].replace("Z", "+00:00")
                        )
                    except ValueError:
                        pass
                
                # Prepare upsert statement
                stmt = insert(Customer).values(
                    customer_id=customer_data["customer_id"],
                    first_name=customer_data["first_name"],
                    last_name=customer_data["last_name"],
                    email=customer_data["email"],
                    phone=customer_data.get("phone"),
                    address=customer_data.get("address"),
                    date_of_birth=date_of_birth,
                    account_balance=Decimal(str(customer_data.get("account_balance", 0))),
                    created_at=created_at
                )
                
                # Update on conflict (upsert logic)
                stmt = stmt.on_conflict_do_update(
                    index_elements=['customer_id'],
                    set_={
                        'first_name': stmt.excluded.first_name,
                        'last_name': stmt.excluded.last_name,
                        'email': stmt.excluded.email,
                        'phone': stmt.excluded.phone,
                        'address': stmt.excluded.address,
                        'date_of_birth': stmt.excluded.date_of_birth,
                        'account_balance': stmt.excluded.account_balance,
                        'created_at': stmt.excluded.created_at
                    }
                )
                
                db.execute(stmt)
                total_records += 1
            
            # Commit after each page
            db.commit()
            
            # Check if we've fetched all records
            if len(customers) < limit:
                break
            
            page += 1
        
        return total_records
        
    except requests.RequestException as e:
        db.rollback()
        raise Exception(f"Error fetching data from Flask API: {str(e)}")
    except Exception as e:
        db.rollback()
        raise Exception(f"Error during ingestion: {str(e)}")
    finally:
        db.close()