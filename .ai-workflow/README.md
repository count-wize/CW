# AI Workflow Orchestrator v4.1

> **Codename:** Swiss Watch  
> **Version:** 4.1.0  
> **Status:** Production Ready

A comprehensive, production-grade AI workflow orchestration system that coordinates multiple AI agents for automated development tasks.

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Creating Tasks](#-creating-tasks)
- [Dashboard](#-dashboard)
- [Configuration](#-configuration)
- [Status Protocol](#-status-protocol)
- [Troubleshooting](#-troubleshooting)
- [Changelog](#-changelog)

---

## ✨ Features

### Core Features
- **Intelligent Task Parsing** - Parses `planning.md` files, extracting only proper task headers (`### Task A1:`)
- **Automatic Phase Splitting** - Splits tasks into optimal phases based on token count and task limits
- **HTTP Polling Dashboard** - Reliable real-time updates without WebSocket complexity
- **Status File Protocol** - Clean communication between orchestrator and Claude Code
- **Auto-Cascade** - Automatically moves to next phase after completion
- **Error Recovery** - Configurable retries with automatic error detection

### Automation Features
- **Git Integration** - Automatic commit and push after each phase
- **Built-in Testing** - Runs validation tests after phase completion
- **Sound Notifications** - macOS system sounds for status changes
- **Session Persistence** - Resume workflows after restarts

### Developer Experience
- **Beautiful Dashboard** - Modern dark theme UI with real-time updates
- **Comprehensive Logging** - Full log history with search and export
- **One-Click Launcher** - macOS app for instant startup
- **Detailed Documentation** - Complete guides for all components

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          AI WORKFLOW SYSTEM v4.1                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │   Advisor   │    │ Orchestrator│    │ Claude Code │    │  TestSprite │  │
│  │  (Claude)   │    │  (Python)   │    │   (Agent)   │    │  (Testing)  │  │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘  │
│         │                  │                  │                  │          │
│         │ Creates          │ Orchestrates     │ Executes         │ Validates│
│         │ planning.md      │ workflow         │ tasks            │ changes  │
│         │                  │                  │                  │          │
│         ▼                  ▼                  ▼                  ▼          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        .ai-workflow/                                │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐    │   │
│  │  │planning.md │  │ status.json│  │command.md  │  │session.json│    │   │
│  │  │ (Tasks)    │  │ (Protocol) │  │ (Current)  │  │ (State)    │    │   │
│  │  └────────────┘  └────────────┘  └────────────┘  └────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                        Dashboard (HTTP :3000)                       │   │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │   │
│  │  │ Status  │  │ Phases  │  │  Logs   │  │ Errors  │  │  Tests  │   │   │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Communication Flow

```
1. User creates planning.md with tasks
2. Orchestrator parses tasks into phases
3. Orchestrator writes current-command.md
4. Claude Code reads and executes tasks
5. Claude Code updates status.json → "completed"
6. Orchestrator detects change, runs tests
7. Orchestrator auto-cascades to next phase
8. Repeat until all phases complete
```

---

## 📦 Installation

### Prerequisites

- **Python 3.8+** - Required for orchestrator
- **macOS 10.13+** - For launcher app and sound notifications
- **Git** - For version control integration

### Quick Install

```bash
# Navigate to the AI-Workflow-v4.1 directory
cd path/to/AI-Workflow-v4.1

# Make installer executable
chmod +x install.sh

# Run installer with your project path
./install.sh /path/to/your/project
```

### Manual Install

```bash
# Copy files to your project
mkdir -p /path/to/project/.ai-workflow
cp orchestrator.py dashboard.html CLAUDE.md /path/to/project/.ai-workflow/

# Make orchestrator executable
chmod +x /path/to/project/.ai-workflow/orchestrator.py

# Create required directories
mkdir -p /path/to/project/.ai-workflow/{logs,phases,test-results,session-history}
```

---

## 🚀 Quick Start

### 1. Create Your Task Plan

Edit `.ai-workflow/planning.md`:

```markdown
# Project Fix Plan

## PHASE A: Critical Fixes

### Task A1: Fix Broken Navigation

**Files:** `index.html`, `css/nav.css`

The navigation menu is broken on mobile devices.

**Required Actions:**
1. Add responsive breakpoints
2. Fix hamburger menu toggle
3. Test on mobile viewport

---

### Task A2: Fix Form Validation

**Files:** `js/forms.js`

Form validation not working properly.

**Required Actions:**
1. Add email format validation
2. Add required field checks
3. Display error messages
```

### 2. Start the Orchestrator

**Option A: Double-click the launcher**
```
~/Desktop/AI-Workflow-v4.1.app
```

**Option B: Terminal**
```bash
cd /path/to/your/project
python3 .ai-workflow/orchestrator.py .
```

### 3. Use the Dashboard

1. Open http://localhost:3000
2. Click **"Analyze Plan"** to parse planning.md
3. Review the phases created
4. Click **"Start"** to begin the workflow

### 4. Execute Tasks (Claude Code)

In Claude Code:
```bash
# Read your current tasks
cat .ai-workflow/current-command.md

# ... execute the tasks ...

# Signal completion
cat > .ai-workflow/status.json << 'EOF'
{
  "state": "completed",
  "current_phase": "A",
  "phases_completed": ["A"],
  "files_modified": ["index.html", "css/nav.css"],
  "errors": []
}
EOF
```

---

## 📝 Creating Tasks

### Task Format (CRITICAL)

Tasks **MUST** follow this exact format:

```markdown
### Task [Letter][Number]: Title Here

Content and description...
```

**Valid Examples:**
- `### Task A1: Fix broken images` ✓
- `### Task B2: Update API endpoints` ✓
- `### Task C10: Refactor database` ✓

**Invalid Examples:**
- `## Task A1: Wrong heading level` ✗
- `Step 1: This is a sub-step` ✗
- `Task A1: Missing ### prefix` ✗
- `### Fix something: No task ID` ✗

### Task Structure

```markdown
### Task A1: Descriptive Title

**Priority:** Critical | High | Medium | Low
**Files:** `file1.html`, `file2.css`, `file3.js`

Description of the issue or feature. Be specific about what needs to change.

**Required Actions:**
1. First specific action to take
2. Second action with details
3. Third action

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

**Notes:**
Any additional context or warnings.
```

### Phase Organization

Tasks are automatically grouped by their phase letter:

```markdown
## PHASE A: Critical Fixes
### Task A1: ...
### Task A2: ...
### Task A3: ...

## PHASE B: High Priority
### Task B1: ...
### Task B2: ...

## PHASE C: Medium Priority
### Task C1: ...
```

The orchestrator will split these into execution phases based on:
- Maximum 6 tasks per phase (configurable)
- Maximum ~90,000 tokens per phase (configurable)

---

## 📊 Dashboard

### Status Panel

Shows current workflow state:
- **IDLE** - No plan loaded
- **READY** - Plan analyzed, ready to start
- **RUNNING** - Executing phases
- **WAITING FOR CLAUDE** - Waiting for Claude Code to complete
- **TESTING** - Running validation tests
- **COMPLETED** - All phases done
- **ERROR** - Something went wrong

### Phases Panel

Lists all phases with:
- Phase letter and name
- Task count and token estimate
- Current state (pending/running/completed/error)
- Action buttons (Start/Skip/Retry)

### Controls

- **Analyze Plan** - Parse planning.md and create phases
- **Start** - Begin workflow execution
- **Pause** - Pause the workflow
- **Reset** - Clear progress and start fresh
- **Preview** - Open localhost:8000 for site preview
- **Refresh** - Manually refresh state

### Logs Panel

Real-time log output with:
- Timestamps
- Log levels (INFO/WARN/ERROR/DEBUG)
- Searchable history
- Export capability

---

## ⚙️ Configuration

Edit `.ai-workflow/config.json`:

```json
{
  "dashboard_port": 3000,
  "websocket_port": 3001,
  "preview_port": 8000,
  
  "auto_cascade": true,
  "auto_cascade_delay": 5,
  "auto_trigger_claude": true,
  "auto_commit": true,
  "auto_push": true,
  
  "sound_notifications": true,
  
  "max_retries": 3,
  "retry_delay": 10,
  
  "run_tests": true,
  "testsprite_api_key": "",
  
  "max_tasks_per_phase": 6,
  "target_tokens_per_phase": 90000,
  
  "log_level": "INFO",
  "max_log_entries": 1000
}
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `dashboard_port` | int | 3000 | HTTP server port for dashboard |
| `auto_cascade` | bool | true | Auto-start next phase after completion |
| `auto_cascade_delay` | int | 5 | Seconds to wait before auto-cascade |
| `auto_commit` | bool | true | Automatically git commit after phases |
| `auto_push` | bool | true | Automatically git push after commits |
| `sound_notifications` | bool | true | Play system sounds on events |
| `max_retries` | int | 3 | Maximum retry attempts for failed phases |
| `run_tests` | bool | true | Run validation tests after phases |
| `max_tasks_per_phase` | int | 6 | Maximum tasks to include per phase |
| `target_tokens_per_phase` | int | 90000 | Target token budget per phase |

---

## 📡 Status Protocol

The orchestrator and Claude Code communicate via `.ai-workflow/status.json`.

### Status File Format

```json
{
  "version": "4.1.0",
  "protocol": "v1",
  "state": "idle|running|completed|error",
  "current_phase": "A",
  "phases_completed": ["A", "B"],
  "files_modified": ["file1.html", "file2.css"],
  "errors": [],
  "last_updated": "2026-01-21T12:00:00.000Z"
}
```

### State Values

| State | Description |
|-------|-------------|
| `idle` | No phase currently executing |
| `running` | Phase execution in progress |
| `completed` | Phase completed successfully |
| `error` | Phase encountered an error |

### Signaling Completion

After completing all tasks in a phase:

```bash
cat > .ai-workflow/status.json << 'EOF'
{
  "state": "completed",
  "current_phase": "A",
  "phases_completed": ["A"],
  "files_modified": ["index.html", "styles.css"],
  "errors": []
}
EOF
```

### Signaling Error

If you encounter an error:

```bash
cat > .ai-workflow/status.json << 'EOF'
{
  "state": "error",
  "current_phase": "A",
  "phases_completed": [],
  "files_modified": [],
  "errors": ["Description of what went wrong"]
}
EOF
```

---

## 🔧 Troubleshooting

### Dashboard shows "Connecting..."

**Fixed in v4.1!** The dashboard now uses HTTP polling instead of WebSocket.

If you still see issues:
1. Check orchestrator is running
2. Verify port 3000 is not in use
3. Refresh the browser

### Tasks not being detected

Ensure your tasks follow the exact format:
```markdown
### Task A1: Title Here
```

Common mistakes:
- Wrong heading level (`##` instead of `###`)
- Missing "Task" keyword
- Missing phase letter or number
- Using "Step X:" format (these are sub-steps, not tasks)

### Phase not advancing

Check that Claude Code updated status.json:
```bash
cat .ai-workflow/status.json
```

The `state` field must be `"completed"` for the orchestrator to advance.

### Orchestrator won't start

Check for port conflicts:
```bash
lsof -i :3000
lsof -i :3001
```

Kill existing processes:
```bash
pkill -f "orchestrator.py"
```

### Git commits failing

Verify git is configured:
```bash
git config user.name
git config user.email
```

Check for uncommitted changes:
```bash
git status
```

---

## 📋 Changelog

### v4.1.0 - "Swiss Watch" (2026-01-21)

**Fixed:**
- Dashboard now uses HTTP polling instead of broken WebSocket
- Task parser only matches `### Task X#:` format (not "Step X:")
- Proper state machine transitions
- Reliable status file change detection

**Added:**
- Comprehensive documentation
- Improved error handling
- Better logging with levels
- Session archiving

**Changed:**
- Simplified communication protocol
- Cleaner dashboard UI
- More robust git integration

### v4.0.0 (2026-01-20)

- Initial release
- WebSocket-based dashboard (had connection issues)
- Basic task parsing

---

## 📄 License

MIT License - Use freely for any purpose.

---

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the logs in `.ai-workflow/logs/`
3. Examine status.json for current state

---

**Happy Automating! 🤖**
