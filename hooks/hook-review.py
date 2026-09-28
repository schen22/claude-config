#!/usr/bin/env python3
"""Summarise ~/.claude/logs/hooks.jsonl, and nag until the log-only trial is reviewed.

    python3 ~/.claude/hooks/hook-review.py                  # print the report
    python3 ~/.claude/hooks/hook-review.py --session-start  # SessionStart hook

As a SessionStart hook it stays silent until the date in REVIEW_DUE, then — while any
hook in settings.json still runs with CLAUDE_HOOK_MODE=log — it asks Claude to raise
the review with Sarah at the start of every session. To finish the review: switch the
hooks to enforce (or remove them), or push the date in REVIEW_DUE forward.
"""
import collections, datetime, json, os, sys

HOME = os.path.expanduser('~/.claude')
LOG = os.environ.get('CLAUDE_HOOK_LOG', f'{HOME}/logs/hooks.jsonl')
DUE_FILE = f'{HOME}/hooks/REVIEW_DUE'
SETTINGS = f'{HOME}/settings.json'


def report():
    rows = []
    if os.path.exists(LOG):
        rows = [json.loads(l) for l in open(LOG) if l.strip()]
    if not rows:
        return 'No hook decisions logged yet.'
    by = collections.Counter((r['hook'], r['decision']) for r in rows)
    reasons = collections.Counter((r['hook'], r['reason'][:110]) for r in rows
                                  if r['decision'] in ('deny', 'would-deny'))
    lines = [f"Hook log {rows[0]['ts'][:10]} → {rows[-1]['ts'][:10]}, {len(rows)} decisions:"]
    lines += [f'  {h:13} {d:11} {n}' for (h, d), n in sorted(by.items())]
    lines += ['Top would-deny reasons:'] + [f'  {n}× {h}: {r}' for (h, r), n in reasons.most_common(5)]
    return '\n'.join(lines)


def still_log_mode():
    try:
        return 'CLAUDE_HOOK_MODE=log' in open(SETTINGS).read()
    except OSError:
        return False


if '--session-start' in sys.argv:
    json.load(sys.stdin)
    try:
        due = datetime.date.fromisoformat(open(DUE_FILE).read().strip())
    except (OSError, ValueError):
        sys.exit(0)
    if datetime.date.today() < due or not still_log_mode():
        sys.exit(0)
    msg = (f'HOOK REVIEW DUE (since {due}). Before other work, tell Sarah the log-only hook '
           'trial is ready for review, show this summary, and propose: switch each hook to '
           'enforce, adjust it, or remove it. Run `python3 ~/.claude/hooks/hook-review.py` '
           'for the full report.\n' + report())
    print(json.dumps({'hookSpecificOutput': {'hookEventName': 'SessionStart',
                                             'additionalContext': msg[:9000]}}))
else:
    print(report())
