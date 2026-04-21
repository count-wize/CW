#!/bin/bash

PROJECT_PATH="$HOME/Desktop/GitHub/CountWize  - Website"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 AI WORKFLOW - SESSION SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "🤖 CLAUDE CODE - Last Work:"
echo "────────────────────────────────────────"
tail -n 15 "$PROJECT_PATH/.ai-workflow/claude-code-session.md"
echo ""

echo "🧪 TESTSPRITE - Last Tests:"
echo "────────────────────────────────────────"
tail -n 15 "$PROJECT_PATH/.ai-workflow/testsprite-results.md"
echo ""

echo "🌐 ANTIGRAVITY - Last Research:"
echo "────────────────────────────────────────"
tail -n 15 "$PROJECT_PATH/.ai-workflow/antigravity-research.md"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Press Enter to continue..."
read
