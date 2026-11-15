#!/usr/bin/env python3
"""Export the committed ~/.claude setup to the public claude-config repo.

Usage: python3 ~/.claude/scripts/export_public.py [DEST]
DEST defaults to ~/Documents/projects/claude-config-public (a clone of schen22/claude-config).

Only files committed at HEAD are exported, so logs, transcripts and uncommitted work never
leave. PLAN.md (personal decisions) stays private. settings.json loses local-only keys.
Exits 1 without writing anything if a term from scripts/private-terms.txt is found. Then review `git diff` in DEST,
commit and push there.
"""
import json, os, re, shutil, subprocess, sys, tempfile

SRC = os.path.expanduser(os.environ.get('CLAUDE_CONFIG_SRC', '~/.claude'))
DEST = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else
                          os.environ.get('CLAUDE_CONFIG_PUBLIC', '~/Documents/projects/claude-config-public'))
TERMS = 'scripts/private-terms.txt'  # one regex per line; private, never exported
PRIVATE = {'PLAN.md', TERMS}
SETTINGS_DROP = {'autoMode', 'feedbackSurveyState', 'permissions'}
PUBLIC_MARKETPLACE = {'source': {'source': 'github', 'repo': 'schen22/claude-config'}}


def git(*args):
    return subprocess.run(['git', '-C', SRC, *args], check=True, capture_output=True).stdout


def sanitize_settings(raw):
    s = json.loads(raw)
    for k in SETTINGS_DROP:
        s.pop(k, None)
    for name in s.get('extraKnownMarketplaces', {}):
        s['extraKnownMarketplaces'][name] = PUBLIC_MARKETPLACE
    return (json.dumps(s, indent=2, ensure_ascii=False) + '\n').encode()


def readme_gaps(files, readme):
    """What the README's "What's here" misses, or lists that no longer exists."""
    have = {f.split('/')[1] for f in files if f.startswith('skills/') and f.count('/') == 2}
    have |= {os.path.basename(f)[:-3] for f in files if re.match(r'hooks/(?!hooklib|test_)\w+\.py$', f)}
    have |= {f.split('/')[1] for f in files if f.startswith('marketplace/') and f.count('/') >= 2}
    have |= {os.path.basename(f) for f in files if re.match(r'git-hooks/pre-\w+$', f)}
    missing = sorted(n for n in have if f'`{n}`' not in readme and f'{n}/' not in readme)
    row = next((l for l in readme.splitlines() if l.startswith('| [`skills/`]')), '')
    listed = set(re.findall(r'`([\w-]+)`', row.split('|')[2] if row.count('|') > 2 else ''))
    stale = sorted(n for n in listed if f'skills/{n}/SKILL.md' not in files)
    return [f'README misses `{n}`' for n in missing] + [f'README lists removed skill `{n}`' for n in stale]


def main():
    terms = [t for t in git('show', f'HEAD:{TERMS}').decode().splitlines() if t.strip() and not t.startswith('#')]
    deny = re.compile('|'.join(terms), re.I)
    files = [f for f in git('ls-files', '-z').decode().split('\0') if f and f not in PRIVATE]
    out, hits = {}, []
    for f in files:
        data = git('show', f'HEAD:{f}')
        if f == 'settings.json':
            data = sanitize_settings(data)
        try:
            text = data.decode()
        except UnicodeDecodeError:
            text = ''
        for n, line in enumerate(text.splitlines(), 1):
            if deny.search(line):
                hits.append(f'{f}:{n}: {line.strip()[:120]}')
        out[f] = data
    hits += readme_gaps(files, out.get('README.md', b'').decode())
    if hits:
        print('BLOCKED — private terms or README gaps found (nothing written):', *hits, sep='\n  ')
        return 1
    if not os.path.isdir(os.path.join(DEST, '.git')):
        print(f'BLOCKED — {DEST} is not a git clone of the public repo')
        return 1
    for entry in os.listdir(DEST):  # full sync: drop files no longer exported
        if entry != '.git':
            p = os.path.join(DEST, entry)
            shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    for f, data in out.items():
        p = os.path.join(DEST, f)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'wb') as fh:
            fh.write(data)
    print(f'OK — {len(out)} files exported to {DEST} (private: {", ".join(sorted(PRIVATE))}).')
    print(f'Next: git -C {DEST} diff --stat, then commit and push.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
