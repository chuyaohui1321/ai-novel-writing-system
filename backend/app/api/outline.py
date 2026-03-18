from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
import os

from ..core.database import get_db, Project
from ..core.config import settings
from ..utils.file_utils import ensure_dir

router = APIRouter(prefix="/api/outline", tags=["outline"])


@router.post("/full", summary="生成全卷大纲")
def generate_full_outline(
    project_id: int = Body(..., description="项目ID"),
    core_idea: str = Body(..., description="核心创意"),
    volume_count: int = Body(5, description="分卷数量"),
    chapters_per_volume: int = Body(20, description="每卷章节数"),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    rules_path = os.path.join(project.project_path, "book_rules.md")
    with open(rules_path, "a", encoding="utf-8") as f:
        f.write(f"\n## 核心创意\n{core_idea}\n")
    
    outline_dir = os.path.join(project.project_path, "大纲文件")
    ensure_dir(outline_dir)
    
    outline_content = f"""# 全卷大纲

## 核心创意
{core_idea}

## 分卷规划

"""
    for v in range(1, volume_count + 1):
        outline_content += f"### 第{v}卷\n"
        for c in range(1, chapters_per_volume + 1):
            outline_content += f"- 第{c}章\n"
        outline_content += "\n"
    
    outline_path = os.path.join(outline_dir, "全卷大纲.md")
    with open(outline_path, "w", encoding="utf-8") as f:
        f.write(outline_content)
    
    for v in range(1, volume_count + 1):
        volume_path = os.path.join(outline_dir, f"第{v}卷大纲.md")
        with open(volume_path, "w", encoding="utf-8") as f:
            f.write(f"# 第{v}卷大纲\n\n")
    
    return {
        "code": 200,
        "msg": "大纲生成成功",
        "outline": outline_content
    }


@router.get("/read", summary="读取大纲")
def read_outline(
    project_id: int,
    outline_type: str = "full",
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    outline_dir = os.path.join(project.project_path, "大纲文件")
    
    if outline_type == "full":
        outline_path = os.path.join(outline_dir, "全卷大纲.md")
    else:
        outline_path = os.path.join(outline_dir, f"{outline_type}大纲.md")
    
    if not os.path.exists(outline_path):
        return {"code": 200, "data": ""}
    
    with open(outline_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    return {"code": 200, "data": content}


@router.post("/save", summary="保存大纲")
def save_outline(
    project_id: int = Body(..., description="项目ID"),
    outline_type: str = Body("full", description="大纲类型"),
    content: str = Body(..., description="大纲内容"),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    outline_dir = os.path.join(project.project_path, "大纲文件")
    ensure_dir(outline_dir)
    
    if outline_type == "full":
        outline_path = os.path.join(outline_dir, "全卷大纲.md")
    else:
        outline_path = os.path.join(outline_dir, f"{outline_type}大纲.md")
    
    with open(outline_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    return {"code": 200, "msg": "大纲保存成功"}
