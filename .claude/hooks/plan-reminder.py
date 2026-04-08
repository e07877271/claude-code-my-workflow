#!/usr/bin/env python3
"""
Plan Persistence Reminder Hook for Claude Code

A Stop hook that checks whether a plan file exists in quality_reports/plans/
when Claude has been in plan mode. If a plan was discussed but not saved to
disk, blocks once with a reminder.

Usage (in .claude/settings.json):
    "Stop": [{ "hooks": [{ "type": "command",
        "command": "python3 \"$CLAUDE_PROJECT_DIR\"/.claude/hooks/plan-reminder.py" }] }]
"""
from __future__ import annotations

import json
import sys
import hashlib
import os
from pathlib import Path
from datetime import datetime


def get_session_dir() -> Path:
    """Return session state directory, consistent with other hooks."""
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    project_hash = hashlib.md5(project_dir.encode()).hexdigest()[:8]
    state_dir = Path.home() / ".claude" / "sessions" / project_hash
    state_dir.mkdir(parents=True, exist_ok=True)
    return state_dir


def get_hook_input():
    """Read hook input from stdin."""
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        hook_input = {}

    # If stop_hook_active, Claude is already continuing from a previous
    # Stop hook block — let it stop this time to avoid infinite loops.
    if hook_input.get("stop_hook_active", False):
        sys.exit(0)

    return hook_input


def load_state(state_path: Path) -> dict:
    """Load persisted state, or return defaults."""
    try:
        return json.loads(state_path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {"reminded": False}


def save_state(state_path: Path, state: dict):
    """Persist state to disk."""
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state))


def has_plan_file_today(project_dir: str) -> bool:
    """Check if any plan file in quality_reports/plans/ was modified today."""
    plans_dir = Path(project_dir) / "quality_reports" / "plans"
    if not plans_dir.is_dir():
        return False

    today = datetime.now().strftime("%Y-%m-%d")
    for md_file in plans_dir.glob("*.md"):
        if md_file.name.startswith(today):
            return True
        mtime = datetime.fromtimestamp(md_file.stat().st_mtime)
        if mtime.strftime("%Y-%m-%d") == today:
            return True

    return False


def conversation_mentions_plan(hook_input: dict) -> bool:
    """Check if the conversation transcript mentions plan-related activity."""
    transcript = hook_input.get("transcript", [])
    if not transcript:
        return False

    plan_keywords = [
        "EnterPlanMode", "ExitPlanMode", "plan mode",
        "## Plan", "## Approach", "## Steps",
        "quality_reports/plans/",
    ]

    recent = transcript[-5:] if len(transcript) >= 5 else transcript
    for msg in recent:
        content = ""
        if isinstance(msg, dict):
            content = str(msg.get("content", ""))
        elif isinstance(msg, str):
            content = msg

        for keyword in plan_keywords:
            if keyword.lower() in content.lower():
                return True

    return False


def main():
    hook_input = get_hook_input()
    project_dir = hook_input.get("cwd", "")
    if not project_dir:
        sys.exit(0)

    state_dir = get_session_dir()
    state_path = state_dir / "plan-reminder-state.json"
    state = load_state(state_path)

    # If already reminded this session, don't block again
    if state.get("reminded", False):
        sys.exit(0)

    # If a plan file was saved today, everything is fine
    if has_plan_file_today(project_dir):
        state["reminded"] = False
        save_state(state_path, state)
        sys.exit(0)

    # Check if the conversation involved plan-related activity
    if not conversation_mentions_plan(hook_input):
        sys.exit(0)

    # Plan was discussed but not saved — remind once
    today = datetime.now().strftime("%Y-%m-%d")
    state["reminded"] = True
    save_state(state_path, state)

    output = {
        "decision": "block",
        "reason": (
            f"Plan was discussed but not saved to disk. "
            f"Write it to quality_reports/plans/{today}_description.md "
            f"before stopping."
        ),
    }
    json.dump(output, sys.stdout)
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Fail open — never block Claude due to a hook bug
        sys.exit(0)
