#!/usr/bin/env python3
"""PreToolUse on every tool, acting only inside subagents (the event has an agent_id).

1. Budget: past BUDGET tokens of context, only wrap-up calls are allowed
   (git, the gate, the final report) — commit what's green, report, stop.
2. Tests: raw full-suite runs are denied when the project has a gate script.
3. Images: reading .png/.jpg/... is denied — compare hashes instead.
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from hooklib import read_event, deny, log, last_context_tokens

HOOK = 'helper-guard'
BUDGET = 150_000
WRAP_UP_TOOLS = {'SubagentHandback', 'SendMessage'}
WRAP_UP_BASH = re.compile(r'^\s*(git |npm run -?s? ?gate)')
RAW_TEST = re.compile(r'\b(npm (run )?test|node --test)\b')
IMAGE = re.compile(r'\.(png|jpe?g|gif|webp)$', re.I)

ev = read_event()
agent = ev.get('agent_id')
if not agent:
    sys.exit(0)                                   # main session: never touched

tool = ev.get('tool_name', '')
ti = ev.get('tool_input') or {}
cmd = ti.get('command', '') if tool == 'Bash' else ''
meta = dict(agent_id=agent, tool=tool)

# 1. Budget. The transcript may lag one turn; close enough for a 150k line.
path = ev.get('transcript_path', '')
if not os.path.basename(path).startswith('agent-'):
    path = os.path.join(os.path.dirname(path), ev.get('session_id', ''),
                        'subagents', f'agent-{agent}.jsonl')
ctx = last_context_tokens(path)
if ctx > BUDGET and tool not in WRAP_UP_TOOLS and not WRAP_UP_BASH.match(cmd):
    deny(HOOK, f'Context is {ctx // 1000}k (budget {BUDGET // 1000}k). Wrap up: commit what '
         'passes the gate on your lane branch, then report in <= 15 lines (done / left / '
         'uncommitted) and stop.', ctx=ctx, **meta)

# 2. Raw full-suite test runs, when the project has gate scripts.
if cmd and RAW_TEST.search(cmd) and '--test-name-pattern' not in cmd:
    try:
        scripts = json.load(open(os.path.join(ev.get('cwd', '.'), 'package.json'))).get('scripts', {})
    except (OSError, ValueError):
        scripts = {}
    if 'gate' in scripts:
        deny(HOOK, 'Use `npm run gate:fast` while iterating and `npm run gate` before a '
             'commit (filtered output). To prove one test fails, run it alone with '
             '`--test-name-pattern`.', cmd=cmd[:200], **meta)

# 3. Screenshots and other images.
if tool == 'Read' and IMAGE.search(ti.get('file_path', '')):
    deny(HOOK, 'No screenshots or images in helpers. Compare files by hash (`shasum`) or '
         'assert computed values; the visual call is the user\'s.',
         file=ti.get('file_path'), **meta)

sys.exit(0)
