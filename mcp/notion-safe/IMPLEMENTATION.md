# Notion MCP Integration 實作文件

## 📋 專案背景與需求

### 原始需求
使用者需要 Claude Code 協助**大量讀取、整理、寫入** Notion 內容，但擔心：
1. 誤改重要資料
2. 程式錯誤導致大量錯誤操作
3. 無法追蹤 Claude 做了什麼

### 核心訴求
- **安全性**：避免災難性錯誤
- **便利性**：保留完整 Notion 功能
- **可追蹤**：知道所有操作記錄

## 🏗️ 架構設計決策

### 為什麼不直接用官方 MCP Server？

**官方 @notionhq/notion-mcp-server 的問題：**
- ❌ 可以存取所有授權頁面（無區域限制）
- ❌ 沒有操作限流（可能失控）
- ❌ 沒有操作日誌（不知道做了什麼）

**但官方的優點：**
- ✅ 功能完整且穩定
- ✅ 官方維護，持續更新
- ✅ 實作了完整 MCP 協議

### 為什麼採用 Wrapper 模式？

**初始考慮的方案：**
1. ❌ **完全自製 MCP Server** - 太複雜，難維護
2. ❌ **只用官方** - 缺乏安全控制
3. ✅ **Wrapper 模式** - 平衡的方案

**最終實作的 Wrapper 架構：**
```
Claude Code
    ↓ [呼叫 MCP API]
notion-mcp-wrapper.js (作為 MCP Server)
    ├── 接收 MCP 請求
    ├── 執行安全檢查（限流、區域、日誌）
    └── spawn 官方 notion-mcp-server 作為子進程
            ↓
        Notion API
```

**關鍵理解**：Wrapper 本身就是一個 MCP Server，它會啟動官方 MCP 作為子進程

- 保留官方所有功能
- 加入必要的安全檢查
- 官方更新時自動獲益
- 實作簡單，易維護

### 為什麼簡化安全功能？

**Notion 已提供的保護：**
- ✅ 版本歷史（可回溯 30 天）
- ✅ Integration 無法永久刪除
- ✅ 頁面級權限控制

**我們只需要補充：**
1. **操作限流** - Notion 沒有的
2. **操作日誌** - 方便審計
3. **區域隔離** - 額外的安全層（可選）

## 💻 技術實作細節

### 1. Wrapper 運作原理

```javascript
// notion-mcp-wrapper.js 核心邏輯

1. 啟動官方 MCP Server 作為子進程
2. 攔截來自 Claude 的請求
3. 如果是寫入操作：
   - 檢查操作頻率（防失控）
   - 檢查目標區域（如果啟用）
   - 記錄操作日誌
4. 通過檢查則轉發給官方 MCP
5. 將回應傳回給 Claude
```

### 2. 關鍵安全檢查

**操作限流：**
```javascript
// 預設 100 次/小時
// 防止程式錯誤導致無限循環寫入
if (recentOps.length >= MAX_OPS_PER_HOUR) {
  return { allowed: false, reason: "Rate limit exceeded" }
}
```

**區域隔離（可選）：**
```javascript
// 如果設定了 NOTION_CLAUDE_ZONE_ID
// 確保所有操作都在這個區域內
if (targetId !== claudeZoneId && !isChildOf(targetId, claudeZoneId)) {
  return { allowed: false, reason: "Outside Claude Zone" }
}
```

### 3. 環境變數設計

```bash
# 必要設定
NOTION_TOKEN=xxx              # Notion API Token

# 可選的安全設定
NOTION_CLAUDE_ZONE_ID=xxx    # 限制操作區域
MAX_OPERATIONS_PER_HOUR=100  # 操作限流
STRICT_ZONE_CHECK=false      # 是否強制區域檢查
LOG_TO_FILE=true             # 記錄操作日誌
```

## 📦 檔案結構說明

```
mcp/notion-safe/
├── src/
│   ├── notion-mcp-wrapper.js    # 核心 Wrapper
│   ├── safe-wrapper.js          # (已廢棄) 原本的完整替代方案
│   └── *.js                     # 其他嘗試的版本
├── scripts/
│   ├── setup-wrapper.sh         # 主要安裝腳本
│   └── *.sh                     # 其他版本的腳本
├── .env.example                  # 環境變數範本
└── logs/                         # 操作日誌目錄
```

## 🚀 部署步驟

### 步驟 1：安裝依賴
```bash
# 安裝官方 Notion MCP Server
npm install -g @notionhq/notion-mcp-server

# 確認安裝成功
which notion-mcp-server
```

### 步驟 2：設定環境變數

```bash
# 將 NOTION_TOKEN 加入 .bash_profile 或 .zshrc
echo 'export NOTION_TOKEN="your_notion_token_here"' >> ~/.bash_profile
source ~/.bash_profile

# 驗證環境變數
echo $NOTION_TOKEN
```

### 步驟 3：準備 Wrapper（可選的安全層）

```bash
# 設定執行權限
cd mcp/notion-safe
chmod +x src/notion-mcp-wrapper.js

# 建立環境設定檔（選擇性，wrapper 會自動讀取）
cat > .env << EOF
NOTION_TOKEN=$NOTION_TOKEN
MAX_OPERATIONS_PER_HOUR=100
STRICT_ZONE_CHECK=false
LOG_TO_FILE=true
NOTION_CLAUDE_ZONE_ID=  # 選填，限制操作區域
EOF
```

### 步驟 4：配置 Claude Code

您可以根據需求配置一個或兩個 MCP servers：

#### 配置官方 MCP Server（基礎使用）
```bash
claude mcp add notion /usr/local/bin/notion-mcp-server \
  --scope user \
  -e NOTION_TOKEN=$NOTION_TOKEN
```

#### 配置安全 Wrapper（大量操作時使用）
```bash
# 從 repo 根目錄執行
claude mcp add notion-safe "$(pwd)/mcp/notion-safe/src/notion-mcp-wrapper.js" \
  --scope user \
  -e NOTION_TOKEN=$NOTION_TOKEN \
  -e MAX_OPERATIONS_PER_HOUR=100 \
  -e STRICT_ZONE_CHECK=false \
  -e LOG_TO_FILE=true
```

**建議**：同時配置兩個，使用不同名稱（notion 和 notion-safe），這樣您可以：
- 使用 `notion` 進行日常讀取和簡單操作
- 使用 `notion-safe` 進行大量批次操作（有限流和日誌保護）

### 步驟 5：驗證安裝

```bash
# 查看已配置的 MCP servers
claude mcp list

# 應該看到（根據您的配置）：
# notion: /usr/local/bin/notion-mcp-server - ✓ Connected
# notion-safe: /path/to/notion-mcp-wrapper.js - ✓ Connected
```

**注意事項**：
- 官方 notion-mcp-server 是必要的基礎元件
- Wrapper 是可選的安全層，它會調用官方 server
- NOTION_TOKEN 必須設定（從環境變數或 -e 參數傳入）

## 🎯 使用場景

### 場景 1：日常使用
- 讀取和整理文件
- 更新少量頁面
- 建立報告

**設定：**
- 使用基本配置
- 依賴 Notion 權限控制
- 不需要區域限制

### 場景 2：大量資料處理
- 批量更新數百個頁面
- 資料庫重組
- 自動化工作流程

**設定：**
- 啟用嚴格區域檢查
- 提高操作限制（如 500/小時）
- 所有操作都在 Claude Zone 內

### 場景 3：測試和開發
- 測試新功能
- 開發自動化腳本

**設定：**
- 使用獨立的測試 Integration
- 設定更低的操作限制
- 只授權測試頁面

## ⚠️ 重要考量

### 安全性考量
1. **API Key 管理**：永遠不要提交到 Git
2. **權限最小化**：只授權必要的頁面
3. **定期審計**：檢查 logs/ 目錄的操作記錄
4. **測試先行**：重要操作先在測試區驗證

### 效能考量
1. **操作限流**：預設 100/小時，可依需求調整
2. **日誌大小**：定期清理舊日誌
3. **子進程管理**：Wrapper 會正確處理信號

### 維護考量
1. **官方更新**：定期更新 @notionhq/notion-mcp-server
2. **日誌輪替**：實作日誌自動清理（如需要）
3. **監控告警**：可加入異常操作通知

## 🔄 版本歷程

### v1：完全替代方案
- 嘗試完全自製 MCP Server
- 太複雜，難以維護
- **已廢棄**

### v2：Wrapper 模式（當前）
- 包裝官方 MCP Server
- 加入安全檢查層
- 平衡安全與功能
- **推薦使用**

## 📝 未來改進方向

1. **更智能的區域檢查**
   - 快取頁面層級關係
   - 減少 API 調用

2. **操作審計報表**
   - 自動生成日報/週報
   - 異常操作告警

3. **配置管理介面**
   - Web UI 查看操作記錄
   - 動態調整限制

## 🤝 給未來實作者的建議

1. **保持簡單**：不要過度設計，Notion 已有很多保護
2. **專注核心**：限流和日誌是最重要的
3. **測試優先**：先在小範圍測試
4. **漸進部署**：先用基本模式，需要時才啟用嚴格模式
5. **保留彈性**：環境變數配置，不要寫死

## 📞 問題排查

### Wrapper 沒有攔截操作？
- 檢查是否正確配置 Claude Code
- 確認使用 wrapper 路徑而非原生 MCP

### 操作被拒絕？
- 檢查 logs/ 目錄查看原因
- 可能是超過限流或區域限制

### 官方 MCP 更新後不相容？
- Wrapper 設計為透明代理，應該自動相容
- 如有問題，檢查 MCP 協議是否有變更

---

*最後更新：2024-01-30*
*作者：Gregory & Claude Code*