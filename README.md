# aifx-finance

**A versioned toolbox for Claude Code — skills in one public repo, dropped into
any project.**

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## The skills

Each skill owns its README — what it does and how to run it live there, not
here. `.claude/skills/` is the authoritative list; this index links what it
holds:

- **[finance-reports](.claude/skills/finance-reports/README.md)** — generates
  standalone HTML investing reports from live market data: a component
  library, every component with a built showcase page, and the report engine
  that builds documents out of them.
- **[strategic-company-analysis](.claude/skills/strategic-company-analysis/README.md)**
  — analyzes companies as strategic systems: modular external, competitive,
  financial, and scenario analysis producing prioritized recommendations,
  with a fact pack that reads live figures so none are recalled from memory.

`.claude/agents/` exists and is empty — the shelf is declared, nothing is on
it yet.

---

## Installation

### Option A — copy (simplest)

Grab any skill folder and paste it into your project. The MIT license allows
exactly this — take it, keep it, modify it.

```
<your-project>/.claude/skills/<skill-name>/   ← copied from aifx-finance/.claude/skills/<skill-name>/
```

Done. Claude Code discovers it next session. Your copy is frozen — it never
changes unless you update it yourself — and it resolves configuration
relative to its own `.claude/`, which has consequences
[SETUP.md](SETUP.md#7-if-you-copied-a-skill-instead-of-cloning) spells out.

### Option B — clone once, link everywhere (always updatable)

One shared clone on your machine serves ALL your projects through links.
Nothing you already have is touched — your own skills stay beside the links.

**1. Clone** once, anywhere (a good spot: next to your projects):

```bash
git clone https://github.com/vasilegrafu/aifx-finance.git
```

**2. Link each skill you want** into every project's `.claude/skills`,
next to your own:

```bat
:: Windows (junction — no admin rights needed)
mklink /J <project>\.claude\skills\<skill-name> <path-to>\aifx-finance\.claude\skills\<skill-name>
```

```bash
# macOS / Linux (symlink)
ln -s <path-to>/aifx-finance/.claude/skills/<skill-name> <project>/.claude/skills/<skill-name>
```

**3. Verify** — open Claude Code in the project: the skill appears in its
skills list.

**Linking is the better option if you intend to run the builders.** A linked
skill resolves back through the junction into this clone, so it reads the
clone's configuration and credentials: one set on the machine, and nothing
lands in your project.

**Update later** — one pull updates every project at once:

```bash
git -C <path-to>/aifx-finance pull            # latest
git -C <path-to>/aifx-finance checkout v8.0.0 # or pin a released version
```

What a version number promises is in [Versioning](#versioning) below — worth
reading before you pull across a major.

## Running the builders

Appearing in Claude Code's skills list means the skill was found; *building*
anything — a report, a fact pack — needs Python, a venv, and credentials.
**[SETUP.md](SETUP.md)** is the single owner of that path, from a bare
machine to a verified install. Each skill's README then documents its own
commands.

---

## Versioning

**One version governs the whole repository** — every skill under
`.claude/skills/`, the CSS, the JS, all of it. The single source of truth is
`version.json` at the root; no version number lives anywhere else. A skill
that versioned itself would let two skills in one clone disagree about which
CSS they were written against, and every generated page links that CSS by tag.

Each release is the git tag `v<version>`, and jsDelivr serves it at
`…/aifx-finance@<version>/.claude/skills/<skill>/…`.

**A published version is immutable.** Any change, however small, is a new
version — never a re-tag. Documents that have left this tree link their assets
by tag, so moving one would silently restyle pages nobody can find any more.

| bump | what changed | what it costs you |
|---|---|---|
| **PATCH** | a visual fix, no markup contract change | nothing — safe for every existing document |
| **MINOR** | additive: a new component, style, JS feature, or skill | nothing — old documents render unchanged |
| **MAJOR** | a markup contract changed, a skill was removed, **or a published command changed shape** | documents must opt in; a linked directory can vanish; a command from the previous release may stop working |

The MAJOR clause covers three different kinds of breakage because each one
arrived and found the contract silent about it. A removed skill did, before
5.0.0. A changed CLI did, at 8.0.0 — `--env`, required since 6.0.0, was
dropped; no document was affected at all, and it was still a break for anyone
with the old command in a script. **A release is major if a thing that worked
stops working**, whether the thing is a page, a link, or a line someone typed.

**Upgrading across a major is opt-in by construction.** An existing page keeps
pointing at the tag it was built against and keeps rendering; it moves only
when you regenerate it. Read the tag message — `git show v8.0.0` — for what
broke and what to do about it.

---

## License

[MIT](LICENSE) — use it, copy it, ship it.
