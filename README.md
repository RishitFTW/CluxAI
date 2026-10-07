<h1 align="center">CluxAI</h1>
<p align="center">
  <strong>RAG-Powered Autonomous AI Coding Assistant</strong><br/>
  <em>AST-aware code intelligence · Hybrid vector search · Autonomous task planning · Multi-LLM support</em>
</p>

---

## What is CluxAI?

CluxAI is a terminal-based AI coding assistant that **deeply understands your codebase**. It uses Tree-Sitter AST parsing to structurally index functions, classes, and scopes, then retrieves them via hybrid vector search to give precise, context-rich answers. Give it a high-level engineering goal and it will decompose it into sub-tasks, execute them with human-in-the-loop safety, and recover automatically from failures.

---

##  Features

####  AST-Aware Codebase RAG
- Structural code parsing via **Tree-Sitter** — extracts functions, classes, and scopes instead of naive line splits
- **Hybrid vector search** (dense + sparse) with **Qdrant** and **ChromaDB** backends
- Real-time file watcher auto-reindexes on file changes without restarts

####  Autonomous Task Planning & Execution
- **Goal decomposition** — breaks high-level objectives into ordered sub-tasks
- **Human-in-the-loop approval** before executing commands or modifying files
- **Self-healing error recovery** — analyzes failures and retries with corrective strategies
- Persistent task state tracking with a progress dashboard

####  Extensibility & LLM Support
- **Model Context Protocol (MCP)** integration — GitHub, filesystem, and custom MCP servers
- **Multi-provider LLMs**: OpenAI, Anthropic, Google Gemini, Ollama (local), HuggingFace
- **Skill system** with on-demand loading — lightweight metadata in prompts, full instructions loaded only when needed

####  Built-in Agent Tools
- Codebase semantic search, file read/write/append/delete, directory listing
- Shell command execution with safety guardrails (blocked dangerous commands, 30s timeout)
- Persistent session memory with SQLite-backed LangGraph checkpointers

---

## Architecture

```
┌──────────────────────────────────────────────────────┐
│                    Terminal REPL                     │
│              (Rich interactive CLI)                  │
├──────────────────────────────────────────────────────┤
│                  Agent Orchestrator                  │
│         (LangGraph + LangChain Agent)                │
├────────────┬────────────┬────────────┬───────────────┤
│  Codebase  │ Filesystem │  Terminal  │  MCP Server   │
│  Search    │   Tools    │   Tools    │   Tools       │
├────────────┴────────────┴────────────┴───────────────┤
│                    Skill System                      │
│          (Registry + On-demand Loading)              │
├──────────────────────────────────────────────────────┤
│              Task Planning Engine                    │
│    (Planner → Executor → Approval → Recovery)        │
├──────────────────────────────────────────────────────┤
│              Context & Retrieval Layer               │
│  ┌──────────┐  ┌──────────┐  ┌────────────────────┐  │
│  │Code      │  │ Vector   │  │  File System       │  │
│  │Parser    │  │ Store    │  │  Watcher           │  │
│  │(Tree-    │  │(Qdrant / │  │  (Watchdog)        │  │
│  │ Sitter)  │  │ChromaDB) │  │                    │  │
│  └──────────┘  └──────────┘  └────────────────────┘  │
├───────────────────────────────────────────────────── ┤
│                  LLM & Embeddings                    │
│   (OpenAI / Anthropic / Gemini / Ollama / HF)        │
├──────────────────────────────────────────────────────┤
│                 Memory & Sessions                    │
│            (SQLite Checkpointer)                     │
└──────────────────────────────────────────────────────┘
```

---

## Installation

### Prerequisites

- **Python 3.12+**
- **Poetry** (package manager)
- **Qdrant** (if using Qdrant as vector store — can run locally via Docker)
- **Node.js / npx** (required for MCP server tools)

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/RishitFTW/CluxAI.git
   cd CluxAI
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

3. **Set up environment variables**

   Create a `.env` file in the project root:
   ```env
   # Required — at least one LLM provider key
   OPENAI_API_KEY=sk-...
   ANTHROPIC_API_KEY=sk-ant-...
   GOOGLE_API_KEY=...

   # Optional — for MCP GitHub integration
   GITHUB_TOKEN=ghp_...
   ```

4. **Run CluxAI**
   ```bash
   poetry run cluxai
   ```

---

## Configuration

All settings live in `config.yaml`:

```yaml
llm:
  provider: ollama              # openai | anthropic | gemini | ollama | huggingface
  model: qwen3:8B

embeddings:
  provider: gemini
  model: gemini-embedding-2

rag:
  mode: hybrid                  # semantic | hybrid

vector_store:
  provider: qdrant              # qdrant | chromadb
  retrieval_mode: hybrid        # dense | sparse | hybrid
```

MCP servers are configured in `cluxai_mcp_servers.json` — GitHub and filesystem servers are included out of the box.

---

## Commands

| Command | Description |
|---|---|
| `/ask <question>` | Ask a natural language question about your codebase |
| `/plan <goal>` | Generate and execute a multi-step task plan |
| `/task_status` | Show progress of active tasks |
| `/show_index` | Inspect indexed code chunks |
| `/new_session` | Start a fresh conversation |
| `/switch <id>` | Resume a previous session |
| `/session` | Show current session ID |
| `/exit` | Quit CluxAI |

---

## Project Structure

```
CluxAI/
├── CluxAI/                  # Main application package
│   ├── main.py              # Entry point & interactive REPL loop
│   ├── config.py            # Configuration loader
│   ├── config.yaml          # Application settings
│   ├── cluxai_mcp_servers.json  # MCP server definitions
│   ├── agent/               # LangGraph agent construction & orchestration
│   ├── context/             # Codebase indexing & retrieval
│   │   ├── indexers/        # Tree-Sitter parser, vector store indexers, file watcher
│   │   └── retrievers/      # Semantic & hybrid search retrievers
│   ├── llm/                 # LLM & embedding provider factory
│   ├── mcp/                 # MCP client adapter integration
│   ├── memory/              # Session management & conversation memory
│   ├── observability/       # Logging infrastructure
│   ├── skills/              # Skill registry & on-demand skill loading
│   ├── tasks/               # Task planner, executor, approval, recovery, status
│   └── tools/               # Filesystem & terminal tool implementations
├── .env                     # Environment variables (not committed)
├── pyproject.toml           # Project metadata & dependencies
└── poetry.lock              # Locked dependency versions
```

---


## Tech Stack

| Category | Technologies |
|---|---|
| **Language** | Python 3.12+ (Poetry) |
| **Agent Framework** | LangGraph, LangChain |
| **LLM Providers** | OpenAI, Anthropic, Gemini, Ollama, HuggingFace |
| **Vector DBs** | Qdrant, ChromaDB, FastEmbed |
| **Code Parsing** | Tree-Sitter |
| **Tool Protocol** | Model Context Protocol (MCP) |
| **CLI** | Rich |

---

