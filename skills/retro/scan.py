#!/usr/bin/env python3
"""Retro scan: repeated prompts, lessons stuck in local memory, hook and helper logs.

    python3 ~/.claude/skills/retro/scan.py [--days 60]

Read-only. Token usage by project/session lives in the session-report plugin.
"""
import collections, glob, json, os, re, subprocess, sys, time

HOME = os.path.expanduser('~/.claude')
DAYS = int(sys.argv[sys.argv.index('--days') + 1]) if '--days' in sys.argv else 60
since_ms = (time.time() - DAYS * 86400) * 1000
STOP = set('the a an to and of in for on is it this that i we you be with as at by or '
           'from are can do not use so if my me our its make what how all'.split())
NOISE = re.compile(r'sarahchen|users|documents|https?|claude\.ai|\.jsonl?|tool calls')  # paths, pasted text

# 1. Repeated prompts: 4-word phrases shared by 3+ distinct prompts.
prompts = []
for line in open(f'{HOME}/history.jsonl', errors='ignore'):
    try:
        d = json.loads(line)
    except ValueError:
        continue
    text = (d.get('display') or '').strip()
    if float(d.get('timestamp') or 0) < since_ms or not text or re.fullmatch(r'/\S+', text):
        continue
    prompts.append((os.path.basename(d.get('project') or ''), text))

seen = collections.defaultdict(set)          # phrase -> {(project, prompt index)}
for i, (proj, text) in enumerate(prompts):
    words = re.findall(r"[a-z0-9'.-]+", text.lower())
    for j in range(len(words) - 3):
        gram = words[j:j + 4]
        if sum(w not in STOP for w in gram) >= 3 and not NOISE.search(' '.join(gram)):
            seen[' '.join(gram)].add((proj, i))
repeats = sorted(((len(v), len({p for p, _ in v}), k) for k, v in seen.items() if len(v) >= 3),
                 reverse=True)
print(f'## Repeated phrases (last {DAYS} days, {len(prompts)} prompts)')
shown = []
for n, projects, phrase in repeats:
    if any(phrase in s or s in phrase for s in shown):
        continue
    shown.append(phrase)
    print(f'  {n:3} prompts · {projects} projects · "{phrase}"')
    if len(shown) == 12:
        break

# 2. Lessons stuck in one folder's local memory.
print('\n## Local memories (only load in their own folder)')
for f in sorted(glob.glob(f'{HOME}/projects/*/memory/*.md')):
    if f.endswith('MEMORY.md'):
        continue
    head = open(f, errors='ignore').read(1500)
    kind = (re.search(r'^\s*type:\s*(\w+)', head, re.M) or [None, '?'])[1]
    desc = (re.search(r'description:\s*"?(.+?)"?\s*$', head, re.M) or [None, ''])[1]
    proj = f.split('/projects/')[1].split('/')[0].replace('-Users-sarahchen-Documents-', '')
    print(f'  [{kind}] {proj}: {os.path.basename(f)} — {desc[:100]}')

# 3. Hooks: what they blocked or would have blocked.
print('\n## Hooks')
print(subprocess.run([sys.executable, f'{HOME}/hooks/hook-review.py'],
                     capture_output=True, text=True).stdout.rstrip())

# 4. Helpers: the costliest finished subagents.
print('\n## Costliest helpers (usage ledger)')
ledger = f'{HOME}/logs/agents.jsonl'
rows = [json.loads(l) for l in open(ledger)] if os.path.exists(ledger) else []
for r in sorted(rows, key=lambda r: -r['processed_k'])[:5]:
    print(f"  {r['ts'][:10]} {r['project']}: {r['agent_type']} {r['model']} · {r['steps']} steps · "
          f"peak {r['peak_k']}k · {r['processed_k']}k processed")
if not rows:
    print('  No helpers logged yet.')
