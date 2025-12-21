# GA 项目 - Git助手

一个集成 AI 模型的 Git 工作流增强工具库，包含自动化周报生成和智能提交信息生成功能。

## 📋 项目概述

本项目提供两个主要功能：

1. **周报生成器** (`generate_weekly_report.py`) - 使用 DeepSeek AI 模型自动生成项目开发周报
2. **提交信息生成器** (`prepare-commit-msg.py`) - 使用本地 Ollama 模型生成中文提交信息

## ✨ 功能特性

### 1. 自动生成周报
- 扫描过去 N 天的 Git 提交记录
- 调用 DeepSeek API 进行智能分析和总结
- 自动分类为三个维度：
  - **Feature Highlights** - 功能亮点
  - **Bug Fixes** - 问题修复
  - **Refactoring** - 代码重构
- 生成专业的 Markdown 格式文档

### 2. 智能提交信息生成
- 基于本次提交的 `git diff` 内容
- 调用本地 Ollama 模型生成中文提交信息
- 自动保存到 Git prepare-commit-msg Hook

## 🚀 快速开始

### 环境要求

- Python 3.x
- Git
- OpenAI Python 库: `pip install openai`
- 环境变量: `DEEPSEEK_API_KEY`

### 安装步骤

```bash
# 1. 克隆或复制项目
cd your_project_path

# 2. 安装依赖
pip install openai python-dotenv

# 3. 配置 API Key
# 在项目根目录创建 .env 文件
echo "DEEPSEEK_API_KEY=your_api_key_here" > .env
```

### 使用方法

#### 生成周报

```bash
python generate_weekly_report.py
```

这将：
1. 扫描过去 7 天的 Git 提交记录
2. 发送给 DeepSeek API 进行分析
3. 生成 `WEEKLY_REPORT.md` 文件

#### 自动生成提交信息

将 `prepare-commit-msg.py` 安装为 Git Hook：

```bash
# 复制到 .git/hooks 目录
cp prepare-commit-msg.py .git/hooks/prepare-commit-msg
chmod +x .git/hooks/prepare-commit-msg
```

使用前需要启动 Ollama：
```bash
ollama serve
```

然后正常提交：
```bash
git add .
git commit
```

脚本会自动调用 AI 生成中文提交信息。（如果觉得不准确，可以在弹出的文件中修改提交信息）

## 📁 项目结构

```
GA/
├── generate_weekly_report.py      # 周报生成脚本
├── prepare-commit-msg.py          # Git Hook 提交信息生成脚本
├── README.md                      # 项目文档
└── WEEKLY_REPORT.md               # 生成的周报（运行后产生）
```

## 🔧 配置详情

### DeepSeek API 配置

```python
API_KEY = os.getenv("DEEPSEEK_API_KEY")
BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-chat"
```

### Ollama 本地模型配置

```json
{
  "model": "yourmodel", // 修改为你所使用的模型
  "api_url": "http://localhost:11434/api/generate",
  "timeout": 15  // 秒
}
```

## 🛠️ 其他用法

### 自定义周报时间范围

修改 `generate_weekly_report.py` 中的参数：

```python
logs = get_git_logs(days=14)  # 改为 14 天
```

### 自定义提交信息生成提示词

在 `prepare-commit-msg.py` 中修改 prompt 字符串，调整 AI 的行为。

## 📝 注意事项

- **DeepSeek API**: 需要有效的 API Key，首次调用需要联网
- **Ollama 本地模型**: 需要提前下载相应模型，调用时需保持服务运行
- **Windows 环保**: `prepare-commit-msg.py` 已处理 UTF-8 编码问题，支持中文输出
- **Git 仓库**: 两个脚本都需要在 Git 仓库内运行

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 支持

如遇问题，请检查：
1. API Key 是否正确配置
2. 是否在 Git 仓库目录内
3. 网络连接是否正常（DeepSeek API）
4. Ollama 服务是否正确启动（Git Hook）
