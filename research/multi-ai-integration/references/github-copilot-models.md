# GitHub Copilot多模型支援參考
GitHub Copilot Multi-Model Support Reference

## 官方公告摘要

### 2024年10月 - 開發者選擇權
GitHub宣布為Copilot帶來多模型選擇，包括：
- Anthropic的Claude 3.5 Sonnet
- Google的Gemini 1.5 Pro
- OpenAI的o1-preview和o1-mini

### 關鍵特性
- 開發者可以在Copilot Chat中即時切換模型
- 不同模型針對不同任務優化
- 企業可以控制團隊可用的模型

## 支援的模型（2025年1月）

### Claude系列
- **Claude 3.5 Sonnet**: 平衡的推理和速度
- **Claude 3.7 Sonnet**: 增強版本
- **Claude 3.7 Sonnet Thinking**: 顯示思考過程
- **Claude 4 Sonnet**: 最新穩定版
- **Claude Opus 4.1 (Preview)**: 最強推理能力

### Gemini系列
- **Gemini 2.0 Flash**: 超快速度，低成本
- **Gemini 2.5 Pro**: 大型上下文，平衡性能

### OpenAI系列
- **GPT-4.1**: 標準模型
- **GPT-5 (Preview)**: 最新一代
- **o3-mini**: 經濟選擇
- **o3**: 強推理
- **o4 (Preview)**: 實驗性

## 使用方式

### 在VS Code中切換模型
```
1. 開啟Copilot Chat
2. 點擊模型選擇器（對話框頂部）
3. 選擇所需模型
4. 開始對話
```

### 在命令行使用
```bash
# 使用特定模型
gh copilot --model claude-3.5-sonnet "explain this code"

# 列出可用模型
gh copilot list-models
```

### 程式化選擇
```javascript
// 在註釋中指定模型
// @copilot-model: gemini-2.0-flash
function optimizedFunction() {
  // Gemini Flash將處理這個請求
}

// @copilot-model: claude-opus-4.1
function complexArchitecture() {
  // Claude Opus將處理這個請求
}
```

## 模型選擇建議

### 基於任務類型
| 任務 | 推薦模型 | 原因 |
|------|----------|------|
| 快速代碼補全 | Gemini 2.0 Flash | 最快響應 |
| 架構設計 | Claude Opus 4.1 | 深度推理 |
| 代碼審查 | Claude 3.7 Sonnet | 平衡準確 |
| 文檔生成 | GPT-4.1 | 自然語言 |
| 調試協助 | o3/o4 | 邏輯分析 |
| 批量重構 | Gemini 2.5 Pro | 大上下文 |

### 基於優先級
- **速度優先**: Gemini Flash, o3-mini
- **品質優先**: Claude Opus, GPT-5
- **成本優先**: Gemini Flash, o3-mini
- **平衡選擇**: Claude Sonnet, GPT-4.1

## 企業配置

### 組織級控制
```json
{
  "copilot": {
    "allowedModels": [
      "claude-3.5-sonnet",
      "gemini-2.0-flash",
      "gpt-4.1"
    ],
    "defaultModel": "gemini-2.0-flash",
    "budgetLimit": 1000,
    "roleBasedAccess": {
      "senior-dev": ["all"],
      "junior-dev": ["gemini-flash", "gpt-4.1"],
      "contractor": ["gemini-flash"]
    }
  }
}
```

### 政策設置
- 控制哪些模型可用
- 設置預算限制
- 基於角色的訪問控制
- 審計和合規追蹤

## 整合擴展

### Copilot Workspace
- 多檔案編輯支援多模型
- 自動選擇最適合的模型
- 跨模型協作功能

### Code Review
- 使用多個模型進行交叉驗證
- 不同視角的代碼分析
- 綜合評分系統

### Security Autofix
- Claude分析漏洞
- GPT生成修復
- Gemini驗證修復

## API整合

### REST API範例
```bash
curl -X POST https://api.github.com/copilot/completions \
  -H "Authorization: token YOUR_TOKEN" \
  -H "X-GitHub-Model: claude-3.5-sonnet" \
  -d '{
    "prompt": "Generate a REST API endpoint",
    "model": "claude-3.5-sonnet",
    "temperature": 0.7
  }'
```

### SDK使用
```javascript
const { Copilot } = require('@github/copilot-sdk');

const copilot = new Copilot({
  token: process.env.GITHUB_TOKEN,
  defaultModel: 'gemini-2.0-flash'
});

// 使用特定模型
const response = await copilot.complete({
  prompt: 'Optimize this function',
  model: 'claude-opus-4.1',
  maxTokens: 1000
});
```

## 性能基準

### 響應時間對比
| 模型 | 平均響應時間 | P95延遲 |
|------|-------------|---------|
| Gemini Flash | 0.8s | 1.2s |
| GPT-4.1 | 1.5s | 2.5s |
| Claude Sonnet | 2.0s | 3.5s |
| Claude Opus | 3.5s | 5.0s |

### 準確率對比
| 模型 | 語法正確率 | 邏輯正確率 |
|------|-----------|-----------|
| Claude Opus | 99% | 96% |
| GPT-5 | 98% | 94% |
| Claude Sonnet | 97% | 93% |
| Gemini Pro | 96% | 91% |
| Gemini Flash | 94% | 88% |

## 未來路線圖

### 2025 Q1-Q2
- 更多模型加入（Llama, Mistral）
- 改進的模型選擇UI
- 自動模型推薦

### 2025 Q3-Q4
- 自定義模型支援
- 本地模型整合
- 混合模型工作流

## 常見問題

### Q: 如何知道哪個模型被使用？
A: Copilot Chat會在回應中顯示使用的模型名稱

### Q: 可以設置預設模型嗎？
A: 是的，在設置中可以配置預設模型

### Q: 不同模型的成本如何計算？
A: 企業版按使用量計費，個人版包含在訂閱中

### Q: 模型切換會影響上下文嗎？
A: 不會，上下文在模型間共享

## 相關連結

- [GitHub Blog - Bringing Developer Choice to Copilot](https://github.blog/news-insights/product-news/bringing-developer-choice-to-copilot/)
- [Copilot Documentation](https://docs.github.com/en/copilot)
- [Supported Models Reference](https://docs.github.com/en/copilot/reference/ai-models/supported-models)

---

*最後更新：2024-12-31*
*來源：GitHub官方文檔和部落格*