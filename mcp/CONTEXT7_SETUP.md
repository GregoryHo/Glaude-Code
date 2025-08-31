# Context7 API Key 配置完成 ✅

## 配置狀態
- **API Key**: 已設定（ctx7sk-...）
- **環境變數**: `CONTEXT7_API_KEY` 已加入 `~/.zshrc`
- **Claude Code**: 已更新配置使用 API key

## 驗證安裝
```bash
# 檢查環境變數
echo $CONTEXT7_API_KEY
# 應顯示: ctx7sk-4871b398-beaf-4635-b53b-8031155f8712

# 檢查 Claude Code 配置
cat ~/.claude.json | grep -A 5 context7
# 應顯示包含 --api-key 參數的配置
```

## 重要步驟
1. **重新載入 shell 配置**（如果開新終端機可跳過）
   ```bash
   source ~/.zshrc
   ```

2. **重啟 Claude Code**
   - 關閉並重新開啟 Claude Code 應用程式
   - API key 會自動從環境變數載入

## 使用方式
在 Claude Code 中，當您詢問關於特定框架或函式庫的問題時，Context7 會自動：
- 獲取最新的官方文檔
- 提供版本特定的程式碼範例
- 確保符合官方最佳實踐

範例提示：
- "use context7 to implement React hooks"
- "use context7 for Vue 3 composition API"
- "use context7 to setup Next.js 14"

## API Key 優勢
有了 API key，您可以：
- ✅ 獲得更高的速率限制
- ✅ 更穩定的服務連接
- ✅ 優先存取最新功能

## 故障排除
如果 Context7 沒有正常運作：
1. 確認環境變數已設定：`echo $CONTEXT7_API_KEY`
2. 確認 Claude Code 已重啟
3. 檢查 MCP 狀態：`python3 mcp/install_mcp.py status`

## 管理 API Key
- **查看 Dashboard**: https://context7.com/dashboard
- **更新 API Key**: 編輯 `~/.zshrc` 並重新執行安裝
- **移除 API Key**: 從 `~/.zshrc` 刪除相關行