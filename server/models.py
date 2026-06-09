# server/models.py
from sqlalchemy import Column, Integer, String, DateTime, Text
from server.database import Base
from datetime import datetime

class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    version = Column(String, nullable=False)
    description = Column(String)
    author = Column(String)
    github_url = Column(String)
    download_url = Column(String)
    install_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    manifest_json = Column(Text)
