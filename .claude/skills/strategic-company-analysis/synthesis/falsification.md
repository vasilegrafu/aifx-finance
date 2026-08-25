# falsification — how this analysis could be wrong, and what would show it first

## Question this answers

What would prove this diagnosis and recommendation wrong, and what observable
signal would show it earliest?

## When to run / when to skip

Run last in every standard and full analysis — this file is the completion
gate; an analysis that has not tried to break itself is a draft. In a quick
take, its spirit survives as the "what to watch" lines. Never skip when a
recommendation was made.

## Inputs

- The three **what-must-be-true assumptions** from
  `synthesis/recommendation.md`, verbatim.
- Early-warning indicators with thresholds from `modules/scenarios-and-risk.md`.
- Unexplained anomalies from `modules/financial-performance.md`.
- The evidence labels (Fact / Inference / Assumption) carried through
  `synthesis/diagnosis.md`.

## Method

1. **Build the falsification table — the loop that ties the skill together.**
   One row per load-bearing assumption:

   | assumption | what would falsify it | leading indicator + threshold | scenario it maps to | review trigger |

   Each falsifier must be *observable* (a price, a filing line, a churn
   figure, a regulatory text — something checkable, not a vibe). These rows
   ARE the leading-KPI set the recommendation carries; if a row has no
   indicator, the assumption is unmonitorable and must be said out loud.
2. **Steelman the alternative explanation.** The strongest *different*
   account of the company's success or trouble — the one a smart bear (or
   bull) would give. State what evidence discriminates between the accounts,
   and which reading the current evidence actually favors. If the analysis
   only survives against weak objections, it has not been tested.
3. **Audit the evidence chain.** Where does the diagnosis rest on Inference
   or Assumption rather than Fact? Which single piece of evidence, if wrong,
   collapses the most? Management statements used as evidence get special
   suspicion — they are the account most incentivized to be wrong. What
   missing data, if it arrived, could flip the conclusion?
4. **The do-nothing check.** What actually happens if management ignores all
   of this — is the burning platform real, or would drift be tolerable for
   years? An analysis that cannot survive this question has overstated its
   urgency.
5. **Gate on the ten questions.** What business is this really in; who is the
   core customer; why does it win; why might it stop winning; which
   capability matters most; which industry force matters most; what is
   management's biggest dilemma; which option creates most value; what must
   management stop doing; what would make the recommendation fail. Any
   answer still fuzzy → the analysis is incomplete, and the module that owns
   the fuzz gets reopened before anything ships.

## What good looks like

> | assumption | falsifier | indicator + threshold | scenario | review |
> |---|---|---|---|---|
> | Certification remains a 3-yr barrier | fast-track provision in the draft rule | consultation text; any mutual-recognition clause | downside | each publication |
> | Switching costs hold at renewal | flagship accounts dual-sourcing | renewal win-rate < 85% | downside | quarterly |
> | Freed capacity is shut | volume reappears down-market | low-end unit shipments > 0 by Q4 | — | quarterly |
>
> Steelman: the bear's account — margins are cyclical, not positional — is
> discriminated by peer comparison: cyclical margins would compress with the
> industry's, and the company's spread *widened* through the last downturn
> [Fact: fact pack five-year table]. The bear's account fails on current
> evidence; it becomes right if the spread narrows two consecutive years.

## Hands off

- The falsification table → the final document's risk section and the
  recommendation's KPI set (`output-forms.md` places it).
- Any reopened module → back up the pipeline before delivery; the gate is
  allowed to send work back.

## Failure modes

- Falsification as ritual: risks restated as "challenges" with no observable
  falsifier attached.
- A steelman built weak so the thesis survives.
- Indicators without thresholds — a signal nobody can act on is scenery.
- Treating the gate as optional under time pressure; the ten questions take
  minutes and catch the failures that cost credibility.
- Confusing confidence with calibration: the deliverable states what would
  change its mind, or it is advocacy, not analysis.
