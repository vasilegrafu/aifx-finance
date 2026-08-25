# business-model — how value is created and captured, and for whom

## Question this answers

How does the company create value for a specific customer, capture part of it,
and do the economics improve or worsen as it grows?

## When to run / when to skip

Run first in every tier — nothing downstream makes sense without it. Skip only
when the question is purely about the industry with no company attached.

## Inputs

- Company definition and profit-engine segment from the hub's *Before any
  module* step.
- `data/fact_pack.py` output if any revenue, margin, or segment figure will be
  stated.
- Standalone: nothing else — this module opens the analysis.

## Method

1. **Customer and job.** Who precisely is the customer (segment, not
   "consumers")? What job do they hire the product for? What is their
   next-best alternative? What drives their willingness to pay — performance,
   risk reduction, convenience, status, price? If the buyer and the user
   differ, say whose problem the company actually solves.
2. **Value creation.** Which levers the company actually pulls:
   differentiation, experience, network or ecosystem value, reliability,
   convenience, brand, innovation. Name the one or two that carry the model;
   do not list all of them.
3. **Value capture.** Pricing model, revenue streams, gross margin structure,
   recurring vs transactional mix, capital intensity, customer acquisition
   cost vs lifetime value, retention. Where does the margin actually come
   from?
4. **Strategic economics.** What drives revenue growth, what drives margins,
   what drives return on invested capital? Where does the *incremental*
   dollar of profit come from? Does scale improve the economics (falling unit
   costs, network effects) or dilute them (complexity, mix shift)? Is the
   model becoming more or less attractive over time?
5. **Segment discipline.** If multi-segment: which segment is the profit
   engine, which is subsidized, and does the reported blend hide either? Name
   the segment the rest of the analysis should be about.

## What good looks like

> The engine is not the hardware, which carries a mid-30s gross margin against
> vertically integrated rivals — it is the attach: each device sold recruits a
> subscriber whose services margin is roughly double, whose churn is low
> because the ecosystem raises switching costs, and whose acquisition cost was
> already paid by the hardware sale. Incremental profit therefore comes from
> installed-base growth and attach rate, not unit growth — which is why flat
> device volumes with rising services revenue is a healthy reading of this
> model, not a warning [Inference from FY figures in the fact pack].

Note what that paragraph does: names the profit engine, traces the incremental
dollar, and converts a headline "flat volumes" fact into a model-specific
judgment.

## Hands off

- The **profit-engine segment** → `industry-structure.md` and
  `competitive-advantage.md` analyze at that level, not the blend.
- The **willingness-to-pay mechanism** → `competitive-position.md` tests it
  against the next-best alternative.
- The **drivers of margin and ROIC** → `financial-performance.md` checks the
  numbers actually move with them.
- **Scale economics verdict** (improving/diluting) → `growth-and-ma.md` and
  `synthesis/diagnosis.md`.

## Failure modes

- Describing the product instead of the model — features are not economics.
- "The customer" as everyone; a model that serves everyone captures from no
  one in particular.
- Listing ten value levers instead of naming the one or two load-bearing ones.
- Analyzing the blended company when one segment pays for the others.
- Stating margins or mix from memory when the fact pack could have read them.
