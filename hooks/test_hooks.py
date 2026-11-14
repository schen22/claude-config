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

# Ledger row carries the task description from the transcript's .meta.json.
tr = f'{tmp}/agent-t1.jsonl'
with open(tr, 'w') as f:
    f.write(json.dumps({'requestId': 'r1', 'message': {'model': 'm', 'usage': {'input_tokens': 30000, 'output_tokens': 10}}}) + '\n')
json.dump({'description': 'Verify ledger row M-16'}, open(f'{tmp}/agent-t1.meta.json', 'w'))
ledger = f'{tmp}/agents-desc.jsonl'
subprocess.run([sys.executable, '-S', f'{HERE}/usage-ledger.py'], env=dict(ENV, CLAUDE_AGENT_LEDGER=ledger),
               input=json.dumps({'agent_transcript_path': tr, 'agent_id': 't1', 'cwd': '/x/p'}), capture_output=True, text=True)
row = json.loads(open(ledger).read()) if os.path.exists(ledger) else {}
ok = row.get('desc') == 'Verify ledger row M-16' and row.get('first_k') == 30
CASES.append(('ledger row has desc', 'usage-ledger', {}, None))
fails += not ok
print(f"{'ok  ' if ok else 'FAIL'} {'usage-ledger':13} ledger row has desc" + ('' if ok else f'  {row}'))

# Session log: the SessionEnd row counts the transcript's tokens, and --last joins the /end note.
slog, proj = f'{tmp}/sessions.jsonl', f'{tmp}/proj'
os.makedirs(proj)
tr = f'{tmp}/session.jsonl'
with open(tr, 'w') as f:
    f.write(json.dumps({'timestamp': '2020-01-01T00:00:00.000Z', 'requestId': 'r1',
                        'message': {'usage': {'input_tokens': 5000, 'cache_read_input_tokens': 40000}}}) + '\n')
SENV = dict(ENV, CLAUDE_SESSION_LOG=slog)
run = lambda *a, **k: subprocess.run([sys.executable, '-S', f'{HERE}/session-log.py', *a], env=SENV,
                                     cwd=proj, capture_output=True, text=True, **k)
run('--note', '--goal', 'G1', '--wrong', 'none', '--lessons', 'none')
run(input=json.dumps({'session_id': 's1', 'transcript_path': tr, 'cwd': proj, 'reason': 'exit'}))
last = run('--last').stdout
ok = 'main 45k' in last and 'goal: G1' in last and '1 with an /end note' in run('--since', '2000-01-01').stdout
CASES.append(('session row + note', 'session-log', {}, None))
fails += not ok
print(f"{'ok  ' if ok else 'FAIL'} {'session-log':13} session row + note" + ('' if ok else f'  {last!r}'))

# due.py: a past retro date is due; a hook-review date is silent with no log-mode hook.
dfile = f'{tmp}/DUE'
open(dfile, 'w').write('retro 2000-01-01\nhook-review 2000-01-01\n')
out = subprocess.run([sys.executable, '-S', f'{HERE}/due.py', '--session-start'], input='{}', capture_output=True,
                     text=True, env=dict(ENV, CLAUDE_DUE_FILE=dfile)).stdout
ok = 'Retro due' in out and 'Hook review' not in out
CASES.append(('retro due, hook review silent', 'due', {}, None))
fails += not ok
print(f"{'ok  ' if ok else 'FAIL'} {'due':13} retro due, hook review silent" + ('' if ok else f'  {out!r}'))

print(f'\n{len(CASES) - fails}/{len(CASES)} passed')
sys.exit(1 if fails else 0)
