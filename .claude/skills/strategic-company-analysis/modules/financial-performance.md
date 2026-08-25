# financial-performance — what the numbers say about whether the strategy works

## Question this answers

Do the financial results confirm that value is being created, and what
strategic causes — not accounting ones — explain their level and trend?

## When to run / when to skip

Run in standard and full analyses and standalone for any performance,
margin, or "is this company actually good" question. **Run
`data/fact_pack.py` first, always** — this module never states a figure from
memory. Skip only when no financial claim will be made at all.

## Inputs

- **The fact pack** — `./.venv/Scripts/python.exe
  .claude/skills/strategic-company-analysis/data/fact_pack.py SYMBOL --peers
  A,B,C`. Peers are chosen, not defaulted: pick the comparators the
  positioning module named. Every figure below comes from it or from a filing,
  with its as-of date.
- The margin/ROIC drivers claimed by `business-model.md` and the relative
  price/cost position claimed by `competitive-position.md` — this module is
  where those claims meet the ledger.

## Method

1. **The value-creation test first.** ROIC (read) against cost of capital
   (estimated — state the estimate and label it Assumption; the pack
   deliberately does not invent one). Above the line, below it, or straddling
   — and the five-year direction. Everything else is commentary on this.
2. **Decompose the trend causally.** For each material move in growth,
   gross margin, operating margin, or FCF: which strategic explanation fits —
   pricing power, mix shift, scale, cost programs, cyclical conditions, or
   underinvestment dressed as efficiency? Each candidate cause implies other
   symptoms (pricing power shows in gross margin *and* stable share;
   underinvestment shows in falling R&D/capex intensity); check them before
   concluding. Margin expansion is not strength until its cause is known.
3. **Growth quality.** Organic vs acquired; capital consumed per dollar of
   new revenue; whether growth arrived with margin (operating leverage) or
   bought without it.
4. **Relative and historical.** Against the chosen peers (pack's peer table:
   ROIC, capex, R&D, SBC intensity, EV/EBITDA) and against the company's own
   five years. A number without a comparator is a mood.
5. **Cash and capacity.** Accrual-to-cash conversion (profits nobody can
   bank are a finding); balance-sheet room — cash, debt, FCF — versus the
   capital the strategic options will demand.
6. **Anomalies.** Anything the strategic story does not explain — a margin
   the position shouldn't earn, growth the market doesn't show — is not
   smoothed over; it is handed to falsification.

## What good looks like

> ROIC of ~19% [Fact: fact pack, FY2025] against an estimated ~9% cost of
> capital [Assumption: stated build-up] — the company clears the bar with
> room, and has for five years. But the decomposition undercuts the headline:
> of the 4pt operating-margin expansion, roughly three points trace to R&D
> intensity falling from 14% to 10% of revenue [Fact: fact pack], not to
> pricing or scale. Peers held theirs at 13–15%. The strongest explanation is
> harvesting: strategically, the margin story and the erosion story in the
> advantage module are the same story [Inference].

## Hands off

- The **value-creation verdict** and its direction →
  `synthesis/diagnosis.md` — it anchors issue sizing.
- **Financial capacity** → `synthesis/alternatives.md` (what is affordable)
  and `growth-and-ma.md`.
- **Unexplained anomalies** → `synthesis/falsification.md`.
- Whether deployed capital earned its cost →
  `management-and-capital-allocation.md`.

## Failure modes

- Any figure stated from memory — the one mechanical rule this module has.
- Ratio recitation: numbers reported without a strategic cause attached.
- Praising margin expansion before ruling out underinvestment.
- Comparing against nothing, or against peers the positioning module would
  reject.
- Treating the accounts as the analysis — this module serves the diagnosis;
  it does not replace it.
