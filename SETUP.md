# SETUP — from a bare machine to running skills

Everything a machine needs before any skill here can *build* anything. Using a
skill from Claude Code needs none of this — installation alone (see
[README.md](README.md#installation)) is enough for Claude to read it. The
moment you want to run a builder — a report, a fact pack, a showcase — you
need what follows.

This file is the **single owner** of machine setup: Python, the environment,
and the three root files including the secrets discipline. Other documents
link here rather than repeating any of it.

---

## 1. Python

The code uses modern syntax (`str | None` unions): **Python 3.10 or newer**.
The repo is developed on 3.14.

**Windows**

```powershell
winget install Python.Python.3.14
```

or download from [python.org/downloads](https://www.python.org/downloads/) —
tick *"Add python.exe to PATH"* in the installer.

**macOS**

```bash
brew install python
```

**Linux (Debian/Ubuntu)**

```bash
sudo apt install python3 python3-venv
```

Verify:

```bash
python --version        # 3.10+ (any shell; py --version also works on Windows)
```

## 2. Git

Needed to clone, to link (Option B in the README), and to pull updates.
Windows: `winget install Git.Git` (Git Bash comes with it). macOS:
`xcode-select --install` or `brew install git`. Linux: `sudo apt install git`.

## 3. Clone and create the venv

```bash
git clone https://github.com/vasilegrafu/aifx-finance.git
cd aifx-finance
python -m venv .venv
```

Install the dependencies — two libraries, and the tree needs no others
(Jinja renders every template, httpx is the only thing that touches the
network):

```powershell
.venv\Scripts\activate                    # PowerShell
pip install -r requirements.txt
```

```bash
source .venv/bin/activate                 # macOS / Linux
pip install -r requirements.txt
```

**Run everything through the venv's interpreter** — on this repo that is
spelled out as:

```bash
./.venv/Scripts/python.exe <script>       # Windows      (NOT bare `python`)
./.venv/bin/python <script>               # macOS / Linux
```

Bare `python` outside the venv has no `jinja2` and fails on the first import.
Invoking the venv's interpreter by path works from any shell without
activating, which is how the commands in every document here are written.

## 4. The three root files

One **environment declaration** selects a **tracked config** and an
**untracked secrets** file together, so a run can never read dev settings
against a prod key. All three sit at the repo root, beside `.claude/`.

### `environment.json` — tracked, already in the repo

```json
{ "environment": "dev" }
```

Or set `ENVIRONMENT` in the shell, which wins over the file. There is no flag
and no default anywhere: a flag would reach only one entry point, and a shell
variable cannot be inherited by every tool that spawns a build. The file is
deliberately **not** named `.env` — that name is where every tutorial says to
put an API key, and this file is tracked; a name nobody reaches for by reflex
is a name that can be committed safely.

### `config.dev.json` / `config.prod.json` — tracked, already in the repo

What is not secret:

```json
{
  "service_providers": {
    "fmp": {
      "api_url": "https://financialmodelingprep.com/stable"
    }
  }
}
```

An `api_key` in a config file is rejected at run time, on purpose.

### `secrets.dev.json` — never tracked, you write it by hand

```json
{
  "fmp": {
    "api_key": "<your-fmp-api-key>"
  }
}
```

Add `secrets.prod.json` in the same shape if you use a separate production
key.

**There is deliberately no `secrets.example.json` to copy.** `.gitignore`
matches `secrets.*.json` with **no exception**, so nothing by that name can
ever be staged. A tracked template would need a negation in `.gitignore`, and
a negation is one mis-ordered line away from publishing a key — in a
repository that is public *and* served by jsDelivr, where anything committed
is fetchable at a URL by anyone who guesses the path. Writing four lines of
JSON is cheaper than that risk.

The split is per **file**, not per field: config is tracked, secrets are not,
so "is this safe to commit?" is decided once for the file rather than judged
every time someone adds a field.

**In CI**, set the `FMP_API_KEY` environment variable instead — it wins over
the file and needs no file at all.

## 5. The FMP key

Both skills read market and fundamentals data from
[Financial Modeling Prep](https://financialmodelingprep.com/). Create an
account and generate an API key from the dashboard. The endpoint notes in
both skills (`…/finance-reports/service_providers/fmp/endpoints.md` and
`…/strategic-company-analysis/data/endpoints.md`) assume the **Starter**
plan and document what it gates; a free key runs the same code against a
smaller endpoint surface.

## 6. Verify the install — free checks first

Neither of these spends an API call:

```bash
./.venv/Scripts/python.exe .claude/skills/finance-reports/status.py
./.venv/Scripts/python.exe .claude/skills/strategic-company-analysis/check.py
```

`status.py` prints which install you got (a linked skill resolves to the
clone's path, a copied one to your project's) and whether anything is stale;
`check.py` verifies the strategic skill's internal consistency. Each skill's
README says how to read the output.

A **live** smoke test costs ~13 API calls per run — real quota, so run it once
you actually want data, not as a reflex:

```bash
./.venv/Scripts/python.exe .claude/skills/strategic-company-analysis/data/fact_pack.py AAPL
```

Every run prints which environment it resolved and where the key came from
(never the key) before spending the first call.

## 7. If you COPIED a skill instead of cloning

A copied skill is a real file tree in your project and resolves everything
relative to its own `.claude/`, so your project's root needs its own copies
of the three files above — and you must add `secrets.*.json` to **your**
project's `.gitignore` yourself, since this repo's cannot reach it. A copied
`finance-reports` additionally needs a `version.json` beside `.claude/`
(`status.py` says so in a sentence instead of a traceback). A **linked**
skill resolves back through the junction into the clone and needs none of
this: one machine, one set of credentials, and nothing lands in your project.
