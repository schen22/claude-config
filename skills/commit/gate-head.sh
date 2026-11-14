#!/bin/zsh
# Run the full gate on a clean checkout of HEAD, so a commit is judged on what it
# contains, not on uncommitted files in the working tree.
#   gate-head.sh [gate command...]     default: npm run gate
# Run from the repo. Prints the gate's last 5 lines; exits with the gate's status.
set -u
repo=$(git rev-parse --show-toplevel) || exit 2
wt=$(mktemp -d "${TMPDIR:-/tmp}/gate-head.XXXXXX")/wt
git -C "$repo" worktree add -q --detach "$wt" HEAD || exit 2
[[ -d $repo/node_modules ]] && ln -s "$repo/node_modules" "$wt/node_modules"
(( $# )) || set -- npm run gate
out=$(cd "$wt" && "$@" 2>&1 </dev/null); rc=$?
git -C "$repo" worktree remove --force "$wt"
print -r -- "$out" | grep -v -e '^>' -e '^$' | tail -5
print "gate-head: $(git -C "$repo" rev-parse --short HEAD) exit $rc"
exit $rc
