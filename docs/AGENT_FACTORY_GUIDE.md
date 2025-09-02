# 🏭 Agent Factory 使用指南

## 概述

Agent Factory 是一個強大的 Pydantic AI agent 自動化建立框架，可在 10-15 分鐘內將簡單需求轉換為完整的、經過測試的 AI agents。

## 🚀 快速開始

### 方法一：使用符號連結（推薦）
```bash
# 快速進入 Agent Factory
cd ~/GitHub/AI/Glaude-Code/agent-factory-project

# 開啟 Claude Code（會自動載入 agent-factory 的 CLAUDE.md）
```

### 方法二：直接進入原始專案
```bash
cd ~/GitHub/AI/context-engineering-intro/use-cases/agent-factory-with-subagents
```

## 📝 使用步驟

### 1. 觸發 Agent 建立
在 Claude Code 中使用以下任一觸發詞：
- "Build an AI agent that..."
- "Create a Pydantic AI agent for..."
- "I need an AI assistant that can..."
- "Make a Pydantic AI agent..."

### 2. 回答澄清問題
系統會詢問 2-3 個問題：
- 主要功能和使用案例
- 偏好的 API 或整合（如適用）
- 輸出格式偏好

### 3. 自動建立流程
系統會自動執行：
1. **Phase 0**: 需求澄清
2. **Phase 1**: 需求文件（pydantic-ai-planner）
3. **Phase 2**: 平行開發
   - 系統提示設計（pydantic-ai-prompt-engineer）
   - 工具整合（pydantic-ai-tool-integrator）
   - 依賴管理（pydantic-ai-dependency-manager）
4. **Phase 3**: 實作
5. **Phase 4**: 驗證測試（pydantic-ai-validator）
6. **Phase 5**: 交付文件

### 4. 產出位置
生成的 agent 會在：
```
agent-factory-project/agents/[your_agent_name]/
├── agent.py           # 主要 agent 邏輯
├── tools.py          # 工具實作
├── settings.py       # 環境設定
├── providers.py      # LLM 提供者
├── dependencies.py   # 依賴注入
├── cli.py           # 命令列介面
├── tests/           # 測試套件
├── planning/        # 規劃文件
└── README.md        # 使用說明
```

## 💡 實際範例

### 簡單 Agent
```
"Build an AI agent that can search the web"
"Create an agent for summarizing documents"
"I need an assistant that can query databases"
```

### 複雜 Agent
```
"Build a customer support agent that integrates with Slack and searches our knowledge base"
"Create a data analysis agent that can query PostgreSQL and generate visualizations"
"Implement a content generation agent with brand voice customization and SEO optimization"
```

### 領域特定 Agent
```
"Build a financial analysis agent that can process earnings reports"
"Create a code review agent that follows our team's style guide"
"Implement a research agent that can search academic papers and summarize findings"
```

## 🔧 執行建立的 Agent

```bash
# 1. 進入 agent 目錄
cd agent-factory-project/agents/your_agent_name/

# 2. 設定環境變數
cp .env.example .env
# 編輯 .env 加入必要的 API keys

# 3. 安裝依賴
pip install -r requirements.txt

# 4. 執行 agent
python cli.py
```

## 📦 必要依賴

建議先安裝以下 Python 套件：
```bash
pip install pydantic-ai pytest asyncpg aiohttp
```

## ⚠️ 注意事項

1. **Context 隔離**：Agent Factory 有自己的 CLAUDE.md，不會影響 Glaude-Code 主環境
2. **工作目錄**：確保在 agent-factory 專案目錄中開啟 Claude Code
3. **API Keys**：某些 agents 可能需要特定的 API keys（如 OpenAI、Anthropic）
4. **Python 版本**：建議使用 Python 3.8 或以上版本

## 🔍 疑難排解

### 問題：找不到 agent-factory 專案
```bash
# 確認符號連結存在
ls -la ~/GitHub/AI/Glaude-Code/agent-factory-project

# 如果不存在，重新建立
ln -s ~/GitHub/AI/context-engineering-intro/use-cases/agent-factory-with-subagents \
      ~/GitHub/AI/Glaude-Code/agent-factory-project
```

### 問題：Agent 建立失敗
- 確保在正確的目錄中開啟 Claude Code
- 檢查是否有足夠的磁碟空間
- 確認 Python 環境設定正確

## 📚 參考資源

- [Agent Factory README](~/GitHub/AI/context-engineering-intro/use-cases/agent-factory-with-subagents/README.md)
- [RAG Agent 範例](~/GitHub/AI/context-engineering-intro/use-cases/agent-factory-with-subagents/agents/rag_agent/)
- [Pydantic AI 文件](https://ai.pydantic.dev/)

## 💬 支援

如有問題，請參考原始專案的文件或在 GitHub 上提出 issue。