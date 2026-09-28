#!/usr/bin/env python3
"""PreToolUse on Agent: a helper brief must follow the `delegate` template.

Checks only general-purpose / claude / unnamed agents — custom agents (Explore, Plan,
your project agents) carry their own instructions, and forks inherit context.
"""
import re, sys
sys.path.insert(0, __import__('os').path.dirname(__file__))
from hooklib import read_event, deny, log

HOOK = 'brief-check'
CHECKED_TYPES = {'', 'general-purpose', 'claude'}
FULL = ['Goal', 'Owns', 'Snippets', 'Gate', 'Report']
READ_ONLY = ['Goal', 'Report']          # briefs marked "## Read-only" (research, search)
EXPENSIVE_MODELS = ('opus', 'fable')
LONG_BRIEF_CHARS = 16_000               # ~4k tokens: logged as a warning, never blocked


def section(prompt, name):
    m = re.search(rf'^## {name}\b[^\n]*\n(.*?)(?=^## |\Z)', prompt, re.M | re.S)
    return m.group(1).strip() if m else None


ev = read_event()
ti = ev.get('tool_input') or {}
kind = ti.get('subagent_type') or ''
if kind not in CHECKED_TYPES:
    sys.exit(0)

prompt = ti.get('prompt') or ''
required = READ_ONLY if re.search(r'^## Read-only\b', prompt, re.M) else FULL
problems = [f'"## {s}" missing or empty' for s in required if not section(prompt, s)]

model = (ti.get('model') or '').lower()
if model.startswith(EXPENSIVE_MODELS) and section(prompt, 'Why this model') is None:
    problems.append(f'model "{model}" needs a "## Why this model" line (default is sonnet)')

meta = dict(agent=kind, model=model, chars=len(prompt), desc=ti.get('description', ''))
if problems:
    deny(HOOK, 'Brief: ' + '; '.join(problems)
         + '. Load the `delegate` skill and use its brief template.', **meta)
log(HOOK, 'warn-long' if len(prompt) > LONG_BRIEF_CHARS else 'allow', **meta)
