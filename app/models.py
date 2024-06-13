# models.py
from sqlalchemy import Column, String, JSON
from .database import Base  # Use relative import if database.py is in the same directory

class Configuration(Base):
    __tablename__ = "configurations"

    country_code = Column(String, primary_key=True, index=True)
    requirements = Column(JSON, nullable=False)
