import os
import requests
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Perfume, Base

DATABASE_URL = "sqlite:///./perfumes.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
session = Session()

SAVE_FOLDER = "static/images"
os.makedirs(SAVE_FOLDER, exist_ok=True)

def sanitize_filename(name):
    return "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip()

def download_and_save(url, name, label):
    filename = f"{sanitize_filename(name)}_{label}.jpg"[:100]
    filepath = os.path.join(SAVE_FOLDER, filename)

    if os.path.exists(filepath):
        return filepath.replace("\\", "/")

    try:
        response = requests.get(url, timeout=10)
        with open(filepath, "wb") as f:
            f.write(response.content)
        print(f"✅ Saved {label} image for {name}")
        return filepath.replace("\\", "/")
    except Exception as e:
        print(f"❌ Failed to download {label} image for {name}: {e}")
        return None

perfumes = session.query(Perfume).all()
for perfume in perfumes:
    # Download Scentari image
    if perfume.image_path and perfume.image_path.startswith("http"):
        local_path = download_and_save(perfume.image_path, perfume.name, "scentari")
        if local_path:
            perfume.image_path = local_path

    # Download Original perfume image
    if perfume.clone_image_path and perfume.clone_image_path.startswith("http"):
        local_path = download_and_save(perfume.clone_image_path, perfume.clone_of or perfume.name, "clone")
        if local_path:
            perfume.clone_image_path = local_path

    session.commit()

session.close()
