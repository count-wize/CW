# AI Workflow System v4.1 - Claude Code Instructions

> **CRITICAL:** Read this entire document before starting any phase.

---

## 📋 Overview

You are executing tasks as part of an automated AI workflow system. The orchestrator monitors your progress via a **status file protocol**. After completing each phase, you **MUST** update the status file to signal completion.

---

## 🚨 CRITICAL: Status File Protocol

The orchestrator watches `.ai-workflow/status.json` for changes. This is how you communicate completion or errors.

### File Location
```
.ai-workflow/status.json
```

### After COMPLETING a Phase Successfully

Update the file with:

```json
{
  "state": "completed",
  "current_phase": "A",
  "phases_completed": ["A"],
  "files_modified": ["index.html", "css/styles.css", "js/main.js"],
  "errors": [],
  "last_updated": "2026-01-21T12:00:00.000Z"
}
```

**Quick command to update status:**
```bash
cat > .ai-workflow/status.json << 'EOF'
{
  "state": "completed",
  "current_phase": "A",
  "phases_completed": ["A"],
  "files_modified": ["file1.html", "file2.css"],
  "errors": []
}
EOF
```

### If You Encounter an ERROR

```json
{
  "state": "error",
  "current_phase": "A",
  "phases_completed": [],
  "files_modified": [],
  "errors": ["Description of what went wrong"],
  "last_updated": "2026-01-21T12:00:00.000Z"
}
```

---

## 📝 Workflow Process

### Step 1: Read Your Tasks

```bash
cat .ai-workflow/current-command.md
```

This file contains:
- Phase identifier
- List of tasks to complete
- Specific files to modify
- Completion instructions

### Step 2: Execute Tasks in Order

Work through each task methodically:
1. Understand the requirement
2. Make the necessary changes
3. Test the changes work
4. Move to next task

### Step 3: Commit and Push

After completing ALL tasks in the phase:

```bash
# Stage all changes
git add -A

# Commit with semantic message
git commit -m "fix: Phase A - [brief description of changes]"

# Push to remote
git push
```

**Commit message format:**
- `fix: Phase X - description` for bug fixes
- `feat: Phase X - description` for new features
- `refactor: Phase X - description` for code improvements

### Step 4: Update Status File (CRITICAL!)

This is the most important step. Without this, the orchestrator won't know you're done.

```bash
cat > .ai-workflow/status.json << 'EOF'
{
  "state": "completed",
  "current_phase": "A",
  "phases_completed": ["A"],
  "files_modified": ["list", "all", "modified", "files"],
  "errors": []
}
EOF
```

---

## ✅ Completion Checklist

Before signaling completion, verify:

- [ ] All tasks in `current-command.md` are complete
- [ ] Changes have been tested and work correctly
- [ ] Git commit has been created with semantic message
- [ ] Git push has been completed
- [ ] **`status.json` has been updated** ← MOST IMPORTANT!

---

## 📁 File Structure

```
project/
├── .ai-workflow/
│   ├── current-command.md  ← READ THIS - your tasks for current phase
│   ├── status.json         ← UPDATE THIS - signal completion/error
│   ├── planning.md         ← Full task plan (reference only)
│   ├── config.json         ← Configuration settings
│   ├── session.json        ← Session state (don't modify)
│   ├── orchestrator.py     ← Main orchestrator (don't modify)
│   ├── dashboard.html      ← Dashboard UI (don't modify)
│   ├── CLAUDE.md           ← This file
│   ├── logs/               ← Log files
│   ├── phases/             ← Individual phase files
│   └── test-results/       ← Test output
└── [your project files]
```

---

## 🔧 Quick Commands Reference

```bash
# Read current tasks
cat .ai-workflow/current-command.md

# Check current status
cat .ai-workflow/status.json

# View session state
cat .ai-workflow/session.json

# Complete a phase (update status)
cat > .ai-workflow/status.json << 'EOF'
{
  "state": "completed",
  "current_phase": "A",
  "phases_completed": ["A"],
  "files_modified": ["file1.html"],
  "errors": []
}
EOF

# Report an error
cat > .ai-workflow/status.json << 'EOF'
{
  "state": "error",
  "current_phase": "A",
  "phases_completed": [],
  "files_modified": [],
  "errors": ["Error description here"]
}
EOF
```

---

## ⚠️ Common Mistakes to Avoid

1. **Forgetting to update status.json** - The orchestrator will wait forever
2. **Not listing modified files** - Track all files you changed
3. **Forgetting to push** - Commit locally is not enough
4. **Wrong status format** - Use exact JSON format shown above
5. **Skipping tasks** - Complete all tasks before signaling done

---

## 🆘 Troubleshooting

### Orchestrator not detecting completion?
1. Check `.ai-workflow/status.json` exists
2. Verify JSON is valid (no syntax errors)
3. Ensure `"state": "completed"` is set
4. Make sure you saved the file

### Need to skip remaining tasks?
Update status.json with `"state": "completed"` anyway - the orchestrator will move on.

### Made a mistake in a completed phase?
The orchestrator supports retrying phases from the dashboard.

---

## 📞 Communication Protocol Summary

```
┌─────────────────────────────────────────────────────────────────┐
│                    COMMUNICATION FLOW                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ORCHESTRATOR                          CLAUDE CODE              │
│  ────────────                          ──────────               │
│       │                                     │                   │
│       │  writes current-command.md          │                   │
│       │ ──────────────────────────────────► │                   │
│       │                                     │                   │
│       │                                     │  reads tasks      │
│       │                                     │  executes work    │
│       │                                     │  commits & pushes │
│       │                                     │                   │
│       │         updates status.json         │                   │
│       │ ◄────────────────────────────────── │                   │
│       │                                     │                   │
│       │  detects change                     │                   │
│       │  runs tests                         │                   │
│       │  starts next phase                  │                   │
│       │                                     │                   │
└─────────────────────────────────────────────────────────────────┘
```

---

**Remember:** The status.json update is how you "talk" to the orchestrator. Without it, nothing happens!
