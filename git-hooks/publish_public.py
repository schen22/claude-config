#!/usr/bin/env python3
"""Publish ~/.claude to the public claude-config repo. Run by pre-push when ~/.claude main is pushed.

Exports (scripts/export_public.py: committed files only, private terms and README gaps block),
then commits and pushes the public clone if anything changed. The commit message lists files only,
so private commit subjects never reach the public repo. Exit 0 = published or already up to date.
Env (tests): CLAUDE_CONFIG_SRC, CLAUDE_CONFIG_PUBLIC.
"""
import os, subprocess, sys

SRC = os.path.expanduser(os.environ.get('CLAUDE_CONFIG_SRC', '~/.claude'))
DEST = os.path.expanduser(os.environ.get('CLAUDE_CONFIG_PUBLIC', '~/Documents/projects/claude-config-public'))


def git(*args):
    return subprocess.run(['git', '-C', DEST, *args], capture_output=True, text=True)


def main():
    if subprocess.run([sys.executable, os.path.join(SRC, 'scripts', 'export_public.py'), DEST],
                      capture_output=True, text=True).returncode:
        # rerun visibly so the reason shows
        subprocess.run([sys.executable, os.path.join(SRC, 'scripts', 'export_public.py'), DEST])
        return 1
    git('add', '-A')
    changed = git('diff', '--cached', '--name-only').stdout.split()
    if not changed:
        print('claude-config: already up to date.')
        return 0
    names = ', '.join(changed[:8]) + (f' and {len(changed) - 8} more' if len(changed) > 8 else '')
    msg = f'Sync from my private setup\n\nChanged: {names}.\n\nExported by scripts/export_public.py.'
    if git('commit', '-q', '-m', msg).returncode:
        print('claude-config: commit failed.', file=sys.stderr)
        return 1
    push = subprocess.run(['git', '-C', DEST, 'push', '-q', 'origin', 'HEAD:main'])
    if push.returncode:
        git('reset', '-q', '--soft', 'HEAD~1')  # keep the export staged; nothing half-published
        return 1
    print(f'claude-config: published {len(changed)} changed file(s).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
