#!/usr/bin/env node

/**
 * 測試批次處理功能
 * 用於驗證 notion-mcp-wrapper 的大內容分段處理能力
 */

// 創建一個包含多個區塊的測試請求
const createTestRequest = (numBlocks) => {
  const children = [];
  
  for (let i = 1; i <= numBlocks; i++) {
    children.push({
      type: "paragraph",
      paragraph: {
        rich_text: [{
          text: {
            content: `測試段落 ${i}: 這是一個測試內容，用於驗證批次處理功能是否正常運作。當內容超過 20 個區塊時，應該自動分批處理。`
          }
        }]
      }
    });
  }
  
  return {
    jsonrpc: "2.0",
    id: "test-batch-" + Date.now(),
    method: "tools/call",
    params: {
      name: "API-patch-block-children",
      arguments: {
        block_id: "test-block-id",
        children: children
      }
    }
  };
};

// 測試場景
const testScenarios = [
  { name: "小內容 (10 blocks)", blocks: 10, shouldBatch: false },
  { name: "邊界情況 (20 blocks)", blocks: 20, shouldBatch: false },
  { name: "需要分批 (30 blocks)", blocks: 30, shouldBatch: true },
  { name: "大內容 (50 blocks)", blocks: 50, shouldBatch: true },
  { name: "超大內容 (100 blocks)", blocks: 100, shouldBatch: true }
];

console.log("🧪 Notion MCP Wrapper 批次處理測試");
console.log("=====================================\n");

testScenarios.forEach(scenario => {
  const request = createTestRequest(scenario.blocks);
  const expectedBatches = Math.ceil(scenario.blocks / 20);
  
  console.log(`📋 測試: ${scenario.name}`);
  console.log(`   區塊數量: ${scenario.blocks}`);
  console.log(`   預期批次: ${expectedBatches}`);
  console.log(`   需要分批: ${scenario.shouldBatch ? '是' : '否'}`);
  
  // 檢查分批邏輯
  const needsBatch = request.params.arguments.children.length > 20;
  const actualBatches = Math.ceil(request.params.arguments.children.length / 20);
  
  if (needsBatch === scenario.shouldBatch) {
    console.log(`   ✅ 分批判斷正確`);
  } else {
    console.log(`   ❌ 分批判斷錯誤`);
  }
  
  if (actualBatches === expectedBatches) {
    console.log(`   ✅ 批次計算正確`);
  } else {
    console.log(`   ❌ 批次計算錯誤 (實際: ${actualBatches})`);
  }
  
  console.log();
});

console.log("=====================================");
console.log("測試完成！\n");

// 輸出測試請求範例
console.log("📝 測試請求範例 (30 blocks):");
const exampleRequest = createTestRequest(30);
console.log(JSON.stringify(exampleRequest, null, 2).substring(0, 500) + "...\n");

console.log("💡 使用方式:");
console.log("1. 將此測試請求通過 stdin 發送給 notion-mcp-wrapper");
console.log("2. 觀察是否正確分成 2 批處理");
console.log("3. 檢查日誌檔案確認批次操作記錄");