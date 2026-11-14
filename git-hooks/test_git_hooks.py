#!/usr/bin/env python3
"""Run the global git hooks against throwaway repos. python3 ~/.claude/git-hooks/test_git_hooks.py"""
import os, random, string, subprocess, sys, tempfile

HOOKS = os.path.dirname(os.path.abspath(__file__))
TERM = 'wib' + 'ey'  # a private term, split so this file passes its own check
TOKEN = 'ghp_' + ''.join(random.choices(string.ascii_letters + string.digits, k=36))


def git(cwd, *args, env=None):
    return subprocess.run(['git', '-C', cwd, *args], capture_output=True, text=True,
                          env={**os.environ, **(env or {})})


def commit(repo, name, text):
    open(os.path.join(repo, name), 'w').write(text + '\n')
    git(repo, 'add', name)
    return git(repo, 'commit', '-q', '-m', f'add {name}').returncode == 0


def main():
    tmp = tempfile.mkdtemp()
    remote, repo = os.path.join(tmp, 'remote.git'), os.path.join(tmp, 'work')
    subprocess.run(['git', 'init', '-q', '--bare', remote])
    subprocess.run(['git', 'init', '-q', '-b', 'main', repo])
    for k, v in [('core.hooksPath', HOOKS), ('user.name', 't'), ('user.email', 't@t'),
                 ('commit.gpgsign', 'false')]:
        git(repo, 'config', k, v)
    git(repo, 'remote', 'add', 'origin', remote)

    def push(vis):
        return git(repo, 'push', '-q', 'origin', 'main', env={'PRIVACY_VISIBILITY': vis}).returncode == 0

    checks = [
        ('commit: clean passes', commit(repo, 'a.txt', 'hello'), True),
        ('commit: secret blocked', commit(repo, 'b.txt', f'token = "{TOKEN}"'), False),
    ]
    git(repo, 'reset', '-q', 'b.txt')
    checks.append(('push public: clean passes', push('public'), True))
    commit(repo, 'c.txt', f'notes from the {TERM} case')
    checks += [
        ('push public: private term blocked', push('public'), False),
        ('push unknown visibility: blocked', push('unknown'), False),
        ('push private: private term passes', push('private'), True),
    ]
    failed = [name for name, got, want in checks if got != want]
    for name, got, want in checks:
        print(('ok   ' if got == want else 'FAIL ') + name)
    print(f'{len(checks) - len(failed)}/{len(checks)} passed')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
