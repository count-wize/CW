#!/bin/bash

PROJECT_PATH="$HOME/Desktop/GitHub/CountWize  - Website"
SESSION_LOG="$PROJECT_PATH/.ai-workflow/claude-code-session.md"
WORKFLOW_STATE="$PROJECT_PATH/.ai-workflow/workflow-state.json"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🤖 CLAUDE CODE - AI WORKFLOW"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Read last session
if [ -f "$SESSION_LOG" ]; then
    echo "📂 Loading previous session context..."
    echo ""
    tail -n 30 "$SESSION_LOG"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
fi

# Update session log
echo "" >> "$SESSION_LOG"
echo "## Session Started: $(date)" >> "$SESSION_LOG"

# Change to project directory
cd "$PROJECT_PATH"

echo ""
echo "💡 TIP: Type '/context' to see all previous work"
echo "💡 When done, your work will be automatically saved"
echo ""
echo "Starting Claude Code..."
echo ""

# Launch Claude Code
claude

# On exit, save session
echo "" >> "$SESSION_LOG"
echo "**Session Ended:** $(date)" >> "$SESSION_LOG"
echo "---" >> "$SESSION_LOG"

echo ""
echo "💾 Session saved to .ai-workflow/claude-code-session.md"
