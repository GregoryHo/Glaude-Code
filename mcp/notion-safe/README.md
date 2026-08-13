# Notion MCP Integration for Claude Code

一個安全的 Notion API 整合層，為 Claude Code 提供限流保護和操作日誌功能。

## 🎯 功能特點

- **安全保護**：操作限流防止失控的大量操作
- **完整日誌**：記錄所有寫入操作供審計追蹤
- **簡單設定**：一鍵安裝腳本，5 分鐘完成設定
- **透明操作**：完全相容官方 Notion MCP Server API
- **專案隔離**：日誌儲存在各自專案目錄，不污染框架

## 🏗️ 架構設計

```
Claude Code
    ↓
Notion MCP Wrapper (安全層)
    ├── 操作限流 (預設 100 ops/hour)
    └── 操作日誌 (JSON 格式)
    ↓
Official Notion MCP Server
    ↓
Notion API
```

## 📁 專案結構

```
mcp/notion/
├── README.md              # 本文件
├── .env.example           # 環境變數範本
├── docs/              
│   ├── security-guide.md  # 安全架構指南
│   └── setup-guide.md     # 詳細設定指南
├── scripts/           
│   └── setup-wrapper.sh   # 安裝設定腳本
├── src/               
│   └── notion-mcp-wrapper.js  # MCP 安全包裝器
└── logs/                  # 操作日誌 (自動建立)
```

## 🚀 快速開始

### 前置需求
- Node.js 18+ 
- Claude Code CLI
- Notion 帳號與工作區

### 步驟 1：取得 Notion API Key
1. 前往 [Notion Integrations](https://www.notion.so/my-integrations)
2. 點擊「New integration」建立新的整合
3. 複製 Internal Integration Token

### 步驟 2：自動安裝（推薦）
```bash
# 進入專案目錄
cd mcp/notion

# 執行安裝腳本
./scripts/setup-wrapper.sh
```

腳本會自動：
- 安裝官方 Notion MCP Server
- 設定執行權限
- 配置 Claude Code
- 驗證連接狀態

### 步驟 3：手動安裝（如需要）
```bash
# 1. 安裝依賴（本地安裝）
cd mcp/notion
npm install

# 2. 設定執行權限
chmod +x src/notion-mcp-wrapper.js

# 3. 設定環境變數（在專案的 .env 檔案中）
echo 'NOTION_TOKEN="your_api_key_here"' >> .env
echo 'NOTION_LOG_DIR="/path/to/project/.notion-logs"' >> .env

# 4. 配置 Claude Code
claude mcp add notion-safe "$(pwd)/src/notion-mcp-wrapper.js"

# 5. 驗證連接
claude mcp list
```

## 🔒 安全功能

| 功能 | 說明 | 預設值 |
|------|------|--------|
| **操作限流** | 防止失控的大量操作 | 100 次/小時 |
| **操作日誌** | JSON 格式記錄所有寫入操作 | 啟用 |
| **錯誤處理** | 優雅處理 API 錯誤和逾時 | 啟用 |

## 📊 使用範例

### 在 Claude Code 中使用
```
// 使用 notion-safe MCP（有安全保護）
mcp__notion-safe__API-get-self

// 查詢資料庫
mcp__notion-safe__API-post-database-query
```

### 檢查操作日誌
```bash
# 日誌現在儲存在專案目錄
# 查看今天的操作
cat .notion-logs/operations-$(date +%Y-%m-%d).jsonl | jq '.'

# 統計操作類型
cat .notion-logs/operations-*.jsonl | jq '.method' | sort | uniq -c
```

## 🛠️ 設定選項

| 環境變數 | 說明 | 預設值 |
|----------|------|--------|
| `NOTION_TOKEN` | Notion API Key | 必填 |
| `NOTION_LOG_DIR` | 日誌儲存目錄 | `./.notion-logs` |
| `MAX_OPERATIONS_PER_HOUR` | 每小時操作上限 | 100 |
| `LOG_TO_FILE` | 是否記錄到檔案 | true |

## 📚 延伸閱讀

- [安全指南](docs/security-guide.md) - 深入了解安全架構
- [設定指南](docs/setup-guide.md) - 詳細設定步驟
- [實作文件](IMPLEMENTATION.md) - 技術實作細節

## ⚠️ 重要提醒

1. **保護 API Key**：永遠不要將 API Key 提交到版本控制
2. **定期檢查日誌**：監控異常操作模式
3. **最小權限原則**：只授權必要的頁面給 Integration
4. **測試優先**：重要操作前先在測試頁面驗證

## 🤝 支援

遇到問題？請查看：
- [常見問題](docs/setup-guide.md#常見問題)
- [設定指南](docs/setup-guide.md) 詳細說明

## 📄 專案說明

- 本專案為 Notion MCP Server 的本地安全包裝層
- 基於官方 @notionhq/notion-mcp-server v1.9.0
- 為個人使用的本地工具，非公開專案