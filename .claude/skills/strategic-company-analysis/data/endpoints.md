# FMP endpoints — what the fact pack uses, what is gated, what lies

Adapted from `finance-reports/service_providers/fmp/endpoints.md` (2026-08-25),
trimmed to what `fact_pack.py` touches. The finance-reports copy is the fuller
account; this one exists so this skill stays self-contained.

Base: `https://financialmodelingprep.com/stable` (from `config.<env>.json`).

## The MCP tool's endpoint names are NOT the API's paths

| MCP tool name | actual path |
|---|---|
| `cashflow-statement` | **`cash-flow-statement`** |
| `profile-symbol` | **`profile`** |

The rest match. A wrong name returns HTTP 404, which reads identically to a
gated endpoint — check this table before concluding the plan is the problem.

## Plan gating (Starter) — what the fact pack relies on

| endpoint | Starter |
|---|---|
| `income-statement`, `balance-sheet-statement`, `cash-flow-statement` — annual AND quarter | works |
| `income-statements-ttm` and siblings | **gated** — TTM must be summed from quarters |
| `revenue-product-segmentation` — annual | works (quarter is gated) |
| `key-metrics`, `financial-scores` | works |
| `profile`, `quote` | works |

A gated endpoint returns an HTTP error, which `FmpClient` turns into an
`FmpError` naming this file. It does **not** return empty data, so a gated
endpoint can never be mistaken for a company with no such disclosure.

## Traps the fact pack compensates for — keep compensating if you extend it

**TTM is not available; build it and label it.** A trailing figure is summed
from four `period=quarter` statements. Never let an annual figure stand in for
a trailing one without labelling it — the pack marks every such row
RECONSTRUCTED.

**`limit` silently truncates a derivation.** Pull the years you intend to
show; never back-calculate a series from a ratio because the pull was short —
it reproduces reported numbers exactly, which is precisely what makes it look
like a read when it is a reconstruction.

**`financial-scores` uses its own inputs.** Its `altmanZScore` is computed
with its own `marketCap` and `ebit`, which differ from `key-metrics` and
`income-statement` for the same fiscal year — as-of different moments, neither
wrong. The pack states the caveat beside the score.

**Statement lines do not always sum to their own subtotals.** Small plugs
(single-digit $M) between components and stated subtotals are normal. Any
derivation that must conserve needs a named plug, never one hidden in a
legitimate line.

**Currency.** `reportedCurrency` is per-statement. Nothing here converts; the
pack prints the currency once in its header.

**Field-name quirk:** key-metrics spells R&D intensity
`researchAndDevelopementToRevenue` — FMP's typo, faithfully queried.
