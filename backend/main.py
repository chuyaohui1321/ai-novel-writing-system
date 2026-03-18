from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import os

app = FastAPI(title="AI Novel Writing System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "AI Novel Writing System API", "version": "1.0.0"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/project/create", summary="新建小说项目")
def create_project(
    title: str = Body(..., description="小说名称"),
    genre: str = Body(..., description="小说题材"),
    chapter_words: int = Body(3000, description="单章目标字数")
):
    cmd = f'inkos book create --title "{title}" --genre {genre} --chapter-words {chapter_words}'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        return {"code": 500, "msg": "项目创建失败", "error": result.stderr}
    return {"code": 200, "msg": "项目创建成功", "data": {"title": title, "genre": genre}}

@app.get("/api/project/list", summary="获取项目列表")
def list_projects():
    return {"code": 200, "msg": "success", "data": []}

@app.get("/api/model/list", summary="获取模型列表")
def list_models():
    return {"code": 200, "msg": "success", "data": []}

@app.post("/api/chat/generate", summary="生成内容")
def generate_content(
    prompt: str = Body(..., description="提示词"),
    model: str = Body("default", description="模型名称")
):
    return {"code": 200, "msg": "success", "data": {"content": "生成的内容"}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
