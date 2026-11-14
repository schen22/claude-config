#!/usr/bin/env python3
"""One row per session in ~/.claude/logs/sessions.jsonl — the retro's main evidence.

    session-log.py                 # SessionEnd hook: facts (commits, tokens, helpers, denies)
    session-log.py --note --goal G --wrong W --lessons L   # /end: the judgement, same folder
    session-log.py --last          # /start: the last session in this folder
    session-log.py --since <ts>    # retro scan: every session since <ts>, one line each
    session-log.py --helpers       # /end: this folder's helpers in the last 24h

A note is joined to its session by folder and time (note written before the session ends),
so /end needs no session id. Never blocks.
"""
import calendar, json, os, subprocess, sys, time

HOME = os.path.expanduser('~/.claude')
LOG = os.environ.get('CLAUDE_SESSION_LOG', f'{HOME}/logs/sessions.jsonl')
LEDGER = os.environ.get('CLAUDE_AGENT_LEDGER', f'{HOME}/logs/agents.jsonl')
HOOKS = os.environ.get('CLAUDE_HOOK_LOG', f'{HOME}/logs/hooks.jsonl')
NOW = time.strftime('%Y-%m-%dT%H:%M:%S')
HERE = os.path.realpath(os.getcwd())  # macOS: /var → /private/var, so compare real paths


def rows(path):
    try:
        return [json.loads(l) for l in open(path) if l.strip()]
    except OSError:
        return []


def append(row):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, 'a') as f:
        f.write(json.dumps(row) + '\n')


def arg(name):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else ''


def sessions(cwd=None):
    """Session rows with their note merged in, oldest first."""
    all_rows = rows(LOG)
    notes = [r for r in all_rows if r.get('kind') == 'note']
    out = []
    for s in (r for r in all_rows if r.get('kind') == 'end'):
        if cwd and s['cwd'] != cwd:
            continue
        for n in notes:
            if n['cwd'] == s['cwd'] and s['start'] <= n['ts'] <= s['ts']:
                s = dict(s, **{k: n[k] for k in ('goal', 'wrong', 'lessons')})
        out.append(s)
    return out


def line(s):
    cost = f"main {s['main_k']}k, {s['helpers']} helpers {s['helper_k']}k, {s['denies']} denies"
    note = ' · '.join(f"{k}: {s[k]}" for k in ('goal', 'wrong', 'lessons') if s.get(k))
    return (f"{s['ts'][:10]} {s['project']} · {len(s['commits'])} commits · {cost}"
            + (f" · {note}" if note else ' · no /end note'))


if '--note' in sys.argv:
    append(dict(kind='note', ts=NOW, cwd=HERE, goal=arg('--goal'), wrong=arg('--wrong'),
                lessons=arg('--lessons')))
    print('note saved')
elif '--last' in sys.argv:
    s = sessions(HERE)
    print(line(s[-1]) + ''.join(f"\n  {c}" for c in s[-1]['commits']) if s else
          'No earlier session logged in this folder.')
elif '--since' in sys.argv:
    recent = [s for s in sessions() if s['ts'] >= arg('--since')]
    for s in recent:
        print('  ' + line(s))
    print(f"  {len(recent)} sessions, {sum(bool(s.get('goal')) for s in recent)} with an /end note"
          if recent else '  No sessions logged yet.')
elif '--helpers' in sys.argv:
    day = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(time.time() - 86400))
    last = {r.get('agent_id'): r for r in rows(LEDGER)}  # rows are running totals
    mine = [r for r in last.values() if r['project'] == os.path.basename(HERE) and r['ts'] >= day]
    for r in mine:
        print(f"  {r['agent_type']} · {r['steps']} steps · peak {r['peak_k']}k · {r['processed_k']}k · {r.get('desc', '')}")
    print(f"{len(mine)} helpers, {sum(r['processed_k'] for r in mine)}k processed")
else:
    ev = json.load(sys.stdin)
    cwd, tr = os.path.realpath(ev.get('cwd') or '.'), os.path.expanduser(ev.get('transcript_path') or '')
    start, reqs = NOW, {}
    try:
        for l in open(tr, errors='ignore'):
            try:
                d = json.loads(l)
            except ValueError:
                continue
            if d.get('timestamp') and start == NOW:
                # Transcript times are UTC; the logs use local time.
                t = calendar.timegm(time.strptime(d['timestamp'][:19], '%Y-%m-%dT%H:%M:%S'))
                start = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(t))
            u = (d.get('message') or {}).get('usage')
            if u:
                reqs[d.get('requestId') or d.get('uuid')] = (u.get('input_tokens', 0)
                    + u.get('cache_read_input_tokens', 0) + u.get('cache_creation_input_tokens', 0))
    except OSError:
        pass
    git = subprocess.run(['git', '-C', cwd, 'log', f'--since={start}', '--format=%h %s'],
                         capture_output=True, text=True)
    last = {r.get('agent_id'): r for r in rows(LEDGER)}
    helpers = [r for r in last.values() if r['project'] == os.path.basename(cwd) and r['ts'] >= start]
    append(dict(kind='end', ts=NOW, start=start, session_id=ev.get('session_id'), cwd=cwd,
                project=os.path.basename(cwd), reason=ev.get('reason'),
                commits=git.stdout.strip().split('\n')[:10] if git.returncode == 0 and git.stdout.strip() else [],
                main_k=sum(reqs.values()) // 1000, helpers=len(helpers),
                helper_k=sum(r['processed_k'] for r in helpers),
                denies=sum(r['decision'] == 'deny' and r['ts'] >= start for r in rows(HOOKS))))
