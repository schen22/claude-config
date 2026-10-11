#!/usr/bin/env python3
"""python3 tests/test_write_scope.py — runs the write-scope hook on sample events."""
import json, os, subprocess, sys, tempfile

HOOK = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'hooks', 'write-scope.py')
tmp = tempfile.mkdtemp()
P = os.path.join(tmp, 'proj')
os.makedirs(os.path.join(P, 'references'))
ENV = dict(os.environ, CLAUDE_HOOK_LOG=os.path.join(tmp, 'hooks.jsonl'))


def ev(agent_type, path, tool='Write', **kw):
    return dict(dict(agent_id='a1', agent_type=agent_type, tool_name=tool, cwd=P,
                     tool_input={'file_path': path}), **kw)


CASES = [  # (name, event, expect_deny)
    ('role writes own report', ev('research-round:ux-researcher', 'references/waste-ux-researcher.md'), False),
    ('role, absolute path', ev('research-round:ux-researcher', f'{P}/references/waste-ux-researcher.md'), False),
    ("role writes another role's report", ev('research-round:ux-researcher', 'references/waste-architect.md'), True),
    ('role writes CLAUDE.md', ev('research-round:data-scientist', 'CLAUDE.md'), True),
    ('role escapes with ..', ev('research-round:ux-researcher', 'references/../../x-ux-researcher.md'), True),
    ('role writes into a subfolder', ev('research-round:ux-researcher', 'references/sub/waste-ux-researcher.md'), True),
    ('fact-checker edits a report', ev('research-round:fact-checker', 'references/waste-architect.md', 'Edit'), False),
    ('fact-checker edits a recipe', ev('research-round:fact-checker', 'recipes/oyakodon.md', 'Edit'), True),
    ('synthesizer writes its proposal', ev('research-round:synthesizer', 'proposals/waste.md'), False),
    ('synthesizer writes root PROPOSAL.md', ev('research-round:synthesizer', 'PROPOSAL.md'), True),
    ('strategy role writes own report', ev('research-round:competitive-analyst', 'references/eu-competitive-analyst.md'), False),
    ('staff engineer writes own report', ev('research-round:staff-software-engineer', 'references/eu-staff-software-engineer.md'), False),
    ('staff engineer writes architect report', ev('research-round:staff-software-engineer', 'references/eu-architect.md'), True),
    ('synthesizer writes PLAN.md', ev('research-round:synthesizer', 'PLAN.md'), True),
    ('overseer writes anything', ev('research-round:overseer', 'references/x-overseer.md'), True),
    ('other agent untouched', ev('general-purpose', 'CLAUDE.md'), False),
    ('main session untouched', {'tool_name': 'Write', 'cwd': P, 'tool_input': {'file_path': 'CLAUDE.md'}}, False),
    ('subagent without type: allowed, logged', {'agent_id': 'w1', 'tool_name': 'Write', 'cwd': P, 'tool_input': {'file_path': 'CLAUDE.md'}}, False),
]

fails = 0
for name, event, expect in CASES:
    out = subprocess.run([sys.executable, '-S', HOOK], input=json.dumps(event), capture_output=True, text=True, env=ENV)
    denied = '"deny"' in out.stdout
    ok = denied == expect and out.returncode == 0
    fails += not ok
    print(f"{'ok  ' if ok else 'FAIL'} {name}" + ('' if ok else f'  rc={out.returncode} {out.stdout[:200]} {out.stderr[:300]}'))
print(f'\n{len(CASES) - fails}/{len(CASES)} passed')
sys.exit(1 if fails else 0)
