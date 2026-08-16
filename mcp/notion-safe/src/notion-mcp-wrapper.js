#!/usr/bin/env node

/**
 * Notion MCP Wrapper
 * 簡化版安全包裝器 - 專注於核心安全功能
 * 
 * 主要功能：
 * 1. 操作限流 - 防止失控的大量操作
 * 2. 操作日誌 - 追蹤所有操作記錄
 */

const { spawn } = require('child_process');
const readline = require('readline');
const path = require('path');
const fs = require('fs').promises;

// 載入 .env 檔案（支援多個位置）
function loadEnvFile(envPath) {
  try {
    if (require('fs').existsSync(envPath)) {
      const envContent = require('fs').readFileSync(envPath, 'utf8');
      envContent.split('\n').forEach(line => {
        const [key, ...valueParts] = line.split('=');
        if (key && !key.startsWith('#') && valueParts.length > 0) {
          const value = valueParts.join('=').trim();
          if (!process.env[key.trim()]) {
            process.env[key.trim()] = value;
          }
        }
      });
      return true;
    }
  } catch (e) {
    // 忽略錯誤
  }
  return false;
}

// 嘗試從多個位置載入 .env
const projectRoot = path.join(__dirname, '../../../');
const envLocations = [
  path.join(projectRoot, '.env'),           // 專案根目錄
  path.join(__dirname, '../../.env'),       // mcp/notion-safe 目錄
  path.join(__dirname, '../.env')           // src 上層目錄
];

for (const envPath of envLocations) {
  if (loadEnvFile(envPath)) {
    process.stderr.write(`Loaded environment from: ${path.relative(projectRoot, envPath)}\n`);
    break;
  }
}

class NotionMCPWrapper {
  constructor() {
    // 載入設定
    this.config = {
      maxOpsPerHour: parseInt(process.env.MAX_OPERATIONS_PER_HOUR || '100'),
      logToFile: process.env.LOG_TO_FILE !== 'false'
    };

    this.operationLog = [];
    // 支援環境變數配置日誌目錄，預設為當前工作目錄的 .notion-logs
    this.logDir = process.env.NOTION_LOG_DIR || path.join(process.cwd(), '.notion-logs');
    
    this.init();
  }

  async init() {
    // 建立日誌目錄
    if (this.config.logToFile) {
      await fs.mkdir(this.logDir, { recursive: true }).catch(() => {});
    }

    // 尋找 Notion MCP Server（優先使用專案內的，否則使用全域的）
    const { execSync } = require('child_process');
    let mcpServerPath = null;
    
    // 嘗試找到 notion-mcp-server
    try {
      // 首先嘗試 mcp/notion-safe 目錄內的 node_modules
      const localMcpPath = path.join(__dirname, '../node_modules/.bin/notion-mcp-server');
      if (require('fs').existsSync(localMcpPath)) {
        mcpServerPath = localMcpPath;
        process.stderr.write(`Using local MCP server: ${path.relative(projectRoot, mcpServerPath)}\n`);
      } else {
        // 嘗試專案根目錄的 node_modules
        const projectMcpPath = path.join(__dirname, '../../../node_modules/.bin/notion-mcp-server');
        if (require('fs').existsSync(projectMcpPath)) {
          mcpServerPath = projectMcpPath;
          process.stderr.write(`Using project-level MCP server: ${path.relative(projectRoot, mcpServerPath)}\n`);
        } else {
          // 使用 which 命令找到全域安裝的
          mcpServerPath = execSync('which notion-mcp-server', { encoding: 'utf8' }).trim();
          process.stderr.write(`Using global MCP server: ${mcpServerPath}\n`);
        }
      }
    } catch (error) {
      process.stderr.write('❌ Error: notion-mcp-server not found!\n');
      process.stderr.write('Please install it with: npm install @notionhq/notion-mcp-server\n');
      process.exit(1);
    }

    // 啟動官方 Notion MCP Server
    this.mcpServer = spawn(mcpServerPath, [], {
      env: { 
        ...process.env,
        NOTION_TOKEN: process.env.NOTION_TOKEN 
      },
      stdio: ['pipe', 'pipe', 'pipe']
    });

    // 設置輸入流處理
    this.rl = readline.createInterface({
      input: process.stdin,
      terminal: false
    });

    // 處理來自 Claude 的請求
    this.rl.on('line', async (line) => {
      try {
        const request = JSON.parse(line);
        
        // 對寫入操作進行安全檢查
        if (this.isWriteOperation(request)) {
          const checkResult = await this.performSafetyCheck(request);
          
          if (!checkResult.allowed) {
            // 拒絕不安全的操作
            this.sendError(request.id, -32000, checkResult.reason);
            return;
          }
          
          // 檢查是否需要分批處理大內容
          if (this.shouldBatchProcess(request)) {
            await this.handleBatchRequest(request);
            return;
          }
          
          // 記錄操作
          await this.logOperation(request, 'pending');
        }
        
        // 轉發給官方 MCP Server
        this.mcpServer.stdin.write(line + '\n');
        
      } catch (error) {
        // 解析錯誤時直接轉發
        this.mcpServer.stdin.write(line + '\n');
      }
    });

    // 轉發官方 MCP Server 的回應
    this.mcpServer.stdout.on('data', (data) => {
      process.stdout.write(data);
      
      // 嘗試記錄回應
      try {
        const lines = data.toString().split('\n').filter(l => l);
        for (const line of lines) {
          const response = JSON.parse(line);
          if (response.id && this.operationLog.find(op => op.requestId === response.id)) {
            this.logOperation(null, response.error ? 'failed' : 'success', response.id);
          }
        }
      } catch (e) {
        // 忽略解析錯誤
      }
    });

    // 錯誤輸出
    this.mcpServer.stderr.on('data', (data) => {
      process.stderr.write(data);
    });

    // 子進程退出處理
    this.mcpServer.on('close', (code) => {
      process.exit(code);
    });

    // 輸出啟動資訊
    this.printStartupInfo();
  }

  /**
   * 判斷是否為寫入操作
   */
  isWriteOperation(request) {
    if (request.method === 'tools/call') {
      const toolName = request.params?.name;
      const writeTools = [
        'API-post-page',              // Create a page
        'API-patch-page',             // Update page properties
        'API-patch-block-children',   // Append block children
        'API-update-a-block',         // Update a block
        'API-create-a-database',      // Create a database
        'API-update-a-database',      // Update a database
        'API-delete-a-block',         // Delete a block
        'API-create-a-comment'        // Create comment
      ];
      return writeTools.includes(toolName);
    }
    return false;
  }

  /**
   * 執行安全檢查
   */
  async performSafetyCheck(request) {
    // 1. 檢查操作頻率限制
    const rateCheckResult = this.checkRateLimit();
    if (!rateCheckResult.allowed) {
      return rateCheckResult;
    }

    // 2. 不再需要區域限制檢查

    return { allowed: true };
  }

  /**
   * 檢查操作頻率
   */
  checkRateLimit() {
    const oneHourAgo = new Date(Date.now() - 60 * 60 * 1000);
    const recentOps = this.operationLog.filter(
      log => new Date(log.timestamp) > oneHourAgo && log.status !== 'failed'
    );

    if (recentOps.length >= this.config.maxOpsPerHour) {
      return {
        allowed: false,
        reason: `Rate limit exceeded: ${recentOps.length}/${this.config.maxOpsPerHour} operations in the last hour`
      };
    }

    return { allowed: true };
  }

  /**
   * 判斷是否需要分批處理
   */
  shouldBatchProcess(request) {
    // 檢查 patch-block-children 操作的內容大小
    if (request.params?.name === 'API-patch-block-children') {
      const children = request.params?.arguments?.children;
      // 如果區塊數量超過 20 個，需要分批
      return children && children.length > 20;
    }
    return false;
  }

  /**
   * 處理批次請求
   */
  async handleBatchRequest(request) {
    const children = request.params.arguments.children;
    const batchSize = 20;
    const batches = [];
    
    // 分割成批次
    for (let i = 0; i < children.length; i += batchSize) {
      batches.push(children.slice(i, Math.min(i + batchSize, children.length)));
    }
    
    process.stderr.write(`📦 Splitting large request into ${batches.length} batches\n`);
    
    // 逐批處理
    for (let i = 0; i < batches.length; i++) {
      const batchRequest = {
        ...request,
        id: `${request.id}_batch_${i}`,
        params: {
          ...request.params,
          arguments: {
            ...request.params.arguments,
            children: batches[i]
          }
        }
      };
      
      process.stderr.write(`📝 Processing batch ${i + 1}/${batches.length} (${batches[i].length} items)\n`);
      
      // 記錄批次操作
      await this.logOperation({
        ...batchRequest,
        batchInfo: { current: i + 1, total: batches.length }
      }, 'pending');
      
      // 轉發批次請求
      this.mcpServer.stdin.write(JSON.stringify(batchRequest) + '\n');
      
      // 等待處理（避免過快發送）
      await new Promise(resolve => setTimeout(resolve, 500));
    }
    
    process.stderr.write(`✅ All ${batches.length} batches sent successfully\n`);
  }


  /**
   * 記錄操作
   */
  async logOperation(request, status, requestId = null) {
    const logEntry = {
      timestamp: new Date().toISOString(),
      requestId: requestId || request?.id,
      method: request?.method,
      tool: request?.params?.name,
      status: status
    };

    this.operationLog.push(logEntry);

    // 寫入日誌檔案
    if (this.config.logToFile) {
      const logFile = path.join(
        this.logDir,
        `operations-${new Date().toISOString().split('T')[0]}.jsonl`
      );
      
      try {
        await fs.appendFile(logFile, JSON.stringify(logEntry) + '\n');
      } catch (error) {
        process.stderr.write(`Failed to write log: ${error.message}\n`);
      }
    }

    // 輸出到 stderr（不影響 MCP 協議）
    if (status === 'pending') {
      process.stderr.write(`📝 ${logEntry.tool || logEntry.method}\n`);
    }
  }

  /**
   * 發送錯誤回應
   */
  sendError(id, code, message) {
    const error = {
      jsonrpc: '2.0',
      id,
      error: { code, message }
    };
    process.stdout.write(JSON.stringify(error) + '\n');
    
    // 記錄被拒絕的操作
    process.stderr.write(`❌ Blocked: ${message}\n`);
  }

  /**
   * 輸出啟動資訊
   */
  printStartupInfo() {
    process.stderr.write('\n');
    process.stderr.write('╔══════════════════════════════════════╗\n');
    process.stderr.write('║   Notion MCP Wrapper Started         ║\n');
    process.stderr.write('╚══════════════════════════════════════╝\n');
    process.stderr.write('\n');
    process.stderr.write('Configuration:\n');
    process.stderr.write(`  • Claude Zone: ${this.config.claudeZoneId || 'not set (unrestricted)'}\n`);
    process.stderr.write(`  • Rate Limit: ${this.config.maxOpsPerHour} ops/hour\n`);
    process.stderr.write(`  • Zone Check: ${this.config.strictZoneCheck ? 'strict' : 'relaxed'}\n`);
    process.stderr.write(`  • Logging: ${this.config.logToFile ? 'enabled' : 'disabled'}\n`);
    if (this.config.logToFile) {
      process.stderr.write(`  • Log Directory: ${this.logDir}\n`);
    }
    process.stderr.write('\n');
    process.stderr.write('Safety Features:\n');
    process.stderr.write('  ✓ Rate limiting protection\n');
    process.stderr.write('  ✓ Operation logging\n');
    if (this.config.claudeZoneId) {
      process.stderr.write('  ✓ Zone isolation enabled\n');
    }
    process.stderr.write('\n');
    process.stderr.write('─────────────────────────────────────────\n');
    process.stderr.write('\n');
  }

  /**
   * 取得操作統計
   */
  getStats() {
    const stats = {
      total: this.operationLog.length,
      successful: this.operationLog.filter(op => op.status === 'success').length,
      failed: this.operationLog.filter(op => op.status === 'failed').length,
      pending: this.operationLog.filter(op => op.status === 'pending').length,
      lastHour: this.operationLog.filter(op => 
        new Date(op.timestamp) > new Date(Date.now() - 60 * 60 * 1000)
      ).length
    };
    return stats;
  }
}

// 啟動 Wrapper
const wrapper = new NotionMCPWrapper();

// 優雅關閉
process.on('SIGINT', () => {
  const stats = wrapper.getStats();
  process.stderr.write('\n');
  process.stderr.write('Session Statistics:\n');
  process.stderr.write(`  • Total operations: ${stats.total}\n`);
  process.stderr.write(`  • Successful: ${stats.successful}\n`);
  process.stderr.write(`  • Failed: ${stats.failed}\n`);
  process.stderr.write('\n');
  process.stderr.write('Shutting down...\n');
  
  if (wrapper.mcpServer) {
    wrapper.mcpServer.kill();
  }
  process.exit(0);
});

process.on('SIGTERM', () => {
  if (wrapper.mcpServer) {
    wrapper.mcpServer.kill();
  }
  process.exit(0);
});