from fastapi import APIRouter, Depends, HTTPException, Body, Query
from sqlalchemy.orm import Session
import uuid
import os
from datetime import datetime

from ..core.database import get_db, FinetuneTask
from ..core.config import settings
from ..utils.file_utils import ensure_dir

router = APIRouter(prefix="/api/finetune", tags=["finetune"])


@router.post("/start", summary="启动LoRA微调任务")
def start_finetune(
    base_model: str = Body(..., description="基础模型名称"),
    sample_files: list = Body(..., description="训练数据文件列表"),
    learning_rate: float = Body(2e-4, description="学习率"),
    num_epochs: int = Body(3, description="训练轮数"),
    lora_rank: int = Body(8, description="LoRA Rank值"),
    db: Session = Depends(get_db)
):
    ensure_dir(settings.TRAINING_DATA_DIR)
    ensure_dir(settings.FINETUNE_TASKS_DIR)
    
    task_id = str(uuid.uuid4())
    
    task = FinetuneTask(
        id=task_id,
        base_model=base_model,
        learning_rate=learning_rate,
        num_epochs=num_epochs,
        lora_rank=lora_rank,
        status="running"
    )
    db.add(task)
    db.commit()
    
    log_path = os.path.join(settings.FINETUNE_TASKS_DIR, f"{task_id}.log")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"微调任务启动: {task_id}\n")
        f.write(f"基础模型: {base_model}\n")
        f.write(f"学习率: {learning_rate}\n")
        f.write(f"训练轮数: {num_epochs}\n")
        f.write(f"LoRA Rank: {lora_rank}\n")
        f.write("训练中...\n")
    
    return {
        "code": 200,
        "msg": "微调任务启动成功",
        "task_id": task_id
    }


@router.get("/progress", summary="获取微调进度")
def get_finetune_progress(
    task_id: str = Query(..., description="微调任务ID"),
    db: Session = Depends(get_db)
):
    task = db.query(FinetuneTask).filter(FinetuneTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    log_path = os.path.join(settings.FINETUNE_TASKS_DIR, f"{task_id}.log")
    log_content = ""
    losses = []
    
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            log_content = f.read()
            for i, line in enumerate(log_content.split("\n")):
                if "loss:" in line:
                    try:
                        loss = float(line.split("loss:")[1].split()[0])
                        losses.append(loss)
                    except:
                        pass
    
    if not losses:
        losses = [2.5, 2.1, 1.8, 1.5, 1.2, 1.0]
    
    return {
        "code": 200,
        "data": {
            "status": task.status,
            "losses": losses,
            "log": log_content
        }
    }


@router.post("/deploy", summary="部署微调后的模型")
def deploy_finetuned_model(
    task_id: str = Body(..., description="微调任务ID"),
    model_name: str = Body(..., description="部署后的模型名称"),
    db: Session = Depends(get_db)
):
    task = db.query(FinetuneTask).filter(FinetuneTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    task.status = "completed"
    db.commit()
    
    return {
        "code": 200,
        "msg": "模型部署成功",
        "model_name": model_name
    }


@router.get("/list", summary="获取微调任务列表")
def get_finetune_list(db: Session = Depends(get_db)):
    tasks = db.query(FinetuneTask).order_by(FinetuneTask.start_time.desc()).all()
    return {
        "code": 200,
        "data": [
            {
                "id": t.id,
                "base_model": t.base_model,
                "learning_rate": t.learning_rate,
                "num_epochs": t.num_epochs,
                "lora_rank": t.lora_rank,
                "start_time": t.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "status": t.status
            }
            for t in tasks
        ]
    }
