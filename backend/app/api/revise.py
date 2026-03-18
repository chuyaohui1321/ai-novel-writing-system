from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
import os

from ..core.database import get_db, Project
from ..core.config import settings

router = APIRouter(prefix="/api/revise", tags=["revise"])


@router.post("/chapter", summary="润色章节内容")
def revise_chapter(
    project_id: int = Body(..., description="项目ID"),
    chapter_number: int = Body(..., description="章节号"),
    style: str = Body("default", description="润色风格"),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    chapter_dir = os.path.join(project.project_path, "章节内容", f"第{chapter_number}章")
    content_path = os.path.join(chapter_dir, "正文.md")
    
    content = ""
    if os.path.exists(content_path):
        with open(content_path, "r", encoding="utf-8") as f:
            content = f.read()
    
    return {
        "code": 200,
        "msg": "润色完成",
        "chapter_content": content
    }


@router.post("/fix", summary="定点修复内容")
def fix_content(
    project_id: int = Body(..., description="项目ID"),
    chapter_number: int = Body(..., description="章节号"),
    target: str = Body(..., description="要修复的内容片段"),
    fix: str = Body(..., description="修复后的内容"),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    chapter_dir = os.path.join(project.project_path, "章节内容", f"第{chapter_number}章")
    content_path = os.path.join(chapter_dir, "正文.md")
    
    content = ""
    if os.path.exists(content_path):
        with open(content_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace(target, fix)
        with open(content_path, "w", encoding="utf-8") as f:
            f.write(content)
    
    return {
        "code": 200,
        "msg": "修复完成",
        "chapter_content": content
    }
