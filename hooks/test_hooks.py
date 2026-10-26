#!/usr/bin/env python3
"""Run each hook against sample events, in enforce mode, with a throwaway log.

    python3 ~/.claude/hooks/test_hooks.py
"""
import glob, json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
tmp = tempfile.mkdtemp()
ENV = dict(os.environ, CLAUDE_HOOK_MODE='enforce', CLAUDE_HOOK_LOG=f'{tmp}/hooks.jsonl',
           CLAUDE_AGENT_LEDGER=f'{tmp}/agents.jsonl')

CASES = [
    # (name, hook, event, expect_deny)
    ('main session untouched', 'helper-guard', {'tool_name': 'Bash', 'tool_input': {'command': 'npm test'}}, False),
    ('helper raw npm test', 'helper-guard', {'agent_id': 'x', 'cwd': os.path.expanduser('~/Documents/projects/sarahs-corner'), 'tool_name': 'Bash', 'tool_input': {'command': 'npm test 2>&1 | tail -100'}}, True),
    ('helper single test', 'helper-guard', {'agent_id': 'x', 'cwd': os.path.expanduser('~/Documents/projects/sarahs-corner'), 'tool_name': 'Bash', 'tool_input': {'command': 'node --test --test-name-pattern "toggle" test/interaction.test.js'}}, False),
    ('helper gate', 'helper-guard', {'agent_id': 'x', 'cwd': os.path.expanduser('~/Documents/projects/sarahs-corner'), 'tool_name': 'Bash', 'tool_input': {'command': 'npm run gate:fast'}}, False),
    ('helper screenshot', 'helper-guard', {'agent_id': 'x', 'tool_name': 'Read', 'tool_input': {'file_path': '/tmp/shot.png'}}, True),
]

# Replay the real 202k lane H transcript, if it is still on disk.
lane_h = glob.glob(os.path.expanduser('~/.claude/projects/*sarahs-corner/*/subagents/agent-a00f21973ff46d8f6.jsonl'))
if lane_h:
    ev = {'agent_id': 'a00f21973ff46d8f6', 'transcript_path': lane_h[0], 'tool_name': 'Edit', 'tool_input': {}}
    CASES += [('over budget: Edit', 'helper-guard', ev, True),
              ('over budget: git commit', 'helper-guard', dict(ev, tool_name='Bash', tool_input={'command': 'git commit -m x'}), False)]

fails = 0
for name, hook, event, expect in CASES:
    out = subprocess.run([sys.executable, "-S", f'{HERE}/{hook}.py'], input=json.dumps(event),
                         capture_output=True, text=True, env=ENV)
    denied = '"deny"' in out.stdout
    ok = denied == expect and out.returncode == 0
    fails += not ok
    print(f"{'ok  ' if ok else 'FAIL'} {hook:13} {name}" + ('' if ok else f'  rc={out.returncode} {out.stdout[:200]} {out.stderr[:300]}'))

if lane_h:
    out = subprocess.run([sys.executable, "-S", f'{HERE}/usage-ledger.py'], env=ENV, capture_output=True, text=True,
                         input=json.dumps({'agent_transcript_path': lane_h[0], 'agent_type': 'general-purpose', 'cwd': '/x/sarahs-corner'}))
    print('ledger row:', open(f'{tmp}/agents.jsonl').read().strip() if os.path.exists(f'{tmp}/agents.jsonl') else out.stderr)

print(f'\n{len(CASES) - fails}/{len(CASES)} passed')
sys.exit(1 if fails else 0)
