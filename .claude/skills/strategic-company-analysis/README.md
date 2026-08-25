# strategic-company-analysis — one diagnosis, many loadable lenses

Analyzes companies as strategic systems: modular external, competitive,
corporate, financial, and scenario analysis producing prioritized
recommendations. Any aspect — industry structure, competitive advantage,
business model, growth options, management quality, financial performance —
can be analyzed on its own; a full analysis runs the modules as a sequential
pipeline and synthesizes a diagnosis, alternatives, a recommendation, and its
falsification.

This README is for a **human** installing and running the skill. How the
skill *thinks* is documented for Claude in [SKILL.md](SKILL.md) — the hub
that routes to everything else:

```
SKILL.md          the hub: stance, evidence rules, depth tiers, pipeline, routing
modules/          one aspect each, separately loadable, on a fixed skeleton
synthesis/        diagnosis → alternatives → recommendation → falsification
company-types.md  emphasis shifts for private / startup / mature / platform / regulated
output-forms.md   report, memo, quick-take, comparative, and academic forms
data/             self-contained FMP access + the fact pack
check.py          structural consistency, exit 1 on drift
```

**Before anything here runs**: Python, the venv, and the credential files are
set up once, centrally — [SETUP.md](../../../SETUP.md) owns that path.
Versioning is central too — see
[Versioning](../../../README.md#versioning); this skill carries no version of
its own.

---

## Check the install — `check.py`

Free — no API call:

```bash
./.venv/Scripts/python.exe .claude/skills/strategic-company-analysis/check.py
```

It verifies the skill against itself: every module and synthesis file matches
the skeleton `SKILL.md` declares (with a non-empty worked example), every
path referenced in any of this skill's documents resolves, and nothing is
orphaned — every module is routed from the hub. Exit 1 on any failure. What
it deliberately does not check is the *quality* of a module — that has no
engine and is found only by using it.

## The fact pack — figures read, not recalled

The skill forbids stating financial figures from model memory.
`data/fact_pack.py` is the mechanism: it reads what a strategic analysis
leans on — multi-year trend with ROIC, reconstructed TTM, balance-sheet
snapshot, the capital-allocation ledger, segments, peer comparison — and
prints one labeled markdown block with a single as-of timestamp, so the
analysis can cite Facts instead of memories.

```bash
./.venv/Scripts/python.exe .claude/skills/strategic-company-analysis/data/fact_pack.py \
    MSFT --peers AAPL,GOOGL,ORCL --out <somewhere>/fact_pack_MSFT.md
```

- **~13 live API calls per run, nothing cached** — a pack describes one
  stated moment. Every run prints which environment it resolved and where
  the key came from (never the key) before spending the first call.
- **Peers are chosen, not defaulted** — pick the comparators the analysis
  named; without `--peers` the peer table is omitted and says so.
- **TTM is reconstructed** from four reported quarters (the TTM endpoints
  are plan-gated) and labeled so; every absent figure prints as `·`, never
  as a plausible zero.
- **It does not estimate a cost of capital** — that is an analyst
  Assumption, not a read; the pack says so at the point of use.
- **The output is an artifact.** It carries live data and differs on every
  run: never commit one, wherever it was written.

`data/endpoints.md` documents what the FMP Starter plan gates and the traps
the pack compensates for. The `data/` layer is adapted from
`finance-reports/service_providers/` — copied, not imported, so this skill
stays self-contained; both read the same root credential files, so there is
one key on the machine either way.

## Using the skill

Ask Claude Code for what you actually want — a quick strategic take, a
standard memo, a full case analysis, or one aspect ("assess the moat", "is
management good at capital allocation?"). The hub's depth tiers load only
what the question needs; the fact pack runs whenever figures will be
asserted. The final document's forms live in `output-forms.md`.
