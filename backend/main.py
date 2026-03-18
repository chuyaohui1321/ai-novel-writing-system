from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.core.config import settings
from app.api import project, outline, chapter, audit, revise, model, finetune, publish


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="基于 InkOS Agent 的 AI 长篇小说创作系统"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for dir_name in [
    settings.PROJECTS_DIR,
    settings.MODELS_DIR,
    settings.TRAINING_DATA_DIR,
    settings.FINETUNE_TASKS_DIR,
    settings.DB_DIR
]:
    if not os.path.exists(dir_name):
        os.makedirs(dir_name, exist_ok=True)

app.include_router(project.router)
app.include_router(outline.router)
app.include_router(chapter.router)
app.include_router(audit.router)
app.include_router(revise.router)
app.include_router(model.router)
app.include_router(finetune.router)
app.include_router(publish.router)


@app.get("/")
def root():
    return {
        "message": "AI Novel Writing System",
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/api/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
