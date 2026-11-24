#!/usr/bin/env python3
"""Renders the Claude Code status line from the JSON payload on stdin."""

import json
import subprocess
import sys

RESET = "\033[0m"
DIM = "\033[2m"
BOLD = "\033[1m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"

SEP = f"{DIM} │ {RESET}"

BAR_WIDTH = 10
FILLED_CHAR = "█"
EMPTY_CHAR = "░"

GIT_TIMEOUT_SECONDS = 1


def format_tokens(count: float) -> str:
    if count >= 999_500:
        return f"{count / 1_000_000:.1f}".removesuffix(".0") + "M"
    if count >= 1_000:
        return f"{count / 1_000:.0f}k"
    return f"{count:.0f}"


def context_tokens(ctx: dict):
    tokens = ctx.get("total_input_tokens")
    if tokens is None:
        usage = ctx.get("current_usage")
        if usage:
            tokens = sum(
                usage.get(key) or 0
                for key in (
                    "input_tokens",
                    "cache_creation_input_tokens",
                    "cache_read_input_tokens",
                )
            )
    return tokens


def context_segment(data: dict) -> str:
    ctx = data.get("context_window") or {}
    used = ctx.get("used_percentage")
    if used is None:
        remaining = ctx.get("remaining_percentage")
        if remaining is not None:
            used = 100 - remaining
    if used is None:
        size = ctx.get("context_window_size")
        used_tokens = ctx.get("total_input_tokens")
        if size:
            used = (used_tokens or 0) / size * 100
    if used is None:
        return None

    used = max(0, min(100, used))
    if used > 75:
        color = RED
    elif used > 50:
        color = YELLOW
    else:
        color = GREEN

    filled = round(used / 100 * BAR_WIDTH)
    bar = FILLED_CHAR * filled + EMPTY_CHAR * (BAR_WIDTH - filled)
    detail = ""
    tokens = context_tokens(ctx)
    size = ctx.get("context_window_size")
    if tokens is not None and size:
        detail = f" {format_tokens(tokens)}/{format_tokens(size)}"
    return f"🧠 {color}[{bar}] {used:.0f}%{detail}{RESET}"


def cost_segment(data: dict) -> str:
    cost = data.get("cost") or {}
    total = cost.get("total_cost_usd")
    if total is None:
        return None
    amount = f"${total:.4f}" if total < 1 else f"${total:.2f}"
    return f"💰 {amount}"


def duration_segment(data: dict) -> str:
    cost = data.get("cost") or {}
    ms = cost.get("total_duration_ms")
    if ms is None:
        return None
    seconds = ms // 1000
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        formatted = f"{hours}h{minutes:02d}m"
    elif minutes:
        formatted = f"{minutes}m{seconds:02d}s"
    else:
        formatted = f"{seconds}s"
    return f"🕐 {formatted}"


def model_segment(data: dict) -> str:
    model = data.get("model") or {}
    name = model.get("display_name") or model.get("id")
    if not name:
        return None
    return f"{BOLD}{name}{RESET}"


def run_git(directory: str, *args: str):
    try:
        result = subprocess.run(
            ["git", "-C", directory, *args],
            capture_output=True,
            text=True,
            timeout=GIT_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def git_branch_segment(data: dict) -> str:
    workspace = data.get("workspace") or {}
    directory = workspace.get("current_dir") or data.get("cwd")
    if not directory:
        return None
    branch = run_git(directory, "branch", "--show-current")
    if not branch:
        branch = run_git(directory, "rev-parse", "--short", "HEAD")
    if not branch:
        return None
    return f"🌿 {branch}"


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        data = {}

    segments = [
        fn(data)
        for fn in (
            model_segment,
            git_branch_segment,
            context_segment,
            cost_segment,
            duration_segment,
        )
    ]
    print(SEP.join(s for s in segments if s))


if __name__ == "__main__":
    main()
