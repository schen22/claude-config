#!/usr/bin/env python3
"""What's due: the retro and the hook review, from dates in ~/.claude/hooks/DUE.

    python3 ~/.claude/hooks/due.py                  # print what's due (/start)
    python3 ~/.claude/hooks/due.py --hooks          # hook log report (retro scan)
    python3 ~/.claude/hooks/due.py --session-start  # SessionStart hook

DUE holds one `<item> <YYYY-MM-DD>` per line (`retro`, `hook-review`). The hook review is
due only while a hook in settings.json runs with CLAUDE_HOOK_MODE=log. Silent when
nothing is due. Push a date forward to snooze it.
"""
import collections, datetime, json, os, sys

HOME = os.path.expanduser('~/.claude')
LOG = os.environ.get('CLAUDE_HOOK_LOG', f'{HOME}/logs/hooks.jsonl')
DUE_FILE = os.environ.get('CLAUDE_DUE_FILE', f'{HOME}/hooks/DUE')
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


def due():
    items = []
    try:
        lines = open(DUE_FILE).read().split('\n')
    except OSError:
        return items
    for l in lines:
        try:
            item, date = l.split()
            date = datetime.date.fromisoformat(date)
        except ValueError:
            continue
        if datetime.date.today() < date:
            continue
        if item == 'retro':
            items.append(f'Retro due (since {date}): run `/retro`.')
        elif item == 'hook-review' and still_log_mode():
            items.append(f'Hook review due (since {date}): propose enforce / adjust / remove for each '
                         'log-mode hook.\n' + report())
    return items


if '--hooks' in sys.argv:
    print(report())
elif '--session-start' in sys.argv:
    json.load(sys.stdin)
    items = due()
    if items:
        msg = 'DUE — tell Sarah before other work:\n' + '\n'.join(items)
        print(json.dumps({'hookSpecificOutput': {'hookEventName': 'SessionStart',
                                                 'additionalContext': msg[:9000]}}))
else:
    print('\n'.join(due()) or 'Nothing due.')
