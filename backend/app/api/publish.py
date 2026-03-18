from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
import os
import shutil

from ..core.database import get_db, Project
from ..core.config import settings
from ..utils.file_utils import ensure_dir

router = APIRouter(prefix="/api/publish", tags=["publish"])


@router.post("/format", summary="格式标准化")
def format_content(
    project_id: int = Body(..., description="项目ID"),
    chapter_numbers: list = Body(..., description="章节号列表"),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    publish_dir = os.path.join(project.project_path, "发布内容")
    ensure_dir(publish_dir)
    
    formatted_chapters = []
    
    for chapter in chapter_numbers:
        chapter_dir = os.path.join(project.project_path, "章节内容", f"第{chapter}章")
        content_path = os.path.join(chapter_dir, "正文.md")
        
        content = ""
        if os.path.exists(content_path):
            with open(content_path, "r", encoding="utf-8") as f:
                content = f.read()
        
        content = content.replace("\n\n", "\n")
        content = content.replace("#", "")
        content = f"第{chapter}章\n\n{content}"
        
        formatted_path = os.path.join(publish_dir, f"第{chapter}章.md")
        with open(formatted_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        formatted_chapters.append({
            "chapter": chapter,
            "path": formatted_path,
            "content": content
        })
    
    return {
        "code": 200,
        "msg": "格式标准化完成",
        "data": formatted_chapters
    }


@router.post("/check_sensitive", summary="敏感词检测")
def check_sensitive(
    project_id: int = Body(..., description="项目ID"),
    chapter_numbers: list = Body(..., description="章节号列表"),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    sensitive_words = ["敏感词1", "敏感词2", "敏感词3"]
    
    sensitive_results = []
    
    for chapter in chapter_numbers:
        chapter_dir = os.path.join(project.project_path, "章节内容", f"第{chapter}章")
        content_path = os.path.join(chapter_dir, "正文.md")
        
        content = ""
        if os.path.exists(content_path):
            with open(content_path, "r", encoding="utf-8") as f:
                content = f.read()
        
        found_words = []
        for word in sensitive_words:
            if word in content:
                found_words.append(word)
        
        sensitive_results.append({
            "chapter": chapter,
            "sensitive_words": found_words,
            "count": len(found_words)
        })
    
    return {
        "code": 200,
        "msg": "敏感词检测完成",
        "data": sensitive_results
    }


@router.post("/export", summary="批量导出发布内容")
def export_content(
    project_id: int = Body(..., description="项目ID"),
    chapter_numbers: list = Body(..., description="章节号列表"),
    export_path: str = Body("./export", description="导出路径"),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    ensure_dir(export_path)
    
    for chapter in chapter_numbers:
        src_path = os.path.join(project.project_path, "发布内容", f"第{chapter}章.md")
        if os.path.exists(src_path):
            dst_path = os.path.join(export_path, f"第{chapter}章.md")
            shutil.copy(src_path, dst_path)
    
    return {
        "code": 200,
        "msg": "导出完成",
        "export_path": export_path
    }
