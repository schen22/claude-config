"""Shared helpers for Sarah's Claude Code hooks.

Every hook reads the event JSON on stdin, logs its decision, and in 'enforce' mode can
deny a tool call. In 'log' mode (the default) it only records what it *would* deny.
A crash exits non-zero, which Claude Code treats as a non-blocking error: the call
still goes ahead, so a broken hook never locks you out.
"""
import json, os, sys, time

LOG = os.environ.get('CLAUDE_HOOK_LOG', os.path.expanduser('~/.claude/logs/hooks.jsonl'))
MODE = os.environ.get('CLAUDE_HOOK_MODE', 'log')  # 'log' | 'enforce'


def read_event():
    return json.load(sys.stdin)


def log(hook, decision, reason='', **extra):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    row = dict(ts=time.strftime('%Y-%m-%dT%H:%M:%S'), hook=hook, mode=MODE,
               decision=decision, reason=reason, **extra)
    with open(LOG, 'a') as f:
        f.write(json.dumps(row) + '\n')


def deny(hook, reason, **extra):
    """Block the tool call (enforce mode) or just record it (log mode). Always exits."""
    log(hook, 'deny' if MODE == 'enforce' else 'would-deny', reason, **extra)
    if MODE == 'enforce':
        print(json.dumps({'hookSpecificOutput': {
            'hookEventName': 'PreToolUse',
            'permissionDecision': 'deny',
            'permissionDecisionReason': reason}}))
    sys.exit(0)


def last_context_tokens(transcript):
    """Context size of the latest request in a transcript (reads only the file's tail)."""
    try:
        with open(transcript, 'rb') as f:
            f.seek(0, 2); f.seek(max(0, f.tell() - 400_000))
            lines = f.read().decode('utf-8', 'ignore').splitlines()
    except OSError:
        return 0
    for line in reversed(lines):
        if '"usage"' not in line:
            continue
        try:
            u = json.loads(line)['message']['usage']
        except (ValueError, KeyError, TypeError):
            continue
        return (u.get('input_tokens', 0) + u.get('cache_read_input_tokens', 0)
                + u.get('cache_creation_input_tokens', 0))
    return 0
