# Archon MCP Server

**Purpose**: AI-powered knowledge base and task management platform for coding assistants

## Prerequisites
- Docker Desktop installed and running
- Node.js 18+ installed
- Supabase account (free tier available)
- OpenAI API key (or Gemini/Ollama alternatives)

## Setup Instructions

### 1. Clone and Configure Archon
```bash
# Clone the repository
git clone https://github.com/coleam00/archon.git
cd archon

# Copy and configure environment
cp .env.example .env
# Edit .env with your credentials:
# SUPABASE_URL=https://your-project.supabase.co
# SUPABASE_SERVICE_KEY=your-service-key-here
```

### 2. Database Setup
Run the SQL script `migration/complete_setup.sql` in your Supabase project's SQL Editor

### 3. Start Docker Services
```bash
docker compose up --build -d
```

This starts:
- **Server** (Port 8181): Core API and business logic
- **MCP Server** (Port 8051): Protocol interface for AI clients
- **UI** (Port 3737): Web interface

### 4. Configure API Keys
Open `http://localhost:3737` to configure your API keys (OpenAI, Gemini, or Ollama)

## Triggers
- Complex project knowledge management needs
- Multi-step task tracking and organization
- AI-assisted requirement generation
- Web crawling and document processing for project context
- Collaborative document editing with AI assistance

## Choose When
- **Over native Claude**: When you need persistent knowledge storage across sessions
- **For new projects**: To build comprehensive project understanding
- **For complex tasks**: When systematic task breakdown and tracking is needed
- **For research**: When extensive web crawling and document analysis is required
- **For collaboration**: When sharing knowledge base with team members

## Works Best With
- **Context7**: Archon stores knowledge → Context7 provides specific docs
- **Sequential**: Archon manages tasks → Sequential plans implementation
- **Serena**: Archon tracks requirements → Serena analyzes code compliance

## Features
- **Knowledge Management**:
  - Web crawling and document processing
  - Smart search with advanced RAG strategies
  - Vector search with contextual embeddings
  
- **Task Management**:
  - Hierarchical project tracking
  - AI-assisted task and requirement generation
  - Progress tracking and prioritization

- **AI Integration**:
  - Works with Claude Code, Cursor, and other AI assistants
  - Supports multiple AI models (OpenAI, Ollama, Google Gemini)
  - Real-time streaming responses

## Examples
```
"Build a knowledge base for my React project" → Archon crawls docs and codebase
"Track features for v2.0 release" → Archon manages hierarchical task structure
"Research authentication best practices" → Archon crawls and analyzes resources
"Generate test requirements from specs" → Archon creates AI-assisted test plans
"Maintain project context across sessions" → Archon persists knowledge
```

## Important Notes
- Requires Docker to be running before use
- Initial setup includes database migration
- Knowledge persists across Claude Code sessions
- HTTP transport at `http://localhost:8051/mcp`