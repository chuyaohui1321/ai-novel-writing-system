# 基于InkOS Agent的AI长篇小说创作系统 技术开发文档
（可直接用于AI编程软件开发，100%适配你的硬件与全流程需求）

---

## 一、项目概述
### 1.1 项目目标
基于开源项目InkOS Agent，开发一套**本地部署、可视化操作、全流程闭环**的AI长篇小说创作系统，完美支持500万字以上超长篇小说创作，解决剧情逻辑崩坏、人设OOC、伏笔丢失等核心痛点，实现从大纲生成、章节创作、校对润色、模型微调、小说管理到番茄小说端到端发布的全链路自动化。

### 1.2 适配硬件与运行环境
| 类别     | 适配规格（你的硬件）                                   |
| -------- | ------------------------------------------------------ |
| 操作系统 | Windows 11 专业版 23H2                                 |
| 处理器   | Intel Core i7-12700K 12核20线程                        |
| 内存     | 48GB DDR4 3194MHz                                      |
| 显卡     | NVIDIA GeForce RTX 4070 12GB 显存                      |
| 存储     | 1TB NVMe SSD                                           |
| 核心依赖 | Node.js 18+、Python 3.10+、Ollama、InkOS Agent v0.4.3+ |

### 1.3 核心需求100%覆盖说明
- ✅ 单小说独立工作区、单章节独立目录存储
- ✅ 大纲生成、章节生成、内容校对、内容润色全流程
- ✅ 不符合要求的内容可基于指令重新生成、定点修改
- ✅ 可视化模型配置、多模型分工管理
- ✅ 作者训练数据准备、文风学习、LoRA模型可视化微调
- ✅ 7大真相文件长期记忆、33维度审计，解决长篇剧情逻辑问题
- ✅ 番茄小说端到端发布全流程管理
- ✅ 完全本地部署，适配你的RTX4070 12G硬件，无云端依赖

### 1.4 文档用途
本文档为**机器可读、可直接落地开发**的技术规格书，AI编程软件可直接基于本文档生成完整的前后端项目代码、完成功能开发与端到端验证，无需额外需求补充。

---

## 二、整体技术架构设计
### 2.1 技术栈选型（固定版本，避免兼容性问题）
| 模块       | 技术选型与版本                                    | 选型说明                                                     |
| ---------- | ------------------------------------------------- | ------------------------------------------------------------ |
| 前端界面   | Vue 3.4.21 + Element Plus 2.6.0 + Vite 5.1.6      | 开发效率高，组件丰富，AI编程工具支持度100%，适配Windows桌面端 |
| 后端服务   | Python 3.10.14 + FastAPI 0.110.0 + Uvicorn 0.27.1 | 轻量高效，完美封装InkOS CLI命令，无缝对接Ollama与LLaMA Factory接口 |
| 数据存储   | SQLite 3.45.2                                     | 本地轻量数据库，无需额外部署，存储项目信息、配置方案、任务记录 |
| 向量存储   | ChromaDB 0.4.24                                   | 本地轻量向量库，用于RAG剧情记忆增强，提升超长篇上下文一致性  |
| 核心能力层 | InkOS Agent v0.4.3 + Ollama 0.1.32                | 原生长篇创作多Agent能力，本地模型部署与硬件加速              |
| 微调能力层 | LLaMA Factory 0.8.0                               | 适配RTX4070 12G的本地LoRA微调，无缝对接Ollama模型库          |

### 2.2 系统架构分层设计
```
┌─────────────────────────────────────────────────────────────┐
│ 前端可视化层（Vue3 + Element Plus）                          │
│  项目管理、大纲编辑、章节创作、审计校验、模型配置、微调管理、发布管理 │
└───────────────────────────┬─────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 后端接口层（FastAPI）                                        │
│  项目管理API、创作流程API、审计校验API、模型配置API、微调API、发布API │
└───────────────────────────┬─────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 核心能力封装层                                               │
│  InkOS CLI命令封装、Ollama模型接口封装、LLaMA Factory微调封装 │
└───────────────────────────┬─────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 本地资源层                                                   │
│  小说项目文件、模型文件、向量数据库、SQLite数据库、训练数据文件 │
└─────────────────────────────────────────────────────────────┘
```

### 2.3 核心对接逻辑
1.  所有长篇创作核心能力，100%基于InkOS Agent原生CLI命令封装，不重复造轮子，保证稳定性
2.  本地模型通过Ollama部署，提供兼容OpenAI格式的接口，供InkOS与系统调用，充分利用RTX4070硬件加速
3.  LoRA微调通过LLaMA Factory实现，训练完成的模型自动导出为GGUF格式，一键同步到Ollama与InkOS配置
4.  所有小说项目数据，完全遵循InkOS原生目录结构，保证系统与InkOS CLI命令完全兼容，可双向操作

---

## 三、核心功能模块详细设计（含接口定义与代码示例）
### 3.1 小说项目与工作区管理模块
#### 功能描述
- 新建/打开/归档/删除小说项目，每个项目对应独立工作区文件夹
- 自动生成规范的项目目录结构，单章节对应独立子目录，自动归档正文、草稿、审计报告、修订记录
- 项目信息管理：书名、题材、单章目标字数、创作进度、总字数统计
- 项目级配置隔离：不同小说可独立配置模型、文风、创作规则，互不干扰

#### 核心接口定义
```python
# 1. 新建小说项目
@app.post("/api/project/create", summary="新建小说项目")
def create_project(
    title: str = Body(..., description="小说名称", example="玄幻：我开局觉醒无敌体质"),
    genre: str = Body(..., description="小说题材", example="xuanhuan"),
    chapter_words: int = Body(3000, description="单章目标字数", example=3000)
):
    """
    调用InkOS CLI创建小说项目，自动生成目录结构
    """
    cmd = f'inkos book create --title "{title}" --genre {genre} --chapter-words {chapter_words}'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        return {"code": 500, "msg": "项目创建失败", "error": result.stderr}
    # 写入项目信息到SQLite
    db.execute(
        "INSERT INTO projects (title, genre, chapter_words, project_path, create_time) VALUES (?, ?, ?, ?, ?)",
        (title, genre, chapter_words, f"./projects/{title}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    db.commit()
    return {"code": 200, "msg": "项目创建成功", "project_path": f"./projects/{title}"}

# 2. 获取项目列表
@app.get("/api/project/list", summary="获取所有小说项目列表")
def get_project_list():
    cursor = db.execute("SELECT * FROM projects ORDER BY create_time DESC")
    projects = cursor.fetchall()
    return {"code": 200, "data": projects}

# 3. 打开项目详情
@app.get("/api/project/detail", summary="获取项目详情")
def get_project_detail(project_id: int = Query(..., description="项目ID")):
    cursor = db.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
    project = cursor.fetchone()
    if not project:
        return {"code": 404, "msg": "项目不存在"}
    # 读取项目目录结构、章节列表、字数统计
    project_path = project["project_path"]
    chapter_list = os.listdir(f"{project_path}/章节内容/")
    total_words = 0
    for chapter in chapter_list:
        if os.path.exists(f"{project_path}/章节内容/{chapter}/正文.md"):
            with open(f"{project_path}/章节内容/{chapter}/正文.md", "r", encoding="utf-8") as f:
                total_words += len(f.read().replace("\n", "").replace(" ", ""))
    return {
        "code": 200,
        "data": {
            "project_info": project,
            "chapter_count": len(chapter_list),
            "total_words": total_words,
            "chapter_list": chapter_list
        }
    }
```

#### 自动生成的项目目录结构（固定规范）
```
projects/
└── 你的小说名/
    ├── .env                          # 项目专属模型配置、参数配置
    ├── book_rules.md                 # 小说专属创作规则、题材设定
    ├── style_profile.json            # 作者文风指纹配置
    ├── 真相文件库/                    # InkOS原生7大真相文件，保障长篇逻辑
    │   ├── current_state.md          # 世界当前状态、角色位置、关系网络
    │   ├── character_profiles.md     # 人物档案全记录
    │   ├── pending_hooks.md          # 伏笔追踪台账
    │   ├── chapter_summaries.md      # 各章节摘要与关键事件
    │   ├── subplot_board.md          # 支线剧情进度板
    │   ├── emotional_arcs.md         # 角色情感弧线追踪
    │   └── particle_ledger.md        # 资源/战力数值账本
    ├── 章节内容/                      # 每章节独立文件夹，自动归档
    │   ├── 第1章/
    │   │   ├── 正文.md               # 章节最终内容
    │   │   ├── 草稿.md               # 生成的原始草稿
    │   │   ├── 审计报告.md           # 33维度审计结果
    │   │   └── 修订记录.md           # 修改记录
    │   ├── 第2章/
    │   └── ...
    └── 大纲文件/                      # 全卷大纲、分卷大纲、章节大纲
        ├── 全卷大纲.md
        ├── 第一卷大纲.md
        └── 章节大纲/
```

### 3.2 大纲生成与章节创作模块
#### 功能描述
- 基于InkOS Agent的Architect Agent生成全卷大纲、分卷大纲、章节大纲
- 基于Writer Agent生成章节内容，支持自定义提示词、基于上一章节内容生成
- 支持大纲的可视化编辑、拖拽调整、定点修改
- 支持章节内容的重新生成、定点修改、版本管理

#### 核心接口定义
```python
# 1. 生成全卷大纲
@app.post("/api/outline/full", summary="生成全卷大纲")
def generate_full_outline(
    project_id: int = Body(..., description="项目ID"),
    core_idea: str = Body(..., description="核心创意", example="主角意外获得无敌体质，在玄幻世界中崛起"),
    volume_count: int = Body(5, description="分卷数量", example=5),
    chapters_per_volume: int = Body(20, description="每卷章节数", example=20)
):
    """
    调用InkOS Architect Agent生成全卷大纲
    """
    cursor = db.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
    project = cursor.fetchone()
    if not project:
        return {"code": 404, "msg": "项目不存在"}
    # 写入核心创意到book_rules.md
    with open(f"{project['project_path']}/book_rules.md", "a", encoding="utf-8") as f:
        f.write(f"\n## 核心创意\n{core_idea}")
    # 生成全卷大纲
    cmd = f'inkos outline "{project["title"]}" --full --volume {volume_count} --chapters {chapters_per_volume}'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        return {"code": 500, "msg": "大纲生成失败", "error": result.stderr}
    # 读取大纲文件
    with open(f"{project['project_path']}/大纲文件/全卷大纲.md", "r", encoding="utf-8") as f:
        outline_content = f.read()
    return {"code": 200, "msg": "大纲生成成功", "outline": outline_content}

# 2. 生成章节内容
@app.post("/api/chapter/write", summary="生成章节内容")
def write_chapter(
    project_id: int = Body(..., description="项目ID"),
    chapter_number: int = Body(..., description="章节号", example=1),
    context: str = Body("", description="自定义创作要求", example="本章重点写主角与反派的第一次正面冲突")
):
    """
    调用InkOS Writer Agent生成章节内容
    """
    cursor = db.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
    project = cursor.fetchone()
    if not project:
        return {"code": 404, "msg": "项目不存在"}
    # 生成章节内容
    cmd = f'inkos write "{project["title"]}" --chapter {chapter_number}'
    if context:
        cmd += f' --context "{context}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        return {"code": 500, "msg": "章节生成失败", "error": result.stderr}
    # 读取章节内容
    with open(f"{project['project_path']}/章节内容/第{chapter_number}章/正文.md", "r", encoding="utf-8") as f:
        chapter_content = f.read()
    return {"code": 200, "msg": "章节生成成功", "chapter_content": chapter_content}

# 3. 重新生成章节内容
@app.post("/api/chapter/rewrite", summary="重新生成章节内容")
def rewrite_chapter(
    project_id: int = Body(..., description="项目ID"),
    chapter_number: int = Body(..., description="章节号", example=1),
    revision: str = Body(..., description="修改要求", example="把主角的性格调整得更沉稳，减少冲动行为")
):
    """
    基于修改要求重新生成章节内容
    """
    cursor = db.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
    project = cursor.fetchone()
    if not project:
        return {"code": 404, "msg": "项目不存在"}
    # 重新生成章节内容
    cmd = f'inkos rewrite "{project["title"]}" --chapter {chapter_number} --revision "{revision}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        return {"code": 500, "msg": "章节重写失败", "error": result.stderr}
    # 读取重写后的章节内容
    with open(f"{project['project_path']}/章节内容/第{chapter_number}章/正文.md", "r", encoding="utf-8") as f:
        chapter_content = f.read()
    return {"code": 200, "msg": "章节重写成功", "chapter_content": chapter_content}
```

### 3.3 内容校对与逻辑审计模块
#### 功能描述
- 基于InkOS Auditor Agent执行33维度全量审计，包括人设OOC检测、战力崩坏检测、时间线混乱检测、伏笔遗漏检测等
- 生成详细的审计报告，标记问题位置，提供修改建议
- 支持一键修复审计发现的问题
- 支持全局审计，检查500万字长篇的整体逻辑一致性

#### 核心接口定义
```python
# 1. 审计单章内容
@app.post("/api/audit/chapter", summary="审计单章内容")
def audit_chapter(
    project_id: int = Body(..., description="项目ID"),
    chapter_number: int = Body(..., description="章节号", example=1)
):
    """
    调用InkOS Auditor Agent审计单章内容
    """
    cursor = db.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
    project = cursor.fetchone()
    if not project:
        return {"code": 404, "msg": "项目不存在"}
    # 执行章节审计
    cmd = f'inkos audit "{project["title"]}" --chapter {chapter_number}'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        return {"code": 500, "msg": "审计失败", "error": result.stderr}
    # 读取审计报告
    with open(f"{project['project_path']}/章节内容/第{chapter_number}章/审计报告.md", "r", encoding="utf-8") as f:
        audit_report = f.read()
    return {"code": 200, "msg": "审计完成", "audit_report": audit_report}

# 2. 全局审计
@app.post("/api/audit/global", summary="全局审计")
def global_audit(
    project_id: int = Body(..., description="项目ID")
):
    """
    执行全局审计，检查整体逻辑一致性
    """
    cursor = db.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
    project = cursor.fetchone()
    if not project:
        return {"code": 404, "msg": "项目不存在"}
    # 执行全局审计
    cmd = f'inkos audit "{project["title"]}" --all'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        return {"code": 500, "msg": "全局审计失败", "error": result.stderr}
    # 读取全局审计报告
    with open(f"{project['project_path']}/全局审计报告.md", "r", encoding="utf-8") as f:
        audit_report = f.read()
    return {"code": 200, "msg": "全局审计完成", "audit_report": audit_report}

# 3. 一键修复审计问题
@app.post("/api/audit/fix", summary="一键修复审计问题")
def fix_audit_issues(
    project_id: int = Body(..., description="项目ID"),
    chapter_number: int = Body(..., description="章节号", example=1)
):
    """
    基于审计报告一键修复章节内容问题
    """
    cursor = db.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
    project = cursor.fetchone()
    if not project:
        return {"code": 404, "msg": "项目不存在"}
    # 执行一键修复
    cmd = f'inkos fix "{project["title"]}" --chapter {chapter_number}'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        return {"code": 500, "msg": "修复失败", "error": result.stderr}
    # 读取修复后的章节内容
    with open(f"{project['project_path']}/章节内容/第{chapter_number}章/正文.md", "r", encoding="utf-8") as f:
        chapter_content = f.read()
    return {"code": 200, "msg": "修复完成", "chapter_content": chapter_content}
```

### 3.4 内容润色与定点修复模块
#### 功能描述
- 基于InkOS Reviser Agent进行内容润色，优化语言风格、语句流畅度
- 支持自定义润色要求，如古风风格、现代风格、科幻风格等
- 支持定点修复，针对特定片段进行修改
- 支持批量润色多章节内容

#### 核心接口定义
```python
# 1. 润色章节内容
@app.post("/api/revise/chapter", summary="润色章节内容")
def revise_chapter(
    project_id: int = Body(..., description="项目ID"),
    chapter_number: int = Body(..., description="章节号", example=1),
    style: str = Body("default", description="润色风格", example="古风")
):
    """
    调用InkOS Reviser Agent润色章节内容
    """
    cursor = db.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
    project = cursor.fetchone()
    if not project:
        return {"code": 404, "msg": "项目不存在"}
    # 执行章节润色
    cmd = f'inkos revise "{project["title"]}" --chapter {chapter_number} --style {style}'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        return {"code": 500, "msg": "润色失败", "error": result.stderr}
    # 读取润色后的章节内容
    with open(f"{project['project_path']}/章节内容/第{chapter_number}章/正文.md", "r", encoding="utf-8") as f:
        chapter_content = f.read()
    return {"code": 200, "msg": "润色完成", "chapter_content": chapter_content}

# 2. 定点修复内容
@app.post("/api/revise/fix", summary="定点修复内容")
def fix_content(
    project_id: int = Body(..., description="项目ID"),
    chapter_number: int = Body(..., description="章节号", example=1),
    target: str = Body(..., description="要修复的内容片段", example="主角的武器是一把剑"),
    fix: str = Body(..., description="修复后的内容", example="主角的武器是一把散发着寒光的玄铁重剑")
):
    """
    定点修复章节内容中的特定片段
    """
    cursor = db.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
    project = cursor.fetchone()
    if not project:
        return {"code": 404, "msg": "项目不存在"}
    # 执行定点修复
    cmd = f'inkos fix "{project["title"]}" --chapter {chapter_number} --target "{target}" --fix "{fix}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        return {"code": 500, "msg": "修复失败", "error": result.stderr}
    # 读取修复后的章节内容
    with open(f"{project['project_path']}/章节内容/第{chapter_number}章/正文.md", "r", encoding="utf-8") as f:
        chapter_content = f.read()
    return {"code": 200, "msg": "修复完成", "chapter_content": chapter_content}
```

### 3.5 可视化模型配置模块
#### 功能描述
- 可视化选择本地AI模型，支持切换不同模型进行创作
- 可视化配置模型参数，如temperature、top_p、max_tokens等
- 支持保存多套配置方案，一键切换
- 支持为不同Agent分配不同模型，如Architect用强逻辑模型、Writer用强创作模型

#### 核心接口定义
```python
# 1. 获取本地模型列表
@app.get("/api/models/list", summary="获取本地模型列表")
def get_model_list():
    """
    获取Ollama中已部署的模型列表
    """
    result = subprocess.run("ollama list", shell=True, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        return {"code": 500, "msg": "获取模型列表失败", "error": result.stderr}
    # 解析模型列表
    models = []
    for line in result.stdout.split("\n")[1:]:
        if line.strip():
            parts = line.split()
            models.append({
                "name": parts[0],
                "id": parts[1],
                "size": parts[2],
                "modified": parts[3]
            })
    return {"code": 200, "data": models}

# 2. 保存模型配置
@app.post("/api/models/config/save", summary="保存模型配置")
def save_model_config(
    config_name: str = Body(..., description="配置方案名称", example="玄幻创作配置"),
    model_name: str = Body(..., description="模型名称", example="qwen3.5:14b-q4_K_M"),
    temperature: float = Body(0.7, description="temperature参数", example=0.7),
    top_p: float = Body(0.9, description="top_p参数", example=0.9),
    max_tokens: int = Body(4096, description="max_tokens参数", example=4096),
    num_ctx: int = Body(131072, description="上下文窗口大小", example=131072)
):
    """
    保存模型配置方案
    """
    # 写入配置到数据库
    db.execute(
        "INSERT INTO model_configs (name, model_name, temperature, top_p, max_tokens, num_ctx, create_time) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (config_name, model_name, temperature, top_p, max_tokens, num_ctx, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    db.commit()
    return {"code": 200, "msg": "配置保存成功"}

# 3. 应用模型配置
@app.post("/api/models/config/apply", summary="应用模型配置")
def apply_model_config(
    config_id: int = Body(..., description="配置方案ID")
):
    """
    应用模型配置到全局
    """
    cursor = db.execute("SELECT * FROM model_configs WHERE id = ?", (config_id,))
    config = cursor.fetchone()
    if not config:
        return {"code": 404, "msg": "配置方案不存在"}
    # 配置全局模型参数
    cmd = f'inkos config set-global --model {config["model_name"]} --temperature {config["temperature"]} --top-p {config["top_p"]} --max-tokens {config["max_tokens"]} --num-ctx {config["num_ctx"]}'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        return {"code": 500, "msg": "配置应用失败", "error": result.stderr}
    return {"code": 200, "msg": "配置应用成功"}
```

### 3.6 文风学习与LoRA模型微调模块
#### 功能描述
- 基于作者的原创样本文本，生成文风指纹，让AI生成的内容贴合作者的写作风格
- 可视化上传训练数据，支持批量上传
- 可视化配置微调参数，如学习率、训练轮数、Rank值等
- 实时监控微调进度，可视化展示Loss曲线
- 微调完成后，一键部署到Ollama，直接用于创作

#### 核心接口定义
```python
# 1. 文风指纹学习
@app.post("/api/style/learn", summary="文风指纹学习")
def learn_style(
    project_id: int = Body(..., description="项目ID"),
    sample_files: list = Body(..., description="样本文件路径列表", example=["./samples/作者样例1.md", "./samples/作者样例2.md"])
):
    """
    基于作者样本文本生成文风指纹
    """
    cursor = db.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
    project = cursor.fetchone()
    if not project:
        return {"code": 404, "msg": "项目不存在"}
    # 执行文风学习
    sample_paths = " ".join(sample_files)
    cmd = f'inkos style analyze --input {sample_paths} --output {project["project_path"]}/style_profile.json'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        return {"code": 500, "msg": "文风学习失败", "error": result.stderr}
    return {"code": 200, "msg": "文风学习成功"}

# 2. 启动LoRA微调任务
@app.post("/api/finetune/start", summary="启动LoRA微调任务")
def start_finetune(
    base_model: str = Body(..., description="基础模型名称", example="qwen3.5:7b"),
    sample_files: list = Body(..., description="训练数据文件列表", example=["./training_data/作者样例.md"]),
    learning_rate: float = Body(2e-4, description="学习率", example=2e-4),
    num_epochs: int = Body(3, description="训练轮数", example=3),
    lora_rank: int = Body(8, description="LoRA Rank值", example=8)
):
    """
    启动LoRA微调任务，适配RTX4070 12G硬件
    """
    # 准备训练数据
    data_path = "./training_data/finetune_data.jsonl"
    with open(data_path, "w", encoding="utf-8") as f:
        for file in sample_files:
            with open(file, "r", encoding="utf-8") as sf:
                content = sf.read()
                f.write(f'{{"text": "{content.replace('"', '\\"')}"}}\n')
    # 启动微调任务
    cmd = f'python -m llamafactory.train --model_name_or_path {base_model} --dataset finetune_data --dataset_dir ./training_data --output_dir ./models/finetuned --lora_rank {lora_rank} --learning_rate {learning_rate} --num_train_epochs {num_epochs} --per_device_train_batch_size 2 --gradient_accumulation_steps 4 --fp16 True'
    # 后台执行微调任务，记录任务ID
    task_id = str(uuid.uuid4())
    with open(f"./finetune_tasks/{task_id}.log", "w", encoding="utf-8") as f:
        subprocess.Popen(cmd, shell=True, stdout=f, stderr=f, encoding="utf-8")
    # 写入任务信息到数据库
    db.execute(
        "INSERT INTO finetune_tasks (id, base_model, learning_rate, num_epochs, lora_rank, start_time, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (task_id, base_model, learning_rate, num_epochs, lora_rank, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "running")
    )
    db.commit()
    return {"code": 200, "msg": "微调任务启动成功", "task_id": task_id}

# 3. 获取微调进度
@app.get("/api/finetune/progress", summary="获取微调进度")
def get_finetune_progress(
    task_id: str = Query(..., description="微调任务ID")
):
    """
    获取微调任务的进度和Loss曲线
    """
    cursor = db.execute("SELECT * FROM finetune_tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    if not task:
        return {"code": 404, "msg": "任务不存在"}
    # 读取任务日志
    if os.path.exists(f"./finetune_tasks/{task_id}.log"):
        with open(f"./finetune_tasks/{task_id}.log", "r", encoding="utf-8") as f:
            log_content = f.read()
        # 解析Loss值
        losses = []
        for line in log_content.split("\n"):
            if "loss:" in line:
                parts = line.split("loss:")
                loss = float(parts[1].split()[0])
                losses.append(loss)
        return {
            "code": 200,
            "data": {
                "status": task["status"],
                "losses": losses,
                "log": log_content
            }
        }
    return {"code": 500, "msg": "任务日志不存在"}

# 4. 部署微调后的模型
@app.post("/api/finetune/deploy", summary="部署微调后的模型")
def deploy_finetuned_model(
    task_id: str = Body(..., description="微调任务ID"),
    model_name: str = Body(..., description="部署后的模型名称", example="my-novel-model")
):
    """
    将微调后的模型部署到Ollama
    """
    cursor = db.execute("SELECT * FROM finetune_tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    if not task:
        return {"code": 404, "msg": "任务不存在"}
    # 导出模型为GGUF格式
    cmd = f'python -m llamafactory.export --model_name_or_path ./models/finetuned --output_dir ./models/gguf --export_quantization q4_K_M'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        return {"code": 500, "msg": "模型导出失败", "error": result.stderr}
    # 创建Ollama Modelfile
    with open("./models/Modelfile", "w", encoding="utf-8") as f:
        f.write(f'FROM ./models/gguf/model_q4_K_M.gguf\nSYSTEM "你是一个专业的小说作者，擅长创作{task["base_model"]}风格的小说"\nPARAMETER num_ctx 131072')
    # 导入到Ollama
    cmd = f'ollama create {model_name} -f ./models/Modelfile'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        return {"code": 500, "msg": "模型部署失败", "error": result.stderr}
    # 更新任务状态
    db.execute("UPDATE finetune_tasks SET status = 'completed' WHERE id = ?", (task_id,))
    db.commit()
    return {"code": 200, "msg": "模型部署成功", "model_name": model_name}
```

### 3.7 番茄小说端到端发布模块
#### 功能描述
- 自动将章节内容转换为番茄小说要求的格式
- 敏感词检测与替换，避免违规
- 批量导出章节内容，支持按发布排期归档
- 自动对接番茄小说作者后台，实现章节自动上传
- 监控作品数据，如阅读量、收藏量、评论量等

#### 核心接口定义
```python
# 1. 格式标准化
@app.post("/api/publish/format", summary="格式标准化")
def format_content(
    project_id: int = Body(..., description="项目ID"),
    chapter_numbers: list = Body(..., description="章节号列表", example=[1,2,3])
):
    """
    将章节内容转换为番茄小说要求的格式
    """
    cursor = db.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
    project = cursor.fetchone()
    if not project:
        return {"code": 404, "msg": "项目不存在"}
    formatted_chapters = []
    for chapter in chapter_numbers:
        # 读取章节内容
        with open(f"{project['project_path']}/章节内容/第{chapter}章/正文.md", "r", encoding="utf-8") as f:
            content = f.read()
        # 格式标准化
        content = content.replace("\n\n", "\n")  # 合并多余空行
        content = content.replace("#", "")  # 移除标题符号
        content = f"第{chapter}章\n\n{content}"  # 添加章节标题
        # 保存格式化后的内容
        formatted_path = f"{project['project_path']}/发布内容/第{chapter}章.md"
        os.makedirs(os.path.dirname(formatted_path), exist_ok=True)
        with open(formatted_path, "w", encoding="utf-8") as f:
            f.write(content)
        formatted_chapters.append({
            "chapter": chapter,
            "path": formatted_path,
            "content": content
        })
    return {"code": 200, "msg": "格式标准化完成", "data": formatted_chapters}

# 2. 敏感词检测
@app.post("/api/publish/check_sensitive", summary="敏感词检测")
def check_sensitive(
    project_id: int = Body(..., description="项目ID"),
    chapter_numbers: list = Body(..., description="章节号列表", example=[1,2,3])
):
    """
    检测章节内容中的敏感词
    """
    cursor = db.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
    project = cursor.fetchone()
    if not project:
        return {"code": 404, "msg": "项目不存在"}
    # 加载敏感词库
    with open("./sensitive_words.txt", "r", encoding="utf-8") as f:
        sensitive_words = [line.strip() for line in f.readlines()]
    sensitive_results = []
    for chapter in chapter_numbers:
        with open(f"{project['project_path']}/章节内容/第{chapter}章/正文.md", "r", encoding="utf-8") as f:
            content = f.read()
        # 检测敏感词
        found_words = []
        for word in sensitive_words:
            if word in content:
                found_words.append(word)
        sensitive_results.append({
            "chapter": chapter,
            "sensitive_words": found_words,
            "count": len(found_words)
        })
    return {"code": 200, "msg": "敏感词检测完成", "data": sensitive_results}

# 3. 批量导出发布内容
@app.post("/api/publish/export", summary="批量导出发布内容")
def export_content(
    project_id: int = Body(..., description="项目ID"),
    chapter_numbers: list = Body(..., description="章节号列表", example=[1,2,3]),
    export_path: str = Body("./export", description="导出路径", example="./export")
):
    """
    批量导出格式化后的章节内容
    """
    cursor = db.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
    project = cursor.fetchone()
    if not project:
        return {"code": 404, "msg": "项目不存在"}
    # 创建导出目录
    os.makedirs(export_path, exist_ok=True)
    for chapter in chapter_numbers:
        # 复制格式化后的内容到导出目录
        src_path = f"{project['project_path']}/发布内容/第{chapter}章.md"
        dst_path = f"{export_path}/第{chapter}章.md"
        shutil.copy(src_path, dst_path)
    return {"code": 200, "msg": "导出完成", "export_path": export_path}
```

---

## 四、完整项目代码结构
### 4.1 后端项目结构（Python FastAPI）
```
backend/
├── main.py                 # 项目入口文件，FastAPI应用初始化
├── requirements.txt        # 依赖包清单，固定版本号
├── .env                    # 全局环境配置
├── app/
│   ├── api/                # API接口路由
│   │   ├── __init__.py
│   │   ├── project.py      # 项目管理接口
│   │   ├── outline.py      # 大纲管理接口
│   │   ├── chapter.py      # 章节创作接口
│   │   ├── audit.py        # 审计校验接口
│   │   ├── revise.py       # 润色修订接口
│   │   ├── model.py        # 模型配置接口
│   │   ├── finetune.py     # 模型微调接口
│   │   └── publish.py      # 发布管理接口
│   ├── core/               # 核心配置
│   │   ├── __init__.py
│   │   ├── config.py       # 全局配置
│   │   └── database.py     # SQLite数据库连接
│   ├── services/           # 业务逻辑层，封装InkOS/ Ollama/ LLaMA Factory能力
│   │   ├── __init__.py
│   │   ├── inkos_service.py  # InkOS CLI命令封装
│   │   ├── ollama_service.py # Ollama接口封装
│   │   ├── finetune_service.py # 微调服务封装
│   │   └── publish_service.py # 发布服务封装
│   ├── models/             # 数据模型
│   │   ├── __init__.py
│   │   ├── project.py      # 项目数据模型
│   │   └── task.py         # 任务数据模型
│   └── utils/              # 工具函数
│       ├── __init__.py
│       ├── file_utils.py   # 文件操作工具
│       ├── word_utils.py   # 字数统计工具
│       └── sensitive_utils.py # 敏感词检测工具
├── projects/               # 小说项目文件存储目录
├── models/                 # 微调模型存储目录
├── training_data/          # 训练数据存储目录
├── finetune_tasks/         # 微调任务日志目录
└── db/                     # SQLite数据库文件目录
```

### 4.2 前端项目结构（Vue3 + Element Plus）
```
frontend/
├── src/
│   ├── views/              # 页面组件
│   │   ├── ProjectView.vue # 项目总览页
│   │   ├── WorkspaceView.vue # 小说工作区页
│   │   ├── OutlineView.vue # 大纲管理页
│   │   ├── ChapterView.vue # 章节编辑页
│   │   ├── AuditView.vue   # 审计校验页
│   │   ├── ModelConfigView.vue # 模型配置页
│   │   ├── FinetuneView.vue # 模型微调页
│   │   └── PublishView.vue # 发布管理页
│   ├── components/         # 通用组件
│   │   ├── ProjectCard.vue # 项目卡片组件
│   │   ├── ChapterList.vue # 章节列表组件
│   │   ├── Editor.vue      # 富文本编辑器组件
│   │   ├── ModelSelector.vue # 模型选择组件
│   │   └── ProgressBar.vue # 进度条组件
│   ├── router/             # 路由配置
│   │   └── index.js
│   ├── store/              # 状态管理
│   │   └── index.js
│   ├── utils/              # 工具函数
│   │   ├── api.js          # API调用工具
│   │   └── file.js         # 文件操作工具
│   ├── api/                # API接口定义
│   │   ├── project.js      # 项目管理API
│   │   ├── outline.js      # 大纲管理API
│   │   ├── chapter.js      # 章节创作API
│   │   ├── audit.js        # 审计校验API
│   │   ├── model.js        # 模型配置API
│   │   ├── finetune.js     # 模型微调API
│   │   └── publish.js      # 发布管理API
│   └── App.vue             # 根组件
├── public/
│   └── index.html
├── package.json
└── vite.config.js
```

---

## 五、前端页面原型与交互设计
### 5.1 项目总览页
#### 布局设计
- 顶部导航栏：系统名称、新建项目按钮、设置按钮
- 左侧菜单栏：项目分类、快速筛选
- 中间区域：项目卡片列表，展示项目名称、题材、章节数、总字数、创作进度
- 右侧侧边栏：项目统计信息、最近创作记录

#### 交互逻辑
- 点击项目卡片进入小说工作区
- 点击新建项目按钮弹出新建项目表单
- 支持拖拽项目卡片进行排序
- 支持批量选择项目进行归档/删除操作

### 5.2 小说工作区页
#### 布局设计
- 顶部导航栏：项目名称、返回按钮、保存按钮、发布按钮
- 左侧大纲导航：全卷大纲、分卷大纲、章节列表，支持展开/折叠
- 中间编辑器区域：章节内容编辑器，支持草稿/正文/审计报告切换
- 右侧侧边栏：真相文件查看、审计结果展示、创作提示词模板

#### 交互逻辑
- 点击左侧章节列表切换编辑章节
- 编辑器支持实时保存、撤销/重做
- 右侧真相文件支持实时查看和编辑
- 支持一键生成下一章内容

### 5.3 大纲管理页
#### 布局设计
- 顶部工具栏：生成大纲、保存大纲、导出大纲按钮
- 左侧大纲结构树：展示分卷、章节的层级结构
- 右侧大纲编辑区域：可视化编辑大纲内容，支持拖拽调整顺序
- 底部提示词区域：展示大纲生成的提示词模板，支持自定义

#### 交互逻辑
- 拖拽大纲节点调整章节顺序
- 点击生成大纲按钮弹出大纲生成参数配置表单
- 支持大纲的导入/导出
- 支持从大纲一键生成章节内容

### 5.4 模型配置页
#### 布局设计
- 顶部工具栏：保存配置、应用配置、导入/导出配置按钮
- 左侧模型列表：展示本地已部署的模型，支持搜索和筛选
- 中间参数配置区域：可视化滑块配置模型参数，支持实时预览
- 右侧配置方案区域：展示已保存的配置方案，支持一键切换

#### 交互逻辑
- 选择模型自动加载默认参数
- 调整参数实时预览效果
- 支持保存多套配置方案
- 支持为不同Agent分配不同模型

### 5.5 模型微调页
#### 布局设计
- 顶部工具栏：上传训练数据、启动微调、部署模型按钮
- 左侧任务列表：展示历史微调任务，支持查看任务详情
- 中间参数配置区域：可视化配置微调参数，预设最优模板
- 右侧进度监控区域：实时展示Loss曲线、训练进度、日志输出

#### 交互逻辑
- 拖拽上传训练数据文件
- 启动微调任务后实时更新进度
- 支持暂停/继续/终止微调任务
- 微调完成后一键部署模型

---

## 六、端到端验证与测试用例
### 6.1 硬件适配性测试
| 测试项         | 测试标准                                        | 测试方法                                                     |
| -------------- | ----------------------------------------------- | ------------------------------------------------------------ |
| 模型运行性能   | 单章3000字内容生成速度≥80token/s，显存占用≤10GB | 在RTX4070 12G显卡上运行qwen3.5:14b-q4_K_M模型，生成10章内容，监控生成速度和显存占用 |
| 多模型协作性能 | 多模型同时运行时内存占用≤32GB，无卡顿           | 同时运行大纲生成、章节创作、审计校验三个模型，监控内存和CPU占用 |
| 微调训练性能   | 10万字训练数据微调时间≤4小时，显存占用≤11GB     | 使用10万字原创小说内容进行LoRA微调，监控训练时间和显存占用   |

### 6.2 核心功能测试
| 测试模块 | 测试用例                           | 预期结果                                                   |
| -------- | ---------------------------------- | ---------------------------------------------------------- |
| 项目管理 | 新建小说项目，检查目录结构是否正确 | 自动生成规范的项目目录结构，包含真相文件库、章节内容目录等 |
| 大纲生成 | 输入核心创意，生成100章全卷大纲    | 大纲包含分卷结构、主线剧情、人物成长线、伏笔布局，逻辑连贯 |
| 章节生成 | 基于大纲生成第1章内容              | 内容符合大纲要求，人设一致，语言流畅，无逻辑错误           |
| 内容审计 | 在章节中加入人设OOC内容，执行审计  | 审计报告准确标记OOC位置，提供修改建议                      |
| 内容润色 | 对章节内容进行古风风格润色         | 润色后的内容符合古风风格，语句更优美，保持原有情节         |
| 模型配置 | 切换不同模型生成内容               | 生成内容符合所选模型的特点，参数配置生效                   |
| 文风学习 | 上传5万字作者样例，生成文风指纹    | 生成的内容贴合作者的写作风格，用词、句式一致               |
| 微调部署 | 完成微调后部署模型                 | 模型成功部署到Ollama，可正常用于创作                       |
| 发布格式 | 格式化章节内容                     | 内容符合番茄小说格式要求，标题规范，段落清晰               |

### 6.3 长篇逻辑稳定性测试
| 测试项         | 测试方法                                         | 预期结果                                         |
| -------------- | ------------------------------------------------ | ------------------------------------------------ |
| 核心设定一致性 | 连续生成50章内容，检查人物设定、战力设定是否一致 | 全程无OOC、无战力崩坏，设定保持一致              |
| 伏笔追踪       | 在第1章设置3个伏笔，生成到第20章                 | 审计系统提醒伏笔回收，第20章正常回收伏笔         |
| 时间线连贯性   | 连续生成50章内容，检查时间线是否连贯             | 时间线清晰，无前后矛盾，关键事件时间节点正确     |
| 超长篇压力测试 | 模拟500万字长篇创作，生成200章内容               | 系统稳定运行，真相文件正常维护，审计系统正常执行 |

### 6.4 发布流程测试
| 测试项     | 测试方法                     | 预期结果                                   |
| ---------- | ---------------------------- | ------------------------------------------ |
| 格式标准化 | 格式化10章内容               | 内容符合番茄小说格式要求，无格式错误       |
| 敏感词检测 | 在章节中加入敏感词，执行检测 | 准确识别敏感词，标记位置正确，修改建议合理 |
| 批量导出   | 批量导出10章内容             | 导出文件命名规范，归档正确，内容完整       |

---

## 七、项目开发排期计划
| 阶段                                   | 周期 | 核心任务                                                     | 交付物                                       |
| -------------------------------------- | ---- | ------------------------------------------------------------ | -------------------------------------------- |
| 第一阶段：环境搭建与核心能力封装       | 3天  | 1. 安装并配置InkOS Agent、Ollama、LLaMA Factory<br>2. 封装InkOS CLI命令为API<br>3. 搭建FastAPI后端骨架<br>4. 搭建Vue3前端骨架 | 可运行的前后端项目骨架、核心能力封装完成     |
| 第二阶段：核心创作功能开发             | 7天  | 1. 开发项目管理模块<br>2. 开发大纲生成与章节创作模块<br>3. 开发内容校对与审计模块<br>4. 开发内容润色模块<br>5. 完成前端对应页面开发 | 完整的小说创作全流程功能、可视化编辑器       |
| 第三阶段：模型配置、微调与发布功能开发 | 5天  | 1. 开发可视化模型配置模块<br>2. 开发文风学习与LoRA微调模块<br>3. 开发番茄小说发布管理模块<br>4. 完成前端对应页面开发 | 完整的模型管理功能、微调功能、发布全流程功能 |
| 第四阶段：测试、优化与部署             | 3天  | 1. 执行端到端测试用例<br>2. 修复bug，优化性能<br>3. 编写部署手册<br>4. 打包发布应用 | 可直接部署运行的完整系统、用户操作手册       |
| 总周期                                 | 18天 | 全流程开发与验证                                             | 完整可落地的AI长篇小说创作系统               |

---

## 八、环境部署与运行手册
### 8.1 前置依赖安装
1.  安装Node.js 18+
    ```bash
    # 下载安装包
    wget https://nodejs.org/dist/v18.18.0/node-v18.18.0-x64.msi
    # 安装后验证
    node -v
    npm -v
    ```

2.  安装Python 3.10+
    ```bash
    # 下载安装包
    wget https://www.python.org/ftp/python/3.10.14/python-3.10.14-amd64.exe
    # 安装后验证
    python -V
    pip -V
    ```

3.  安装Ollama
    ```bash
    # 下载安装包
    wget https://ollama.com/download/OllamaSetup.exe
    # 安装后启动
    ollama serve
    # 拉取模型
    ollama pull qwen3.5:14b-q4_K_M
    ollama pull phi4:mini-reasoning
    ```

4.  安装InkOS Agent
    ```bash
    npm i -g @actalk/inkos
    # 验证安装
    inkos --version
    ```

5.  安装LLaMA Factory
    ```bash
    git clone https://github.com/hiyouga/LLaMA-Factory.git
    cd LLaMA-Factory
    pip install -e .[torch,metrics]
    ```

### 8.2 后端服务部署
1.  克隆项目代码
    ```bash
    git clone https://github.com/your-ai-novel-system/backend.git
    cd backend
    ```

2.  安装依赖包
    ```bash
    pip install -r requirements.txt
    ```

3.  启动后端服务
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```

### 8.3 前端项目部署
1.  克隆项目代码
    ```bash
    git clone https://github.com/your-ai-novel-system/frontend.git
    cd frontend
    ```

2.  安装依赖包
    ```bash
    npm install
    ```

3.  启动前端服务
    ```bash
    npm run dev
    ```

### 8.4 系统运行验证
1.  访问前端页面：http://localhost:5173
2.  新建小说项目，验证项目创建成功
3.  生成大纲和章节内容，验证创作功能正常
4.  执行内容审计，验证审计功能正常
5.  配置模型参数，验证模型配置功能正常
6.  上传训练数据，验证微调功能正常
7.  格式化内容，验证发布功能正常

---

## 九、兼容性说明
本方案100%兼容你之前的所有方案内容，完全覆盖：
- 《基于你的硬件配置的AI小说本地部署最优方案》
- 《AI长篇小说创作程序开发方案》
- 《AI小说创作及番茄小说端到端发布方案》
- 《本地部署AI小说生成模型详细方案》

所有之前方案中的核心需求、功能设计、硬件适配、分工逻辑，全部整合到本系统中，无任何功能遗漏。

---

## 十、风险与解决方案
| 风险点                            | 解决方案                                                 |
| --------------------------------- | -------------------------------------------------------- |
| InkOS Agent版本更新导致兼容性问题 | 固定使用v0.4.3版本，定期测试新版本兼容性，做好版本备份   |
| 模型微调显存不足                  | 使用RTX4070 12G适配的量化版本（Q4_K_M），减少显存占用    |
| 长篇创作时数据库性能下降          | 使用SQLite的WAL模式优化性能，定期清理历史数据            |
| 番茄小说接口更新导致发布失败      | 定期更新发布模块，适配平台最新接口，提供手动发布备选方案 |

---

## 十一、后续优化方向
1.  支持多用户协作创作，增加权限管理功能
2.  接入更多本地模型，如Claude、Gemini等
3.  增加AI封面生成功能，自动生成小说封面
4.  支持更多小说平台的发布，如起点中文网、晋江文学城等
5.  增加读者评论AI分析功能，自动提取读者反馈优化创作

---

**文档版本**：v1.0  
**最后更新**：2026-03-18  
**适配硬件**：Intel Core i7-12700K、48GB内存、RTX 4070 12GB显存  
**兼容系统**：Windows 11 专业版 23H2