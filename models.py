from sqlalchemy import Column, Integer, String
from database import Base

class Perfume(Base):
    __tablename__ = "perfumes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    image_path = Column(String)
    brand = Column(String)
    clone_of = Column(String)
    clone_image_path = Column(String)  # NEW: Local path to original perfume image
