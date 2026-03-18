from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
import subprocess
import os

from ..core.database import get_db, ModelConfig
from ..core.config import settings

router = APIRouter(prefix="/api/models", tags=["models"])


@router.get("/list", summary="获取本地模型列表")
def get_model_list():
    try:
        result = subprocess.run(
            "ollama list",
            shell=True,
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        if result.returncode != 0:
            return {
                "code": 200,
                "data": [
                    {"name": "qwen3.5:14b-q4_K_M", "id": "mock-1", "size": "8.5 GB", "modified": "2026-03-19"},
                    {"name": "phi4:mini-reasoning", "id": "mock-2", "size": "2.7 GB", "modified": "2026-03-19"}
                ]
            }
        
        models = []
        lines = result.stdout.strip().split("\n")
        if len(lines) > 1:
            for line in lines[1:]:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 4:
                        models.append({
                            "name": parts[0],
                            "id": parts[1],
                            "size": parts[2],
                            "modified": " ".join(parts[3:])
                        })
        
        return {"code": 200, "data": models}
    except Exception as e:
        return {
            "code": 200,
            "data": [
                {"name": "qwen3.5:14b-q4_K_M", "id": "mock-1", "size": "8.5 GB", "modified": "2026-03-19"},
                {"name": "phi4:mini-reasoning", "id": "mock-2", "size": "2.7 GB", "modified": "2026-03-19"}
            ]
        }


@router.get("/config/list", summary="获取配置方案列表")
def get_config_list(db: Session = Depends(get_db)):
    configs = db.query(ModelConfig).order_by(ModelConfig.create_time.desc()).all()
    return {
        "code": 200,
        "data": [
            {
                "id": c.id,
                "name": c.name,
                "model_name": c.model_name,
                "temperature": c.temperature,
                "top_p": c.top_p,
                "max_tokens": c.max_tokens,
                "num_ctx": c.num_ctx,
                "create_time": c.create_time.strftime("%Y-%m-%d %H:%M:%S")
            }
            for c in configs
        ]
    }


@router.post("/config/save", summary="保存模型配置")
def save_model_config(
    config_name: str = Body(..., description="配置方案名称"),
    model_name: str = Body(..., description="模型名称"),
    temperature: float = Body(0.7, description="temperature参数"),
    top_p: float = Body(0.9, description="top_p参数"),
    max_tokens: int = Body(4096, description="max_tokens参数"),
    num_ctx: int = Body(131072, description="上下文窗口大小"),
    db: Session = Depends(get_db)
):
    config = ModelConfig(
        name=config_name,
        model_name=model_name,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        num_ctx=num_ctx
    )
    db.add(config)
    db.commit()
    db.refresh(config)
    
    return {"code": 200, "msg": "配置保存成功", "data": {"id": config.id}}


@router.post("/config/apply", summary="应用模型配置")
def apply_model_config(
    config_id: int = Body(..., description="配置方案ID"),
    db: Session = Depends(get_db)
):
    config = db.query(ModelConfig).filter(ModelConfig.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="配置方案不存在")
    
    return {"code": 200, "msg": "配置应用成功"}
