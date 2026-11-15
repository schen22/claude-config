#!/usr/bin/env python3
"""Run the global git hooks against throwaway repos. python3 ~/.claude/git-hooks/test_git_hooks.py"""
import os, random, shutil, string, subprocess, sys, tempfile

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
    git(repo, 'reset', '-q', '--hard', 'HEAD~1')
    open(os.path.join(repo, 'd.txt'), 'w').write('fine\n'); git(repo, 'add', 'd.txt')
    git(repo, 'commit', '-q', '-m', f'notes from the {TERM} case')
    checks.append(('push public: private term in message blocked', push('public'), False))
    checks += publish_checks(tmp)
    failed = [name for name, got, want in checks if got != want]
    for name, got, want in checks:
        print(('ok   ' if got == want else 'FAIL ') + name)
    print(f'{len(checks) - len(failed)}/{len(checks)} passed')
    return 1 if failed else 0


def publish_checks(tmp):
    """Pushing the setup repo's main exports it and pushes the public clone; a leak blocks both."""
    real = os.path.expanduser('~/.claude')
    src, priv, pub, dest = (os.path.join(tmp, n) for n in ('src', 'priv.git', 'pub.git', 'dest'))
    for bare in (priv, pub):
        subprocess.run(['git', 'init', '-q', '--bare', '-b', 'main', bare])
    subprocess.run(['git', 'init', '-q', '-b', 'main', src])
    subprocess.run(['git', 'clone', '-q', pub, dest], capture_output=True)
    for r in (src, dest):
        for k, v in [('core.hooksPath', HOOKS), ('user.name', 't'), ('user.email', 't@t'), ('commit.gpgsign', 'false')]:
            git(r, 'config', k, v)
    os.makedirs(os.path.join(src, 'scripts'))
    for f in ('scripts/export_public.py', 'scripts/private-terms.txt'):
        shutil.copy(os.path.join(real, f), os.path.join(src, f))
    open(os.path.join(src, 'README.md'), 'w').write('# test\n')
    open(os.path.join(src, 'CLAUDE.md'), 'w').write('rules\n')
    git(src, 'add', '-A'); git(src, 'commit', '-q', '-m', 'init'); git(src, 'remote', 'add', 'origin', priv)
    env = {'CLAUDE_CONFIG_SRC': src, 'CLAUDE_CONFIG_PUBLIC': dest, 'PRIVACY_VISIBILITY': 'private'}
    ok = git(src, 'push', '-q', 'origin', 'main', env=env).returncode == 0
    published = 'CLAUDE.md' in git(pub, 'ls-tree', '--name-only', 'main').stdout
    open(os.path.join(src, 'CLAUDE.md'), 'a').write(f'from the {TERM} case\n')
    git(src, 'commit', '-qam', 'leak')
    blocked = git(src, 'push', '-q', 'origin', 'main', env=env).returncode != 0
    clean_pub = TERM not in git(pub, 'show', 'main:CLAUDE.md').stdout
    return [('publish: push of setup publishes it', ok and published, True),
            ('publish: leak blocks private push', blocked, True),
            ('publish: leak never reaches public', clean_pub, True)]


if __name__ == '__main__':
    sys.exit(main())
