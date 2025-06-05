from fastapi import FastAPI, Request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Perfume
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS setup for frontend hosted on Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://perfume-helppage-ui.onrender.com"],  # production frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
DATABASE_URL = "sqlite:///./perfumes.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# ✅ Route using request to build correct base URL
@app.get("/perfumes/")
def list_perfumes(request: Request):
    db = SessionLocal()
    base_url = str(request.base_url).rstrip("/")  # e.g. https://perfume-helppage.onrender.com

    perfumes = db.query(Perfume).all()
    result = []
    for p in perfumes:
        scentari_img = f"{base_url}/{p.image_path}" if p.image_path else None
        clone_img = f"{base_url}/{p.clone_image_path}" if p.clone_image_path else None
        result.append({
            "name": p.name,
            "brand": p.brand,
            "image_url": scentari_img,
            "clone_of": p.clone_of,
            "clone_image_url": clone_img
        })
    db.close()
    return result
