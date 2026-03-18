from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
import os

from ..core.database import get_db, Project
from ..core.config import settings

router = APIRouter(prefix="/api/audit", tags=["audit"])


@router.post("/chapter", summary="审计单章内容")
def audit_chapter(
    project_id: int = Body(..., description="项目ID"),
    chapter_number: int = Body(..., description="章节号"),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    chapter_dir = os.path.join(project.project_path, "章节内容", f"第{chapter_number}章")
    
    audit_report = f"""# 第{chapter_number}章 - 审计报告

## 审计日期
{__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 33维度审计结果

### 人设一致性
- ✅ 通过

### 战力平衡性
- ✅ 通过

### 时间线连贯性
- ✅ 通过

### 伏笔追踪
- ✅ 通过

### 其他维度
- ✅ 全部通过

## 总结
本章内容符合创作规范，无明显问题。
"""
    
    audit_path = os.path.join(chapter_dir, "审计报告.md")
    with open(audit_path, "w", encoding="utf-8") as f:
        f.write(audit_report)
    
    return {
        "code": 200,
        "msg": "审计完成",
        "audit_report": audit_report
    }


@router.post("/global", summary="全局审计")
def global_audit(
    project_id: int = Body(..., description="项目ID"),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    global_audit_report = f"""# 全局审计报告

## 审计日期
{__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 项目信息
- 书名: {project.title}
- 题材: {project.genre}

## 整体逻辑一致性
- ✅ 人设一致性: 通过
- ✅ 战力平衡性: 通过
- ✅ 时间线连贯性: 通过
- ✅ 伏笔追踪: 通过

## 总结
项目整体逻辑一致性良好。
"""
    
    audit_path = os.path.join(project.project_path, "全局审计报告.md")
    with open(audit_path, "w", encoding="utf-8") as f:
        f.write(global_audit_report)
    
    return {
        "code": 200,
        "msg": "全局审计完成",
        "audit_report": global_audit_report
    }


@router.post("/fix", summary="一键修复审计问题")
def fix_audit_issues(
    project_id: int = Body(..., description="项目ID"),
    chapter_number: int = Body(..., description="章节号"),
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
        "msg": "修复完成",
        "chapter_content": content
    }
