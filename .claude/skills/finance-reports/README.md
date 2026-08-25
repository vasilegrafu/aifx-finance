# finance-reports — reports as programs, not documents

Generates standalone HTML investing reports from live market and fundamentals
data: a component library — every component with a built showcase page — and
the report engine that builds documents out of them. A report is a program: a
controller fetches and asserts, a view chooses which components appear, and
the output is regenerated, never edited.

This README is for a **human** installing and running the skill. How the
skill *works* — its contracts, procedures, and internals — is documented for
Claude in [SKILL.md](SKILL.md) and the `REFERENCE.md` beside each engine;
`components/CATALOG.md` is the generated index of what exists.

**Before anything here runs**: Python, the venv, and the credential files are
set up once, centrally — [SETUP.md](../../../SETUP.md) owns that path.
Versioning is central too: one version governs the whole repository — see
[Versioning](../../../README.md#versioning).

---

## Check the install — `status.py`

Appearing in Claude Code's skills list means the skill was found. It does not
mean it can build anything. One command says what is actually there, for
either install:

```bash
./.venv/Scripts/python.exe .claude/skills/finance-reports/status.py
```

```
finance-reports  <path>\aifx-finance\.claude\skills\finance-reports

components  …
  charts-apache-echarts                   …
  diagrams-mermaid                        …
  …
reports     …
version     …        every generated page pins this at BUILD time

checks
  usage.md skeleton                     ok
  class prefixes own their directory    ok
  every class in markup is reachable    ok
  components/CATALOG.md                 ok
  reports/CATALOG.md                    ok
  showcase pages                        ok
  bundles load every module             ok
```

The counts are elided above on purpose: `status.py` reads them off the tree,
so printing them here would only record what was true the day this was typed.

Two things to read there. **The path on the first line tells you which
install you got** — it resolves through a junction, so a *linked* skill
prints the clone's path and a *copied* one prints your project's. **The
version line is the copy path's usual failure**: a copied skill needs its own
`version.json` beside `.claude/`, and without one it cannot render a single
page. `status.py` says so in a sentence instead of a traceback.

The checks that regenerate something to compare against it — both catalogues
and every showcase page — render templates, so they need Jinja from the venv.
On an interpreter without it they report `NOT RUN` and name the missing
library rather than claiming anything is stale, because being sent to
regenerate a catalogue that was already current is worse than being told
nothing. The rest are pure file reading and always run.

`--check` exits 1 if any of them fails — a stale catalogue or showcase page,
a `usage.md` off the skeleton, a class whose prefix does not match the
directory it lives in or that no stylesheet can reach, or a `css/bundle.css`
or `js/bundle.js` that has stopped loading a file beside it. Useful in a
pre-commit hook if you intend to *modify* the skill; not needed to use it.

## Building a report

```powershell
./.venv/Scripts/python.exe .claude/skills/finance-reports/reports/report_builder.py `
    financial-profile AMD --peers NVDA,INTC --out ./some/directory
```

`--out` is required and has no default: the page's local asset links are
computed relative to wherever it is written, so the destination is a decision.

`--asset-bundles` says which bundle the page links, and **defaults to `cdn`**
— the pinned version, so the page renders anywhere: copied, mailed, opened
from a download folder. Pass `local` to point it at this tree relative to
`--out` instead, which is live against whatever you have just edited and
broken the moment the file is moved. The default goes to the portable one
because `cdn` works everywhere `local` does and more, so it cannot be
silently wrong.

Every build says what it resolved, and from where, before spending ~13 API
calls:

```
environment: dev (from D:\...\environment.json)   config.dev.json, key from D:\...\secrets.dev.json
fetching ...
deriving and asserting ...
<path to the written file>
```

How the environment, config, and key resolve — and why there is no flag and
no default — is [SETUP.md](../../../SETUP.md#4-the-three-root-files)'s to
explain.

```powershell
./.venv/Scripts/python.exe .claude/skills/finance-reports/reports/report_builder.py financial-profile --help
```

A built report carries live market data and differs on every run: it is an
artifact — never commit one, wherever it was written.

## Every report validates itself

There is no separate test to remember to run. `build()` checks the page it
just rendered and **writes what it found into the top of the document**,
above the cover — so the findings arrive where you already have to look,
since charts draw at view time and the page has to be opened anyway.

A report that left this tree therefore carries its own warning. That matters
more than the developer case: a reader cannot otherwise tell a healthy page
from one whose endpoint returned nothing, because `0 + 0 == 0` satisfies
every identity the controller asserts.

- **errors** — the page is broken: a chart spec that will not parse, an asset
  half that does not resolve, a link to an id nothing carries, unrendered
  template syntax. Independent of which company was asked for.
- **warnings** — the page rendered and its content is thin: an empty chart, a
  table with no rows, a section mostly blank, a requested symbol appearing
  nowhere. Usually a sparse subject, so they are shown and fail nothing.

Neither raises. The page has already cost ~13 live calls and is written
either way — a page you can open beats an exception. A clean build carries
the all-clear as an HTML comment rather than a box, so *"validated and
clean"* is never confused with *"validation never ran"*.

The checks live in `reports/_report_validation.py`, one home for all reports.
What each report expects of itself — its sections, its domain class prefix,
the symbols the request named — is declared on its controller beside `TITLE`.

That is why the warnings exist at all: an endpoint returning 200 with an
empty body passes every structural check, and the report renders beautifully
with flat lines and no numbers. The warnings are what measure that.

**A clean report is valid, not correct.** Charts draw at view time and
nothing in the build has seen one, so **open it**.
