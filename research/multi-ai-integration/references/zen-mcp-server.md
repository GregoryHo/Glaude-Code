# zen-mcp-server專案分析
Analysis of zen-mcp-server Project

## 專案概述

**GitHub**: BeehiveInnovations/zen-mcp-server
**描述**: 將Claude Code/GeminiCLI/CodexCLI與多個AI模型整合為一體的MCP伺服器

## 核心概念

### 統一AI協調
```
Claude Code / GeminiCLI / CodexCLI
            ↓
      zen-mcp-server
            ↓
    ┌───────┴───────┐
    │               │
Gemini API    OpenAI API
    │               │
Grok API      OpenRouter
    │               │
Ollama        Custom Models
```

## 主要特性

### 1. 多模型支援
- **雲端模型**: Gemini, OpenAI, Anthropic, Grok
- **路由服務**: OpenRouter (100+ models)
- **本地模型**: Ollama (Llama, Mistral, etc.)
- **自定義模型**: 任何兼容的API

### 2. 智能調度
```javascript
// 智能模型選擇邏輯
function selectModel(task) {
  // 基於任務特性自動選擇
  if (task.requiresLargeContext) {
    return 'gemini-pro'; // 1M tokens
  }
  if (task.requiresDeepReasoning) {
    return 'claude-opus';
  }
  if (task.isSensitive) {
    return 'ollama-local'; // 隱私保護
  }
  return 'gpt-4'; // 預設
}
```

### 3. 上下文管理
- 跨模型的上下文共享
- 自動上下文壓縮
- 歷史記錄追蹤
- 智能摘要生成

## 架構設計

### MCP Server實作
```javascript
class ZenMCPServer {
  constructor() {
    this.models = new Map();
    this.contextManager = new ContextManager();
    this.router = new IntelligentRouter();
  }

  async handleRequest(request) {
    // 1. 分析請求
    const analysis = this.analyzeRequest(request);
    
    // 2. 選擇最佳模型
    const model = this.router.selectModel(analysis);
    
    // 3. 準備上下文
    const context = this.contextManager.prepare(request, model);
    
    // 4. 執行請求
    const response = await this.models.get(model).execute(context);
    
    // 5. 更新上下文
    this.contextManager.update(model, response);
    
    return response;
  }
}
```

### 配置範例
```json
{
  "zen-mcp": {
    "models": {
      "gemini": {
        "enabled": true,
        "apiKey": "${GEMINI_API_KEY}",
        "defaultModel": "gemini-pro-1.5",
        "maxTokens": 1000000
      },
      "openai": {
        "enabled": true,
        "apiKey": "${OPENAI_API_KEY}",
        "defaultModel": "gpt-4-turbo",
        "maxTokens": 128000
      },
      "ollama": {
        "enabled": true,
        "endpoint": "http://localhost:11434",
        "defaultModel": "llama3-70b",
        "maxTokens": 8192
      }
    },
    "routing": {
      "strategy": "cost-optimized",
      "fallbackChain": ["gemini", "openai", "ollama"],
      "contextSharing": true
    }
  }
}
```

## 使用案例

### 1. 多模型代碼審查
```bash
# 啟動多模型審查
zen-mcp review --models "claude,gemini,gpt" --file src/main.js

# 輸出
[Claude]: 架構設計建議...
[Gemini]: 性能優化建議...
[GPT]: 代碼風格建議...
[綜合]: 整合所有建議的最終報告
```

### 2. 大型重構
```bash
# 使用Gemini的大上下文處理整個專案
zen-mcp refactor --model gemini --context-size 1M --project ./

# 自動分割給不同模型
[Gemini]: 分析整體結構（1M tokens）
[Claude]: 設計重構方案
[GPT]: 實施具體改動
```

### 3. 成本優化工作流
```bash
# 配置成本優化模式
zen-mcp config --mode cost-optimized

# 自動路由
簡單任務 → Gemini Flash ($0.75/1M)
複雜任務 → GPT-4 ($10/1M)
關鍵任務 → Claude ($15/1M)
```

## 進階功能

### 1. 工作流程定義
```yaml
# workflows/code-review.yaml
name: comprehensive-code-review
steps:
  - name: initial-scan
    model: gemini-flash
    prompt: "Quick scan for obvious issues"
    
  - name: deep-analysis
    model: claude-opus
    prompt: "Detailed architectural review"
    context: include-previous
    
  - name: security-check
    model: gpt-4
    prompt: "Security vulnerability analysis"
    
  - name: summarize
    model: gemini-pro
    prompt: "Combine all findings"
    context: all-previous
```

### 2. 自定義路由規則
```javascript
// routing-rules.js
module.exports = {
  rules: [
    {
      pattern: /refactor|restructure/i,
      model: 'gemini-pro',
      reason: 'Large context needed'
    },
    {
      pattern: /debug|fix/i,
      model: 'claude-sonnet',
      reason: 'Strong debugging capability'
    },
    {
      pattern: /document|explain/i,
      model: 'gpt-4',
      reason: 'Best natural language'
    }
  ]
};
```

### 3. 成本追蹤
```javascript
// 自動成本計算和報告
const costTracker = {
  track: async (model, tokens) => {
    const cost = calculateCost(model, tokens);
    await db.save({ model, tokens, cost, timestamp: Date.now() });
    
    if (cost > BUDGET_ALERT_THRESHOLD) {
      notify('Budget alert: High cost detected');
      switchToEconomyMode();
    }
  },
  
  report: () => {
    return {
      daily: getDailyCost(),
      byModel: getCostByModel(),
      projection: getMonthlyProjection(),
      savings: getOptimizationSavings()
    };
  }
};
```

## 安裝和設置

### 基本安裝
```bash
# 克隆專案
git clone https://github.com/BeehiveInnovations/zen-mcp-server
cd zen-mcp-server

# 安裝依賴
npm install

# 配置環境變數
cp .env.example .env
# 編輯.env添加API keys

# 啟動服務
npm start
```

### 整合到Claude Code
```json
// ~/.claude.json
{
  "mcpServers": {
    "zen": {
      "command": "node",
      "args": ["/path/to/zen-mcp-server/index.js"],
      "env": {
        "GEMINI_API_KEY": "${GEMINI_API_KEY}",
        "OPENAI_API_KEY": "${OPENAI_API_KEY}",
        "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}"
      }
    }
  }
}
```

## 性能優化

### 並行處理
```javascript
// 同時調用多個模型
async function parallelProcess(prompt) {
  const models = ['claude', 'gemini', 'gpt'];
  const promises = models.map(model => 
    callModel(model, prompt)
  );
  
  const results = await Promise.all(promises);
  return combineResults(results);
}
```

### 快取策略
```javascript
// LRU快取實作
class ModelCache {
  constructor(maxSize = 100) {
    this.cache = new LRUCache(maxSize);
  }
  
  async get(prompt, model) {
    const key = hash(prompt + model);
    
    if (this.cache.has(key)) {
      return this.cache.get(key);
    }
    
    const result = await callModel(model, prompt);
    this.cache.set(key, result);
    return result;
  }
}
```

## 社群貢獻

### 擴展生態系
- 自定義模型適配器
- 工作流程模板庫
- 成本優化策略
- 性能基準測試

### 整合專案
- VS Code擴展
- JetBrains插件
- CLI工具
- Web介面

## 限制和注意事項

### 技術限制
1. 需要穩定的網路連接
2. API rate limits需要管理
3. 本地模型需要足夠硬體資源

### 安全考量
1. API金鑰需要安全存儲
2. 敏感數據路由需要配置
3. 審計日誌建議啟用

### 成本管理
1. 監控API使用量
2. 設置預算上限
3. 定期審查使用報告

## 未來發展

### 計劃功能
- GUI配置介面
- 更多模型支援
- 進階分析儀表板
- 自動化測試套件

### 社群願景
- 成為標準的多AI協調層
- 開放的模型市場
- 共享的工作流程庫

---

*最後更新：2024-12-31*
*基於GitHub專案和社群討論*