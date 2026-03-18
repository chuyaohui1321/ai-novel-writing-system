# AI Novel Writing System

基于 InkOS Agent 的 AI 长篇小说创作系统

## 项目简介

基于开源项目 InkOS Agent，开发的一套**本地部署、可视化操作、全流程闭环**的 AI 长篇小说创作系统，完美支持 500 万字以上超长篇小说创作。

## 技术栈

### 前端
- Vue 3.4.21
- Element Plus 2.6.0
- Vite 5.1.6

### 后端
- Python 3.10.14
- FastAPI 0.110.0
- Uvicorn 0.27.1
- SQLite 3.45.2
- ChromaDB 0.4.24

### 核心能力
- InkOS Agent v0.4.3
- Ollama 0.1.32
- LLaMA Factory 0.8.0

## 功能特性

- 单小说独立工作区、单章节独立目录存储
- 大纲生成、章节生成、内容校对、内容润色全流程
- 不符合要求的内容可基于指令重新生成、定点修改
- 可视化模型配置、多模型分工管理
- 作者训练数据准备、文风学习、LoRA 模型可视化微调
- 7 大真相文件长期记忆、33 维度审计，解决长篇剧情逻辑问题
- 番茄小说端到端发布全流程管理

## 快速开始

### 前置要求

- Windows 11 专业版
- Node.js 18+
- Python 3.10+
- Ollama
- InkOS Agent v0.4.3+
- NVIDIA RTX 4070 12GB

### 安装

```bash
# 克隆项目
git clone <repository-url>

# 安装前端依赖
cd frontend
npm install

# 安装后端依赖
cd ../backend
pip install -r requirements.txt
```

### 运行

```bash
# 启动后端
cd backend
uvicorn main:app --reload

# 启动前端
cd frontend
npm run dev
```

## 项目结构

```
├── frontend/          # 前端项目
│   ├── src/
│   └── package.json
├── backend/          # 后端项目
│   ├── app/
│   └── requirements.txt
└── README.md
```

## 许可证

MIT
