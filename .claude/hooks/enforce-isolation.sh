#!/bin/bash
# enforce-isolation.sh — PreToolUse hook enforcing pipeline isolation
#
# Reviewer agents are READ-ONLY. They may only write to quality_reports/
# for their reports. All other Edit/Write calls from reviewer agent
# contexts are blocked.
#
# Principle: "Critics never create. Creators never self-score."
# See: .claude/rules/pipeline-isolation.md
#
# Hook event: PreToolUse (matcher: "Edit|Write")

INPUT=$(cat)

TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null) || TOOL_NAME=""
if [[ "$TOOL_NAME" != "Edit" && "$TOOL_NAME" != "Write" ]]; then
    exit 0
fi

FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null) || FILE_PATH=""
if [[ -z "$FILE_PATH" ]]; then
    exit 0
fi

# Check if we're in a subagent context (agent_name field present)
AGENT_NAME=$(echo "$INPUT" | jq -r '.agent_name // empty' 2>/dev/null) || AGENT_NAME=""

# If no agent context, allow (main session can edit anything)
if [[ -z "$AGENT_NAME" ]]; then
    exit 0
fi

# Reviewer agents: read-only except for quality_reports/
REVIEWER_AGENTS="proofreader|slide-auditor|pedagogy-reviewer|domain-reviewer|tikz-reviewer|quarto-critic|r-reviewer"

if echo "$AGENT_NAME" | grep -qiE "$REVIEWER_AGENTS"; then
    # Allow writes to quality_reports/ (reports are their output)
    if echo "$FILE_PATH" | grep -q "quality_reports/"; then
        exit 0
    fi
    # Block all other writes
    echo "BLOCKED by enforce-isolation: Reviewer agent '$AGENT_NAME' cannot edit files outside quality_reports/. File the issue in your report; a fixer agent will implement it." >&2
    exit 2
fi

exit 0
