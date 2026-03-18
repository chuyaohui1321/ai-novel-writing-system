from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from .config import settings


if not os.path.exists(settings.DB_DIR):
    os.makedirs(settings.DB_DIR)


engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    genre = Column(String(50), nullable=False)
    chapter_words = Column(Integer, default=3000)
    project_path = Column(String(500), nullable=False)
    create_time = Column(DateTime, default=datetime.now)


class ModelConfig(Base):
    __tablename__ = "model_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    model_name = Column(String(200), nullable=False)
    temperature = Column(Float, default=0.7)
    top_p = Column(Float, default=0.9)
    max_tokens = Column(Integer, default=4096)
    num_ctx = Column(Integer, default=131072)
    create_time = Column(DateTime, default=datetime.now)


class FinetuneTask(Base):
    __tablename__ = "finetune_tasks"
    
    id = Column(String(100), primary_key=True, index=True)
    base_model = Column(String(200), nullable=False)
    learning_rate = Column(Float, default=2e-4)
    num_epochs = Column(Integer, default=3)
    lora_rank = Column(Integer, default=8)
    start_time = Column(DateTime, default=datetime.now)
    status = Column(String(20), default="running")


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
