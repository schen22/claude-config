#!/usr/bin/env python3
"""PreToolUse Write/Edit: a research-round agent may write only its own output file.

  role agent    → <cwd>/references/*-<role>.md
  fact-checker  → <cwd>/references/*.md
  synthesizer   → <cwd>/PROPOSAL.md
  anything else (overseer, unknown) → denied

Other agents and the main session are never touched. Logs to $CLAUDE_HOOK_LOG
(default ~/.claude/logs/hooks.jsonl). Fails open: a crash never blocks the call.
"""
import json, os, sys, time

HOOK = 'research-round-write-scope'
PREFIX = 'research-round:'
ROLES = {'product-designer', 'ux-researcher', 'market-researcher', 'ranking-engineer',
         'architect', 'data-scientist', 'data-engineer'}
LOG = os.environ.get('CLAUDE_HOOK_LOG', os.path.expanduser('~/.claude/logs/hooks.jsonl'))


def log(decision, reason='', **extra):
    try:
        os.makedirs(os.path.dirname(LOG), exist_ok=True)
        with open(LOG, 'a') as f:
            f.write(json.dumps(dict(ts=time.strftime('%Y-%m-%dT%H:%M:%S'), hook=HOOK,
                                    mode='enforce', decision=decision, reason=reason, **extra)) + '\n')
    except OSError:
        pass


def allowed(kind, path, cwd):
    real = os.path.realpath(os.path.join(cwd, path))
    root = os.path.realpath(cwd)
    refs = os.path.join(root, 'references')
    in_refs = os.path.dirname(real) == refs and real.endswith('.md')
    if kind in ROLES:
        return in_refs and os.path.basename(real).endswith(f'-{kind}.md')
    if kind == 'fact-checker':
        return in_refs
    if kind == 'synthesizer':
        return real == os.path.join(root, 'PROPOSAL.md')
    return False


ev = json.load(sys.stdin)
agent_type = ev.get('agent_type') or ''
if not agent_type:
    if ev.get('agent_id'):          # a subagent without a type: record it (tells us what workflows send)
        log('allow', 'subagent event has no agent_type', agent_id=ev.get('agent_id'), tool=ev.get('tool_name'))
    sys.exit(0)
if not agent_type.startswith(PREFIX):
    sys.exit(0)

kind = agent_type[len(PREFIX):]
ti = ev.get('tool_input') or {}
path = ti.get('file_path') or ti.get('notebook_path') or ''
cwd = ev.get('cwd') or os.getcwd()
meta = dict(agent_type=agent_type, agent_id=ev.get('agent_id'), tool=ev.get('tool_name'), path=path)
if path and allowed(kind, path, cwd):
    log('allow', **meta)
    sys.exit(0)

reason = (f'{agent_type} may write only its own output file '
          f'(role: references/<slug>-<role>.md, fact-checker: references/*.md, synthesizer: PROPOSAL.md), not {path or "(no path)"}.')
log('deny', reason, **meta)
print(json.dumps({'hookSpecificOutput': {'hookEventName': 'PreToolUse',
                                         'permissionDecision': 'deny',
                                         'permissionDecisionReason': reason}}))
