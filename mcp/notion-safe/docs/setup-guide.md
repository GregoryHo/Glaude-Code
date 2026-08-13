# Notion MCP Wrapper 設定指南

本指南協助您設定 Notion MCP Wrapper，為 Claude Code 提供安全的 Notion API 整合。

## 🎯 選擇安裝方式

### 方式 A：使用 Wrapper（推薦）
提供操作限流、日誌記錄等安全功能。適合需要額外保護的環境。

### 方式 B：直接使用官方 Server
最簡單的設定方式，適合個人使用。

---

## 方式 A：安裝 Notion MCP Wrapper（推薦）

提供操作限流、日誌記錄等安全功能。適合需要額外保護的環境。

### 步驟 1：前置需求
```bash
# 安裝依賴套件（包含官方 Notion MCP Server）
cd mcp/notion
npm install
```

### 步驟 2：取得 Notion API Key
1. 前往 https://www.notion.so/my-integrations
2. 建立新的 Integration（例如："Claude Code Safe"）
3. 複製 Internal Integration Token

### 步驟 3：自動安裝
```bash
# 進入專案目錄
cd mcp/notion

# 執行安裝腳本
./scripts/setup-wrapper.sh
```

### 步驟 4：手動安裝（如自動安裝失敗）
```bash
# 1. 安裝依賴（如尚未安裝）
cd mcp/notion
npm install

# 2. 設定執行權限
chmod +x src/notion-mcp-wrapper.js

# 3. 設定環境變數 (加入 ~/.bash_profile 或 ~/.zshrc)
export NOTION_TOKEN="your_api_key_here"

# 4. 配置 Claude Code
claude mcp add notion-safe "$(pwd)/src/notion-mcp-wrapper.js"
```

### 步驟 5：驗證安裝
```bash
# 1. 檢查 MCP 狀態
claude mcp list

# ✅ 預期結果：
# notion-safe: /path/to/notion-mcp-wrapper.js - ✓ Connected
# ❌ 不會顯示 notion（Wrapper 在內部呼叫官方 Server）

# 2. 確認官方 Server 已安裝（Wrapper 的依賴）
ls node_modules/.bin/notion-mcp-server
# ✅ 預期結果：node_modules/.bin/notion-mcp-server 存在
# 備註：Wrapper 會自動尋找本地、專案或全域安裝的 Server

# 3. 測試 Notion API 連接
# 在 Claude Code 中測試：
# - 開啟新的 Claude Code session
# - 詢問 "Can you search for pages in my Notion workspace?"
# ✅ 預期結果：Claude 使用 mcp__notion-safe__API-post-search 工具
# ⚠️ 注意：工具名稱是 notion-safe 而非 notion

# 4. 檢查操作日誌（Wrapper 獨有功能）
ls -la mcp/notion/logs/
# ✅ 預期結果：看到 operations-YYYY-MM-DD.jsonl 檔案

# 5. 測試日誌記錄
# 執行任何 Notion 操作後：
tail -f mcp/notion/logs/operations-$(date +%Y-%m-%d).jsonl
# ✅ 預期結果：看到 JSON 格式的操作記錄
```

### 步驟 6：授權 Notion 頁面
1. 在 Notion 開啟要分享的頁面
2. 點擊右上角 **Share**
3. 選擇你建立的 Integration
4. 給予存取權限

---

## 方式 B：直接使用官方 Server

最簡單的設定方式，適合個人使用。沒有額外的安全層，直接使用官方 API。

### 步驟 1：安裝官方 Server
```bash
# 選項 A：全域安裝（傳統方式）
npm install -g @notionhq/notion-mcp-server --registry https://registry.npmjs.org

# 選項 B：本地安裝（推薦）
cd mcp/notion
npm install @notionhq/notion-mcp-server
```

### 步驟 2：取得 Notion API Key
1. 前往 https://www.notion.so/my-integrations
2. 建立新的 Integration（例如："Claude Code"）
3. 複製 Internal Integration Token

### 步驟 3：配置 Claude Code
```bash
claude mcp add notion /usr/local/bin/notion-mcp-server \
  --scope user \
  -e NOTION_API_KEY=your_api_key_here
```

### 步驟 4：授權 Notion 頁面
1. 在 Notion 開啟要分享的頁面
2. 點擊右上角 **Share**
3. 選擇你建立的 Integration
4. 給予存取權限

### 步驟 5：驗證連接
```bash
# 1. 檢查 MCP 狀態
claude mcp list

# ✅ 預期結果：
# notion: /usr/local/bin/notion-mcp-server - ✓ Connected
# ❌ 不會顯示 notion-safe（只有官方 Server）

# 2. 測試 Notion API 連接
# 在 Claude Code 中測試：
# - 開啟新的 Claude Code session
# - 詢問 "Can you search for pages in my Notion workspace?"
# ✅ 預期結果：Claude 使用 mcp__notion__API-post-search 工具
# ⚠️ 注意：工具名稱是 notion 而非 notion-safe

# 3. 確認沒有日誌功能（官方版本限制）
ls -la mcp/notion/logs/
# ❌ 預期結果：目錄不存在或沒有新的日誌檔案
# ⚠️ 官方版本不提供操作日誌功能
```

---

## 配置詳解

### MCP 配置檔位置
- User 層級：`~/.claude.json`
- Project 層級：`.mcp.json`

### 配置結構
```json
{
  "mcpServers": {
    "notion": {
      "command": "/usr/local/bin/notion-mcp-server",
      "args": [],
      "env": {
        "NOTION_API_KEY": "ntn_xxx..."
      }
    }
  }
}
```

## 管理命令

```bash
# 列出所有 MCP servers
claude mcp list

# 查看特定 server 設定
claude mcp get notion

# 移除 server
claude mcp remove notion

# 重新添加（更新 API Key）
claude mcp add notion /usr/local/bin/notion-mcp-server \
  --scope user \
  -e NOTION_API_KEY=new_api_key
```

## 安全建議

1. **API Key 管理**
   - 不要將 API Key 提交到版本控制
   - 定期更換 API Key
   - 使用環境變數儲存敏感資訊

2. **權限控制**
   - 只授權必要的 Notion 頁面
   - Notion Integration 預設不支援刪除操作
   - 建立專屬的 Claude Work Zone

3. **隔離策略**
   - 建立專屬工作區域
   - 重要文件使用唯讀權限
   - 定期審查存取記錄

## 📋 常見問題

### Q1: Wrapper 和官方 Server 的差異？
| 功能 | Wrapper (notion-safe) | 官方 Server (notion) |
|------|----------------------|---------------------|
| 操作限流 | ✅ 100 ops/hour | ❌ 無限制 |
| 操作日誌 | ✅ JSON 格式記錄 | ❌ 無記錄 |
| API 相容性 | ✅ 100% 相容 | ✅ 原生 API |
| 設定複雜度 | 中等 | 簡嗮 |

### Q2: 連接失敗怎麼辦？
```bash
# 1. 檢查 MCP 服務狀態
claude mcp list

# 2. 檢查 API Key（Wrapper 使用）
echo $NOTION_TOKEN

# 3. 檢查 API Key（官方 Server）
claude mcp get notion

# 4. 重新配置
claude mcp remove notion-safe  # 或 notion
# 然後重新執行安裝步驟
```

### Q3: npm 安裝失敗？
```bash
# 使用官方 registry
npm install -g @notionhq/notion-mcp-server --registry https://registry.npmjs.org

# 檢查 npm 權限
sudo npm install -g @notionhq/notion-mcp-server

# 確認安裝路徑
which notion-mcp-server
npm config get prefix
```

### Q4: 如何切換兩種模式？
```bash
# 從官方切換到 Wrapper
claude mcp remove notion
cd mcp/notion && ./scripts/setup-wrapper.sh

# 從 Wrapper 切換到官方
claude mcp remove notion-safe
claude mcp add notion /usr/local/bin/notion-mcp-server \
  --scope user \
  -e NOTION_API_KEY=your_key
```

### Q5: 日誌檔案在哪裡？
```bash
# Wrapper 日誌位置
ls -la mcp/notion/logs/

# 查看今天的操作
cat mcp/notion/logs/operations-$(date +%Y-%m-%d).jsonl | jq '.'
```

## 🔧 進階設定

### 調整 Wrapper 限流
```bash
# 設定環境變數
export MAX_OPERATIONS_PER_HOUR=200  # 調整為需要的值

# 重啟 Claude Code 使設定生效
```

## 📞 取得協助

- 查看 [README](../README.md) 了解功能概覽
- 查看 [安全指南](security-guide.md) 了解安全架構
- 本專案為本地工具，相關問題請參考文件自行解決

## 版本資訊
- Notion MCP Server: @notionhq/notion-mcp-server v1.9.0
- 維護者：Notion 官方團隊 (@makenotion.com)
- Wrapper: 本地安全層實作