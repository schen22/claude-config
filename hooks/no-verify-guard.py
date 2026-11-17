#!/usr/bin/env python3
"""PreToolUse on Bash, main session and subagents alike.

Denies skipping git hooks: `--no-verify`, `git commit -n` (any short-flag cluster with n),
and `git -c core.hooksPath=…`. The pre-commit hooks are the gate an agent must not route
around. Sarah bypasses by running the command herself (`! git commit --no-verify …`).
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from hooklib import read_event, deny

HOOK = 'no-verify-guard'
QUOTED = re.compile(r'"(?:\\.|[^"\\])*"|\'[^\']*\'')   # message text can say anything
SEGMENT = re.compile(r'[;&|\n]+')
NO_VERIFY = re.compile(r'(^|\s)--no-verify\b')
COMMIT_N = re.compile(r'\bcommit\b.*\s-[a-zA-Z]*n[a-zA-Z]*(\s|$)')
HOOKS_PATH = re.compile(r'\bgit\s+(-\S+\s+)*-c\s*core\.hookspath', re.I)

ev = read_event()
if ev.get('tool_name') != 'Bash':
    sys.exit(0)
cmd = QUOTED.sub('""', (ev.get('tool_input') or {}).get('command', ''))
for seg in SEGMENT.split(cmd):
    if not re.search(r'\bgit\b', seg):
        continue
    if NO_VERIFY.search(seg) or COMMIT_N.search(seg) or HOOKS_PATH.search(seg):
        deny(HOOK, 'Skipping git hooks is Sarah\'s call, not an agent\'s. Fix what the hook '
             'reports (run the gate), or ask Sarah to run the command herself with `!`.',
             command=cmd[:200])
sys.exit(0)
