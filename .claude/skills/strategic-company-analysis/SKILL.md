---
name: strategic-company-analysis
description: Analyze companies from a strategic management perspective — external, internal, competitive, corporate, financial, and scenario analysis producing prioritized strategic recommendations. Also for analyzing one aspect on its own — industry structure, competitive advantage, business model, growth or M&A options, management quality, financial performance — each is a separately loadable module. Use for strategy case analyses, competitive-advantage assessments, strategic comparisons of companies, 3–5 year strategic outlooks, and consulting-style or academic strategy work.
---

# strategic-company-analysis — one diagnosis, many loadable lenses

This file is the only part that always loads. Everything else is a module,
loaded when the question needs it and never otherwise:

| where | load it when |
|---|---|
| `modules/<aspect>.md` | analyzing that aspect — alone, or as a pipeline step |
| `synthesis/diagnosis.md` → `synthesis/alternatives.md` → `synthesis/recommendation.md` → `synthesis/falsification.md` | turning module output into a recommendation — in that order |
| `company-types.md` | once the company's type is known (private, startup, mature, platform, regulated) |
| `output-forms.md` | before writing the final document — it owns every output format |
| `data/fact_pack.py` | BEFORE asserting any financial figure it can fetch — see Evidence |

A single-aspect question loads one module plus whatever its `Inputs` section
names. A full analysis follows the pipeline below. Never load everything for a
narrow question.

## Stance

Analyze the company as a **strategic system**; do not merely describe it. The
movement is always:

**Facts → Diagnosis → Causal explanation → Strategic choices → Recommendation
→ Implementation → Risks**

Think like a strategist, not a reporter: *what happened → why → why it matters
→ what will competitors do → what should management do → what must be true for
that to work → how could this be wrong.*

Frameworks (Porter, VRIO, PESTEL, SWOT, RBV…) are used only where they explain
a causal relationship that matters here. The modules are **inputs to one
diagnosis, not chapters of a report** — the final document is structured by
`output-forms.md`, deliberately differently from the module list, so the
output can never degrade into disconnected framework tables.

## Six rules that bind every module

1. **Strategy is choices with trade-offs.** Where to compete, how, for whom,
   what deliberately not to do, and how the choices reinforce one another. A
   strategy without a real trade-off is an aspiration.
2. **Every advantage claim carries its causal chain**: what creates it → why
   customers care → effect on willingness to pay, acquisition cost, retention,
   pricing, or cost → why imitation is slow or expensive → strengthening or
   eroding. "Strong brand" is banned as a finished statement.
3. **Value is created only where return on invested capital exceeds its
   cost.** Growth below that spread destroys value. Say which side of the line
   the company is on before praising growth or recommending more of it.
4. **Distinguish temporary success from durable advantage.** Market
   conditions, first-mover timing, competitor underinvestment, and cycles all
   masquerade as moats. History is not proof of durability.
5. **Analyze in time.** What changed, why, who responded, and whether the
   position is strengthening or eroding. A static snapshot is not a diagnosis.
6. **Size what you diagnose.** Each issue and each option gets an
   order-of-magnitude economic estimate with the arithmetic shown — or an
   explicit "unquantifiable because X". Rank by magnitude, not list order.

## Evidence discipline

- **Read, don't recall.** Date-stamp the analysis. Every load-bearing fact is
  either *read* — from `data/fact_pack.py`, a filing, or a live source, with
  its as-of date — or explicitly flagged `[recalled — verify]`. The model's
  own memory of a company is a Tier-3 source: confidently stale.
- **Run the fact pack before asserting any figure it can fetch**:
  `./.venv/Scripts/python.exe .claude/skills/strategic-company-analysis/data/fact_pack.py SYMBOL --peers A,B`.
  Its output is live data — an artifact, never committed.
- **Never invent** revenue, market share, margins, growth rates, customer
  counts, market size, valuations, or management intentions. If reliable data
  is unavailable, say so and use ranges.
- **Source tiers**: 1 — filings, annual reports, official investor and
  government material; 2 — major financial press, industry publications,
  academic and professional research; 3 — blogs, aggregators, forums, model
  memory. Tier 3 finds leads; it never carries a critical claim.
- **Label claims**: **Fact** (evidenced) / **Inference** (derived from facts)
  / **Assumption** (required, not established) / **Hypothesis** (plausible,
  needs validation). Never present inference as fact.
- **Missing information is not a blocker.** Use what exists, state
  assumptions, use ranges, say how the missing piece could flip the
  conclusion, and continue. Ask the user only when the analysis is genuinely
  impossible without an answer.

## Before any module

1. **Define the object.** Company, ownership, segments, geographies, customer
   groups, revenue and profit model, key competitors. If diversified, analyze
   the businesses *and* the parent — never assume strategic homogeneity.
   Identify the **profit-engine segment** and aim the deep analysis there: a
   blended average of a monopoly segment and a commodity segment describes
   neither.
2. **Formulate the central strategic question.** One central tension — defend
   profitability or chase growth, ride the model or rebuild it. Every module's
   findings are read against it.

## Depth tiers

| tier | loads | output (see `output-forms.md`) |
|---|---|---|
| **quick take** | `modules/business-model.md`, `modules/competitive-advantage.md` (+ fact pack if figures appear) | one page: position, advantage verdict, central tension, what to watch |
| **standard** | quick take + `modules/industry-structure.md`, `modules/competitive-position.md`, `modules/financial-performance.md`, `synthesis/diagnosis.md`, `synthesis/recommendation.md` | short memo |
| **full** | every applicable module + all four synthesis files | full report |

Match the tier to the question asked; nobody who asked a question wants to pay
for a case study.

## Full analysis — the sequential pipeline

Run in order, in one context. Each module ends with a **Hands off** block —
carry those conclusions forward; they are the analysis. The order:

1. `modules/business-model.md`
2. `modules/external-environment.md`
3. `modules/industry-structure.md`
4. `modules/competitive-position.md`
5. `modules/competitive-advantage.md`
6. `modules/value-chain.md` — only if its *When to run* says so
7. `modules/corporate-strategy.md` — only if multi-business
8. `modules/growth-and-ma.md` — only if growth or M&A is on the table
9. `modules/management-and-capital-allocation.md`
10. `modules/financial-performance.md` — fact pack first
11. `modules/scenarios-and-risk.md`
12. `synthesis/diagnosis.md` — stop collecting; diagnose
13. `synthesis/alternatives.md`
14. `synthesis/recommendation.md`
15. `synthesis/falsification.md` — the completion gate lives here

Then write the document per `output-forms.md`, adjusted by `company-types.md`.

## Module skeleton

Every file in `modules/` and `synthesis/` follows this exact heading order —
`check.py` enforces it:

```
## Question this answers      one question, so routing is unambiguous
## When to run / when to skip
## Inputs                     data needed; which modules feed it in the pipeline
## Method
## What good looks like       a short worked fragment, never empty
## Hands off                  conclusions later modules and synthesis consume
## Failure modes
```

## Failure modes that end an analysis (apply everywhere)

- Framework dumping: a table exists because the framework exists.
- Description without diagnosis: facts never become cause → consequence → choice.
- Generic anything: "strong brand", "threat: competition", "increase
  innovation", "expand internationally" without where, why, and how.
- A recalled number presented as a read one.
- An advantage without a causal chain, or durability argued from history.
- A recommendation missing any of: trade-off, capability check, capital check,
  competitor response, falsifier.
- Alternatives that are one strategy reworded.
- Equal weight to all findings — magnitude ranks, always.
- False precision: invented decimals where honest ranges belong.
- Backward-looking analysis with no forward implication.

## Maintenance

`./.venv/Scripts/python.exe .claude/skills/strategic-company-analysis/check.py`
verifies: every module and synthesis file matches the skeleton with a
non-empty *What good looks like*, every path referenced in any of this skill's
documents resolves, and every module is routed from this file. The `data/`
layer is adapted from `finance-reports/service_providers/` — copied, not
imported, so this skill stays self-contained; each copied file names its
origin. Fact-pack output carries live data: never commit it, wherever it was
written.
