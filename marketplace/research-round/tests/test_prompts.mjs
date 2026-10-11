// node tests/test_prompts.mjs — runs the workflow with stub agents, then checks every prompt it
// sent equals the matching prompts.md block filled with the same values. Also checks bad args.
import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'

const here = dirname(new URL(import.meta.url).pathname)
const src = readFileSync(join(here, '../workflows/research-round.js'), 'utf8').replace('export const meta', 'const meta')
const runWorkflow = new Function('args', 'agent', 'parallel', 'phase', 'log', `return (async () => {\n${src}\n})()`)

const blocks = {}
for (const [, name, body] of readFileSync(join(here, '../prompts.md'), 'utf8').matchAll(/^## (.+)\n[\s\S]*?```text\n([\s\S]*?)\n```/gm)) blocks[name] = body
const fill = (name, v) => blocks[name].replace(/\{(\w+)\}/g, (m, k) => (k in v ? v[k] : m))

let sent = {}
const agent = async (prompt, o) => {
  sent[o.label] = prompt
  if (o.agentType.endsWith('fact-checker')) return { checked: 3, confirmed: 2, corrected: [{ claim: 'c', fix: 'f' }], unverified: [], numbersRecomputed: 1 }
  if (o.agentType.endsWith('overseer')) return { reports: [{ role: 'ux-researcher', pass: false, fixes: [{ item: 7, fix: 'rate as a ÷ b' }] }, { role: 'data-scientist', pass: true, fixes: [] }], crossRole: [{ issue: 'units differ', roles: ['ux-researcher', 'data-scientist'] }] }
  if (o.agentType.endsWith('synthesizer')) return { file: '/p/PROPOSAL.md', tldr: ['t'], decisions: 1 }
  return { file: 'f', tldr: [], lowConfidence: 0 }
}
const parallel = fs => Promise.all(fs.map(f => f()))
const quiet = () => {}

let fails = 0
const check = (name, ok, detail = '') => { fails += !ok; console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}${ok ? '' : '  ' + detail}`) }
let total = 0
const compare = (label, want) => {
  total += 1
  const got = sent[label]
  const at = got ? [...want].findIndex((c, i) => c !== got[i]) : -1
  check(`prompt ${label}`, got === want, got ? `differs at char ${at}: ${JSON.stringify(want.slice(at, at + 40))} vs ${JSON.stringify(got.slice(at, at + 40))}` : 'not sent')
}

const args = { question: 'Q?', slug: 'sl', type: 'build', roles: ['ux-researcher', 'data-scientist'], goals: '/p/CLAUDE.md § Success criteria', projectRoot: '/p', pluginRoot: '/x', date: '2026-10-10' }
const result = await runWorkflow(args, agent, parallel, quiet, quiet)

const v = { root: '/p', plugin: '/x', question: 'Q?', date: '2026-10-10', slug: 'sl', type: 'build', goals: args.goals, typeDir: '/x/types/build', proposal: '/p/proposals/sl.md' }
const out = r => `/p/references/sl-${r}.md`
const reportList = args.roles.map(r => `- ${r}: ${out(r)}`).join('\n')
const factSummary = args.roles.map(r => `${r}: 3 checked, 2 confirmed, 1 corrected, 0 unverified, 1 numbers recomputed`).join('\n')
const expected = {
  'research:ux-researcher': fill('Research', { ...v, output: out('ux-researcher') }),
  'research:data-scientist': fill('Research', { ...v, output: out('data-scientist') }),
  'fact-check:ux-researcher': fill('Fact-check', { ...v, report: out('ux-researcher') }),
  'fact-check:data-scientist': fill('Fact-check', { ...v, report: out('data-scientist') }),
  overseer: fill('Oversee', { ...v, reportList, factSummary }),
  'fix:ux-researcher': fill('Research', { ...v, output: out('ux-researcher') }) + fill('Fix', { fixList: '- [7] rate as a ÷ b' }),
  synthesis: fill('Synthesis', { ...v, reportList, factSummary, crossList: '- units differ (ux-researcher, data-scientist)' }),
}

for (const [label, want] of Object.entries(expected)) compare(label, want)
total += 2
check('no unexpected agents', Object.keys(sent).length === Object.keys(expected).length, Object.keys(sent).join(','))
check('stats: 7 agents, 1 fix pass', result.stats.agents === 7 && result.stats.fixPasses === 1, JSON.stringify(result.stats))

// Strategy round: type paths reach every prompt; roles outside the overseer stub still run.
sent = {}
const sArgs = { ...args, type: 'strategy', roles: ['competitive-analyst', 'staff-software-engineer'], goals: 'G1 grow revenue; G2 enter EU' }
const sv = { ...v, type: 'strategy', goals: sArgs.goals, typeDir: '/x/types/strategy' }
const sOut = r => `/p/references/sl-${r}.md`
const sResult = await runWorkflow(sArgs, agent, parallel, quiet, quiet)
compare('research:competitive-analyst', fill('Research', { ...sv, output: sOut('competitive-analyst') }))
compare('research:staff-software-engineer', fill('Research', { ...sv, output: sOut('staff-software-engineer') }))
compare('synthesis', fill('Synthesis', { ...sv, reportList: sArgs.roles.map(r => `- ${r}: ${sOut(r)}`).join('\n'), factSummary: sArgs.roles.map(r => `${r}: 3 checked, 2 confirmed, 1 corrected, 0 unverified, 1 numbers recomputed`).join('\n'), crossList: '- units differ (ux-researcher, data-scientist)' }))
total += 1
check('strategy result type', sResult.type === 'strategy', sResult.type)

total += 2
const bad = await runWorkflow({ question: 'q', slug: 'Bad Slug', type: 'plan', roles: ['nope'], projectRoot: 'rel', pluginRoot: '/x' }, agent, parallel, quiet, quiet)
check('bad args rejected', bad.started === false && bad.problems.length === 5, JSON.stringify(bad.problems))
const noGoals = await runWorkflow({ ...args, goals: '' }, agent, parallel, quiet, quiet)
check('missing goals rejected', noGoals.started === false && /goals/.test(noGoals.problems.join()), JSON.stringify(noGoals.problems))

console.log(`\n${total - fails}/${total} passed`)
process.exit(fails ? 1 : 0)
