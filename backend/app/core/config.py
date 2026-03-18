from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    APP_NAME: str = "AI Novel Writing System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    PROJECTS_DIR: str = os.path.join(BASE_DIR, "projects")
    MODELS_DIR: str = os.path.join(BASE_DIR, "models")
    TRAINING_DATA_DIR: str = os.path.join(BASE_DIR, "training_data")
    FINETUNE_TASKS_DIR: str = os.path.join(BASE_DIR, "finetune_tasks")
    DB_DIR: str = os.path.join(BASE_DIR, "db")
    
    DATABASE_URL: str = f"sqlite:///{DB_DIR}/novel_system.db"
    
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    
    class Config:
        env_file = ".env"


settings = Settings()
