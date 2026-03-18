from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
import os
import subprocess

from ..core.database import get_db, Project
from ..core.config import settings
from ..utils.file_utils import ensure_dir, sanitize_filename

router = APIRouter(prefix="/api/project", tags=["project"])


@router.post("/create", summary="新建小说项目")
def create_project(
    title: str = Body(..., description="小说名称"),
    genre: str = Body(..., description="小说题材"),
    chapter_words: int = Body(3000, description="单章目标字数"),
    db: Session = Depends(get_db)
):
    safe_title = sanitize_filename(title)
    project_path = os.path.join(settings.PROJECTS_DIR, safe_title)
    
    if os.path.exists(project_path):
        raise HTTPException(status_code=400, detail="项目已存在")
    
    ensure_dir(project_path)
    ensure_dir(os.path.join(project_path, "真相文件库"))
    ensure_dir(os.path.join(project_path, "章节内容"))
    ensure_dir(os.path.join(project_path, "大纲文件"))
    ensure_dir(os.path.join(project_path, "大纲文件/章节大纲"))
    ensure_dir(os.path.join(project_path, "发布内容"))
    
    env_content = f"PROJECT_TITLE={title}\nPROJECT_GENRE={genre}\n"
    with open(os.path.join(project_path, ".env"), "w", encoding="utf-8") as f:
        f.write(env_content)
    
    with open(os.path.join(project_path, "book_rules.md"), "w", encoding="utf-8") as f:
        f.write(f"# {title} - 创作规则\n\n## 题材\n{genre}\n")
    
    with open(os.path.join(project_path, "style_profile.json"), "w", encoding="utf-8") as f:
        f.write('{\n  "style": "default"\n}\n')
    
    truth_files = [
        "current_state.md", "character_profiles.md", "pending_hooks.md",
        "chapter_summaries.md", "subplot_board.md", "emotional_arcs.md",
        "particle_ledger.md"
    ]
    for filename in truth_files:
        with open(os.path.join(project_path, "真相文件库", filename), "w", encoding="utf-8") as f:
            f.write(f"# {filename.replace('.md', '')}\n\n")
    
    project = Project(
        title=title,
        genre=genre,
        chapter_words=chapter_words,
        project_path=project_path,
        create_time=datetime.now()
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    
    return {
        "code": 200,
        "msg": "项目创建成功",
        "data": {
            "id": project.id,
            "title": project.title,
            "genre": project.genre,
            "project_path": project.project_path
        }
    }


@router.get("/list", summary="获取所有小说项目列表")
def get_project_list(db: Session = Depends(get_db)):
    projects = db.query(Project).order_by(Project.create_time.desc()).all()
    
    project_list = []
    for project in projects:
        chapter_count = 0
        total_words = 0
        chapter_dir = os.path.join(project.project_path, "章节内容")
        if os.path.exists(chapter_dir):
            chapters = [d for d in os.listdir(chapter_dir) if os.path.isdir(os.path.join(chapter_dir, d))]
            chapter_count = len(chapters)
            for chapter in chapters:
                content_path = os.path.join(chapter_dir, chapter, "正文.md")
                if os.path.exists(content_path):
                    with open(content_path, "r", encoding="utf-8") as f:
                        total_words += len(f.read().replace("\n", "").replace(" ", ""))
        
        project_list.append({
            "id": project.id,
            "title": project.title,
            "genre": project.genre,
            "chapter_words": project.chapter_words,
            "create_time": project.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "chapter_count": chapter_count,
            "total_words": total_words
        })
    
    return {"code": 200, "data": project_list}


@router.get("/detail", summary="获取项目详情")
def get_project_detail(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    chapter_dir = os.path.join(project.project_path, "章节内容")
    chapter_list = []
    total_words = 0
    
    if os.path.exists(chapter_dir):
        chapters = sorted([d for d in os.listdir(chapter_dir) if os.path.isdir(os.path.join(chapter_dir, d))])
        for chapter in chapters:
            content_path = os.path.join(chapter_dir, chapter, "正文.md")
            words = 0
            if os.path.exists(content_path):
                with open(content_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    words = len(content.replace("\n", "").replace(" ", ""))
                    total_words += words
            chapter_list.append({
                "name": chapter,
                "words": words
            })
    
    return {
        "code": 200,
        "data": {
            "project_info": {
                "id": project.id,
                "title": project.title,
                "genre": project.genre,
                "chapter_words": project.chapter_words,
                "project_path": project.project_path,
                "create_time": project.create_time.strftime("%Y-%m-%d %H:%M:%S")
            },
            "chapter_count": len(chapter_list),
            "total_words": total_words,
            "chapter_list": chapter_list
        }
    }


@router.delete("/delete", summary="删除项目")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    import shutil
    if os.path.exists(project.project_path):
        shutil.rmtree(project.project_path)
    
    db.delete(project)
    db.commit()
    
    return {"code": 200, "msg": "项目删除成功"}
