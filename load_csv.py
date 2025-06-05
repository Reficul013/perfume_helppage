import pandas as pd
from sqlalchemy import create_engine
from models import Perfume, Base
from database import Base

# Path to enriched CSV
CSV_FILE = "scentari_perfumes_enriched_final.csv"

# Setup database connection
DATABASE_URL = "sqlite:///./perfumes.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create tables if not exist
Base.metadata.create_all(bind=engine)

# Load CSV using pandas
df = pd.read_csv(CSV_FILE)

# Clean column names if needed
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

# Rename to match DB schema
df = df.rename(columns={
    "perfume_name": "name",
    "image_url": "image_path",  # scentari image
    "clone_image_url": "clone_image_path"
})

# Only use required columns
df = df[["name", "image_path", "brand", "clone_of", "clone_image_path"]]

# Save to DB
df.to_sql("perfumes", con=engine, if_exists="append", index=False)

print("✅ Data imported successfully into perfumes.db")
