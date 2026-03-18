from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
import os

from ..core.database import get_db, Project
from ..core.config import settings
from ..utils.file_utils import ensure_dir

router = APIRouter(prefix="/api/chapter", tags=["chapter"])


@router.post("/write", summary="生成章节内容")
def write_chapter(
    project_id: int = Body(..., description="项目ID"),
    chapter_number: int = Body(..., description="章节号"),
    context: str = Body("", description="自定义创作要求"),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    chapter_dir = os.path.join(project.project_path, "章节内容", f"第{chapter_number}章")
    ensure_dir(chapter_dir)
    
    draft_content = f"# 第{chapter_number}章\n\n"
    if context:
        draft_content += f"## 创作要求\n{context}\n\n"
    draft_content += "（章节内容生成中...）\n"
    
    draft_path = os.path.join(chapter_dir, "草稿.md")
    with open(draft_path, "w", encoding="utf-8") as f:
        f.write(draft_content)
    
    content_path = os.path.join(chapter_dir, "正文.md")
    with open(content_path, "w", encoding="utf-8") as f:
        f.write(draft_content)
    
    audit_path = os.path.join(chapter_dir, "审计报告.md")
    with open(audit_path, "w", encoding="utf-8") as f:
        f.write("# 审计报告\n\n（待审计）\n")
    
    revision_path = os.path.join(chapter_dir, "修订记录.md")
    with open(revision_path, "w", encoding="utf-8") as f:
        f.write("# 修订记录\n\n")
    
    return {
        "code": 200,
        "msg": "章节创建成功",
        "chapter_content": draft_content
    }


@router.get("/read", summary="读取章节内容")
def read_chapter(
    project_id: int,
    chapter_number: int,
    content_type: str = "正文",
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    chapter_dir = os.path.join(project.project_path, "章节内容", f"第{chapter_number}章")
    content_path = os.path.join(chapter_dir, f"{content_type}.md")
    
    if not os.path.exists(content_path):
        return {"code": 200, "data": ""}
    
    with open(content_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    return {"code": 200, "data": content}


@router.post("/save", summary="保存章节内容")
def save_chapter(
    project_id: int = Body(..., description="项目ID"),
    chapter_number: int = Body(..., description="章节号"),
    content: str = Body(..., description="章节内容"),
    content_type: str = Body("正文", description="内容类型"),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    chapter_dir = os.path.join(project.project_path, "章节内容", f"第{chapter_number}章")
    ensure_dir(chapter_dir)
    
    content_path = os.path.join(chapter_dir, f"{content_type}.md")
    with open(content_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    return {"code": 200, "msg": "章节保存成功"}


@router.post("/rewrite", summary="重新生成章节内容")
def rewrite_chapter(
    project_id: int = Body(..., description="项目ID"),
    chapter_number: int = Body(..., description="章节号"),
    revision: str = Body(..., description="修改要求"),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    chapter_dir = os.path.join(project.project_path, "章节内容", f"第{chapter_number}章")
    ensure_dir(chapter_dir)
    
    revision_path = os.path.join(chapter_dir, "修订记录.md")
    from datetime import datetime
    with open(revision_path, "a", encoding="utf-8") as f:
        f.write(f"\n## {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{revision}\n")
    
    return {
        "code": 200,
        "msg": "修订记录已保存",
        "revision": revision
    }
