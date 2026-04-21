#!/bin/bash

PROJECT_PATH="$HOME/Desktop/GitHub/CountWize  - Website"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 AI WORKFLOW SETUP VERIFICATION"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check directories
echo "📁 Checking directories..."
[ -d "$PROJECT_PATH/.ai-workflow" ] && echo "  ✅ .ai-workflow exists" || echo "  ❌ .ai-workflow missing"
[ -d "$PROJECT_PATH/.ai-workflow-config" ] && echo "  ✅ .ai-workflow-config exists" || echo "  ❌ .ai-workflow-config missing"
echo ""

# Check session logs
echo "📝 Checking session logs..."
[ -f "$PROJECT_PATH/.ai-workflow/claude-code-session.md" ] && echo "  ✅ Claude Code log exists" || echo "  ❌ Claude Code log missing"
[ -f "$PROJECT_PATH/.ai-workflow/testsprite-results.md" ] && echo "  ✅ TestSprite log exists" || echo "  ❌ TestSprite log missing"
[ -f "$PROJECT_PATH/.ai-workflow/antigravity-research.md" ] && echo "  ✅ Antigravity log exists" || echo "  ❌ Antigravity log missing"
echo ""

# Check state files
echo "🔄 Checking state files..."
[ -f "$PROJECT_PATH/.ai-workflow/workflow-state.json" ] && echo "  ✅ Workflow state exists" || echo "  ❌ Workflow state missing"
[ -f "$PROJECT_PATH/.ai-workflow/handoff-queue.json" ] && echo "  ✅ Handoff queue exists" || echo "  ❌ Handoff queue missing"
echo ""

# Check scripts
echo "🛠️  Checking scripts..."
[ -x "$PROJECT_PATH/.ai-workflow-config/claude-code-wrapper.sh" ] && echo "  ✅ Claude Code wrapper executable" || echo "  ❌ Claude Code wrapper not executable"
[ -x "$PROJECT_PATH/.ai-workflow-config/session-restore.sh" ] && echo "  ✅ Session restore executable" || echo "  ❌ Session restore not executable"
echo ""

# Check launcher
echo "🚀 Checking launcher..."
[ -d "$HOME/Desktop/CountWize-AI-Workflow.app" ] && echo "  ✅ Master launcher exists on Desktop" || echo "  ❌ Master launcher missing"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Setup verification complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
