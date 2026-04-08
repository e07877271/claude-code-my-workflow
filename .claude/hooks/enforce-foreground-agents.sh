#!/bin/bash
# enforce-foreground-agents.sh — blocks background agents
#
# Background agents cannot prompt for user permissions, causing silent failures.
# This hook denies any Agent tool call with run_in_background=true.
#
# Hook event: PreToolUse (matcher: "Agent")

trap 'jq -n "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\"enforce-foreground-agents hook encountered an unexpected error\"}}" 2>/dev/null; exit 0' ERR

INPUT=$(cat)

RUN_IN_BG=$(echo "$INPUT" | jq -r '.tool_input.run_in_background // empty' 2>/dev/null) || RUN_IN_BG=""

if [ "$RUN_IN_BG" = "true" ]; then
  jq -n '{
    "hookSpecificOutput": {
      "hookEventName": "PreToolUse",
      "permissionDecision": "deny",
      "permissionDecisionReason": "Background agents are not permitted. Background agents cannot prompt for user permissions, causing silent tool call failures. Remove run_in_background or set it to false."
    }
  }'
fi

exit 0
