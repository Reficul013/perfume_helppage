from sqlalchemy import create_engine
from database import Base
from models import Perfume

DATABASE_URL = "sqlite:///./perfumes.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)

print("✅ Database created.")
