# Session Log: Workflow Infrastructure Research

**Date:** 2026-04-07
**Goal:** Research and evaluate external tools/repos for improving the claude-code-my-workflow template

---

## Context

User is exploring updates to the academic workflow infrastructure. Researching multiple external resources in parallel to identify what's worth importing or adapting.

## Resources Under Investigation

| Resource | URL | Purpose |
|----------|-----|---------|
| Oracle (steipete) | github.com/steipete/oracle | Bridge to ChatGPT Pro for complex reasoning |
| statsclaw | github.com/statsclaw/statsclaw | Infrastructure patterns to import |
| Karpathy autoresearch | github.com/karpathy/autoresearch | Research automation patterns |
| liteparse | github.com/run-llama/liteparse | PDF parsing for context engineering |
| Anthropic resources | anthropic.com | Latest Claude Code best practices |
| Econ730 repo | pedrohcgs GitHub | Existing lecture repo infrastructure |
| Aniket's advice | X post | Using ChatGPT Pro via Oracle for econ research |

## Key Ideas from Aniket's Post

- Oracle packages codebase context + external context + prompt for ChatGPT Pro
- Pro model is best for: econometric theory, structural IO, quant macro/finance, micro theory
- Two recommended uses: (1) review plans for complex empirical projects, (2) proving theorems/extending models
- Comingle code and paper (TeX files) for better context engineering
- Use liteparse or extended abstracts for others' papers
- Install Oracle as a skill, not CLI
- If OPENAI_API_KEY is set, tweak skill to avoid defaulting to API

## Key Findings

### Oracle (steipete/oracle) -- INSTALL
- Bridge to ChatGPT Pro for hard reasoning tasks (~30 min/call)
- Install: `npm install -g @steipete/oracle` (Node 22+)
- Best for: reviewing complex plans, proving theorems, structural estimation
- SKILL.md ready to install as Claude Code skill
- Aniket tip: don't use as CLI, use as skill; tweak to avoid defaulting to API if OPENAI_API_KEY set

### LiteParse (run-llama/liteparse) -- INSTALL
- Local PDF-to-text extraction, no cloud dependency
- Install: `npm i -g @llamaindex/liteparse`
- Use text for prose, screenshots for tables/equations
- Limitation: no LaTeX math reconstruction

### StatsClaw (statsclaw/statsclaw) -- ADOPT PATTERNS
- Pipeline isolation: builder/tester never see each other's specs
- Tolerance integrity: never relax tolerances to pass tests
- Deep comprehension protocol: planner proves understanding before specifying
- State machine with hard gates and formal transitions

### Karpathy Autoresearch -- ADOPT PATTERNS
- Single file to modify, single scalar metric, fixed time budget
- Keep-or-revert with git; program.md as orchestration
- Maps to Monte Carlo: prepare.R (fixed) + simulation.R (agent-modified) + program.md
- 70/30 rule: spend 70% on problem definition, 30% on execution

### Anthropic Best Practices -- ADOPT
- CLAUDE.md should be ~100 lines; domain knowledge in skills
- `/compact Focus on [topic]` for directed compaction
- Hooks = deterministic; CLAUDE.md = advisory
- Subagents beat single agents by 90% on breadth-first tasks
- Writer/Reviewer in fresh sessions eliminates confirmation bias

### Econ730 Gaps -- PORT TO TEMPLATE
- 9 missing hooks (bash-safety, output-scanner, audit-log, enforce-isolation, etc.)
- Deny list in settings.json (17 destructive patterns) -- SECURITY GAP
- 10 missing skills, 8 missing rules
- CI validation workflow (.github/workflows/validate-infrastructure.yml)

## Decisions Made

- All 7 research streams completed and synthesized
- Priority order: P0 security gaps > P1 tool installation > P2 pattern adoption > P3 new capabilities
- Memories saved for all key findings

## Implementation Progress

### Completed
- 6 new hooks created + chmod +x (bash-safety, output-scanner, audit-log, enforce-isolation, enforce-foreground-agents, plan-reminder)
- 6 new skills created (oracle, parse-paper, mailbox, progress, ship, simulation-study)
- 2 new rules created (pipeline-isolation, inter-agent-communication)
- 1 new template created (research-program.md)
- settings.json: deny list (17 patterns), showThinkingSummaries, 6 new hook configs, npx/npm/lit permissions
- .gitignore: .claude/logs/ added
- 4 skills updated: context:fork (lit-review, research-ideation, review-paper), effort:max (data-analysis)
- 2 rules updated: tolerance integrity (quality-gates), deep comprehension (plan-first)
- CLAUDE.md: research-before-editing principle, 6 new skills, compaction directives
- MEMORY.md: 12 new [LEARN] entries (security, agents, research, anthropic)
- WORKFLOW_QUICK_REF.md: security layer, new capabilities

### Verification
- settings.json: VALID JSON
- Hook permissions: all 13 executable
- Counts: 13 hooks, 28 skills, 20 rules, 10 agents, 8 templates
- Econ730 references: only in intentional examples (meta-governance, r-code-conventions)
- .gitignore: .claude/logs/ present

### Pending
- README.md update (agent running)
- guide/workflow-guide.qmd update (agent running)
