#!/usr/bin/env python3
"""SubagentStop: append one line per finished subagent to ~/.claude/logs/agents.jsonl.

Never blocks. Feeds the monthly review of which helpers were expensive and why.
"""
import json, os, sys, time

LEDGER = os.environ.get('CLAUDE_AGENT_LEDGER', os.path.expanduser('~/.claude/logs/agents.jsonl'))

ev = json.load(sys.stdin)
path = os.path.expanduser(ev.get('agent_transcript_path') or '')
reqs, model = {}, None
try:
    for line in open(path, errors='ignore'):
        if '"usage"' not in line:
            continue
        try:
            d = json.loads(line)
        except ValueError:
            continue
        m = d.get('message') or {}
        u = m.get('usage') or {}
        model = m.get('model', model)
        reqs[d.get('requestId') or d.get('uuid')] = (
            u.get('input_tokens', 0) + u.get('cache_read_input_tokens', 0)
            + u.get('cache_creation_input_tokens', 0), u.get('output_tokens', 0))
except OSError:
    sys.exit(0)
if not reqs:
    sys.exit(0)

# The task description lives beside the transcript; keep it so a row still says what the
# helper did after transcripts are cleaned up.
try:
    desc = json.load(open(path[:-len('.jsonl')] + '.meta.json')).get('description', '')
except (OSError, ValueError):
    desc = ''

ctx = [c for c, _ in reqs.values()]
row = dict(ts=time.strftime('%Y-%m-%dT%H:%M:%S'), project=os.path.basename(ev.get('cwd', '')),
           agent_type=ev.get('agent_type'), agent_id=ev.get('agent_id'), desc=desc, model=model,
           steps=len(ctx), first_k=ctx[0] // 1000, peak_k=max(ctx) // 1000,
           processed_k=sum(ctx) // 1000, output_k=sum(o for _, o in reqs.values()) // 1000)
os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
with open(LEDGER, 'a') as f:
    f.write(json.dumps(row) + '\n')
