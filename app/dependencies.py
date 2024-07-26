from passlib.context import CryptContext
from sqlalchemy.orm import sessionmaker
from app.database import Database

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = Database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
