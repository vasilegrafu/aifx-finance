# USER-MANUAL — driving the strategic-company-analysis skill

For **humans**. The model never reads this file — it reads
[SKILL.md](SKILL.md), which is why everything here works. This manual owns
exactly one thing: **what to type, what comes back, and what to say when the
answer is not good enough.** What the skill costs to run and how to install
it is [README.md](README.md)'s; what the modules contain is theirs.

The skill's interface is natural language. You do not name modules or pass
flags — your phrasing selects the depth and the lens. This manual is a
phrasebook.

---

## Start here — three prompts, three different sizes

> **"Quick take on Nike."**

One page: position, moat verdict, the central tension, two or three things to
watch. Minutes, not a report.

> **"Analyze Nike strategically."**

A short memo: diagnosis with sized issues and a defended recommendation.

> **"Full strategic case analysis of Nike."**

The complete report — industry structure through falsification, per the forms
the skill carries.

The words *quick*, *analyze*, and *full case* are doing the work. If you get
more than you wanted, say so — *"shorter — just the diagnosis"* works at any
point.

---

## Guided exploration — the flagship way to use it

If you do not already know what you want to ask, do not guess — let the
analysis lead. Say any of:

> **"Walk me through Deere & Co."**
> **"Help me understand what kind of business Adyen actually is."**
> **"Let's explore Disney together — surface what's interesting."**

What happens: an opening scan (business model plus live figures for a listed
company), then a short map — *"three things look interesting here"* — and
from then on, every step ends with **offers**: two or three places the
finding points, each phrased as what it would settle. You pick, redirect, or
say *"you choose."*

Steering phrases that work at any step:

| you say | what happens |
|---|---|
| *"go deeper on that"* | the current thread, one level down |
| *"you choose"* | the highest-value thread, with the reason stated |
| *"what haven't we looked at?"* | the coverage map — and whether the gaps could change the verdict |
| *"synthesize"* | jumps to the diagnosis with what has been gathered, gaps declared |
| *"finish it"* | the remaining pipeline runs in batch; you get the full document |
| *"park that, come back to X"* | thread saved, focus moves |

A guided session that wandered through enough ground can end as a real memo —
just ask for it. There is a condensed transcript of a session at the
[end of this manual](#a-worked-session).

---

## By what you are asking

### The whole company

> *"What's the strategic situation at Starbucks?"* — standard memo.
> *"Is LVMH's success the industry or the company?"* — a sharper full-company
> question; expect the industry-vs-position attribution to carry the answer.

### One aspect — the reason the skill is modular

Each of these loads one lens, not the whole pipeline:

> *"Does Costco actually have a durable moat? Explain the mechanism."*
> *"Run five forces on the European low-cost airline industry."*
> *"Why does anyone choose Bing over Google? Who is Microsoft's real
> competitor there?"*
> *"Is Oracle's management good at capital allocation? Check the ledger, not
> the narrative."*
> *"Where in Zara's value chain does the speed advantage actually live?"*
> *"Does Amazon's conglomerate structure add value, or would the pieces be
> worth more apart?"*
> *"What would have to be true for Rivian to ever earn its cost of capital?"*
> *"What kills Salesforce? Give me scenarios with early warnings, not a risk
> list."*

### A decision

> *"Should Netflix get into live sports — build, buy, or partner?"*
> *"Spotify is considering hardware again. Steelman it, then tell me why
> it's probably wrong — or right."*
> *"Our company [describe it] is choosing between deepening in DACH or
> entering France. Frame the choice."*

Decision questions get the alternatives treatment: a do-nothing baseline and
the post-retaliation test — what the move looks like *after* competitors
respond, not before.

### A comparison

> *"Compare Visa and Mastercard strategically — where do they actually
> differ?"*
> *"UPS vs FedEx: same industry, different economics. Why?"*

Comparisons come back on one scoring frame with prose only where the
companies genuinely differ — never two reports stapled together.

### An industry with no company attached

> *"Is enterprise cybersecurity a structurally good industry to be in?"*
> *"Where do the profit pools sit in the EV supply chain?"*

### A post-mortem

> *"Why did Peloton's advantage evaporate? What was temporary and what was
> real?"*
> *"What did Nokia's management actually get wrong strategically — not in
> hindsight-hero terms?"*

Post-mortems force the temporary-vs-durable distinction, which is where most
casual accounts of failure go wrong.

---

## By who you are

Say who you are — it changes emphasis and form, not rigor:

> **Student:** *"Strategic management case analysis of IKEA for a
> university course — use Porter and RBV explicitly and define the
> concepts."* → academic mode: definitions, frameworks connected, an
> assumptions section.
>
> **Investor:** *"I'm long NVDA. Attack my thesis — what would make the moat
> verdict wrong, and what would I see first?"* → the falsification loop as
> the main course.
>
> **Operator:** *"I run a 40-person specialty coffee roaster [context].
> A private-equity-backed rollup entered our region. What are my real
> options?"* → capability- and capital-constrained alternatives; no
> Fortune-500 advice.
>
> **Consultant:** *"Client-ready two-pager on Siemens Healthineers'
> strategic position — decisive, calibrated language."*
>
> **Interview candidate:** *"Mock case: coach me through analyzing a
> D2C mattress company. Ask, don't tell — correct my reasoning as I go."*
> → guided mode inverted: you drive, the skill referees.

---

## By what the company is

- **Listed large cap** — the default everything above assumes; figures come
  live from the fact pack.
- **Thin-data small cap** — expect visible `·` gaps and loud warnings rather
  than smoothed-over blanks; the analysis says what the gaps could change.
- **Private company** — *"Analyze IKEA"* works: public information plus
  benchmarks from listed peers, every estimate labeled as one, never
  pretending the financials are known.
- **Startup** — *"Assess Anduril strategically"* shifts to unit economics,
  product-market fit evidence, capital runway, and imitation-once-proven;
  traditional ratios are not forced onto a company they do not fit.
- **Conglomerate** — *"Analyze Samsung Electronics — and don't blend the
  segments"* triggers the profit-engine discipline; you can also aim at one
  unit: *"just the foundry business."*
- **Regulated** — banks, pharma, utilities, defense: regulation is analyzed
  as industry structure (who the regulator is, direction of travel), not a
  bullet in a risk list.
- **Platform** — network effects get tested, not asserted: which side values
  which, where multi-homing breaks the lock.
- **Turnaround** — *"Is Bayer fixable? What's the honest downside?"* — the
  do-nothing baseline matters most here and is always priced.

---

## Working with live data

For any listed company where figures will appear, the skill runs its fact
pack first — that is the *read, don't recall* rule, and it is why the numbers
in the analysis carry as-of dates instead of being confident memories.

What you control with phrasing:

> *"Analyze AMD **versus NVDA and INTC**"* — peers are **chosen, not
> defaulted**. Name the comparators you consider fair; unnamed, the peer
> table is omitted and the analysis says so.
>
> *"Fresh numbers, please"* — nothing is cached; every run is live. Each run
> costs real API quota (README.md says how much), so a long session reuses
> the pack from earlier in the conversation rather than re-pulling per
> question. Ask for a re-pull when staleness would matter.
>
> *"Is that figure read or recalled?"* — the enforcement question. Any
> load-bearing number should be a labeled **Fact** with a source, or flagged
> `[recalled — verify]`.

The pack's output is a live-data artifact: it can be written to a file for
your reference, but it never gets committed to this repository.

---

## Judging the output — weak-answer signs and the phrase that fixes each

The skill is built to avoid these, but you should be able to catch them.
This table is the manual's most valuable section:

| weak-answer sign | say this |
|---|---|
| "Strong brand" / "network effects" named, mechanism absent | *"Give me the causal chain on that — why can't a rival with money copy it?"* |
| A recommendation with no trade-off | *"What does management stop doing? What does this cost?"* |
| Framework tables instead of a conclusion | *"Skip the frameworks — what's the actual problem, in three sentences?"* |
| Hedged non-conclusion ("it depends", "balanced approach") | *"Pick one and defend it. What must be true for you to be right?"* |
| A number with no label or date | *"Read or recalled? Show the source and as-of."* |
| Issues listed but not ranked | *"Size those — which one is the biggest in money terms?"* |
| Durability argued from history ("20 great years") | *"History isn't a mechanism. What protects it for the NEXT five?"* |
| Growth praised without economics | *"Above or below the cost of capital? Show the sketch."* |
| An option priced as if rivals stand still | *"What does this look like AFTER competitors respond?"* |
| Advice ignoring who runs the company | *"Can THIS management team, with THESE incentives, execute that?"* |
| Analysis that never says what would change its mind | *"What would prove this wrong, and what would I see first?"* |

If a claim survives your challenge, you learned why it holds. If it folds,
the analysis just got better. Either way you win — challenge freely.

---

## Troubleshooting

| symptom | what it means / what to do |
|---|---|
| No figures appear for a listed company | The fact pack likely was not run — say *"pull the fact pack first."* |
| `fact_pack: … empty response` | Wrong ticker, or FMP does not cover it (some foreign listings). Try the primary listing's symbol. |
| `HTTP 402/403` naming endpoints.md | A plan-gated endpoint — `data/endpoints.md` says what the Starter plan can and cannot reach. |
| No credential / environment errors | Machine setup — [SETUP.md](../../../SETUP.md) owns the fix, step by step. |
| Segments section says unavailable | Real: some issuers (banks, some foreign filers) have no segmentation endpoint data. The analysis proceeds and says what it cannot see. |
| Peer row is all `·` | That peer's fetch failed (named in warnings). Swap it or accept the gap. |
| Figures look off by a currency | Nothing converts, on purpose — the pack states `reportedCurrency` once; check it before comparing across borders. |
| The answer is far too long | Say the tier you wanted: *"quick take"*, *"one page"*, *"just the diagnosis."* |
| You disagree with the analysis | Best case. Say why — your objection is evidence, and the falsification machinery is built to take it. |

---

## A worked session

Condensed from a real guided-mode shape — your lines in bold:

> **"Walk me through Microsoft."**
>
> *Scan: fact pack pulled (13 calls, as-of stated). Map: three things stand
> out — (1) capex has exploded to ~35% of revenue, triple the software norm;
> (2) operating margin is rising anyway; (3) one segment cluster is ~70% of
> revenue. Where do we start?*
>
> **"The capex. That looks like it changes what kind of company this is."**
>
> *Finding: the ledger says Microsoft is becoming capital-intensive
> infrastructure — ~$277B deployed over five years, most of it recent, into
> AI datacenters. ROIC has drifted down five years straight while margins
> rose: the classic signature of a company trading return quality for a
> position. This points three places: (a) does the moat logic change when
> the product needs $60B/yr of concrete? (b) can rivals match this spend —
> industry structure? (c) is management's capital discipline trustworthy at
> this scale? Which?*
>
> **"You choose."**
>
> *(b), because it decides whether the spend is a moat or an arms race: if
> only three companies can play, the capex IS the entry barrier and the
> falling ROIC is the price of an oligopoly seat…*
>
> **"What haven't we looked at?"**
>
> *Covered: business model, capital allocation, industry structure (partly).
> Untouched: competitive position per segment, scenarios. The scenario gap
> matters — everything so far assumes AI demand materializes; that
> assumption deserves a falsifier before you trust any conclusion.*
>
> **"Synthesize."**
>
> *Diagnosis with what we have — two issues sized, one explicitly thin
> (positioning was never tested against the next-best alternative), and the
> falsification table's first row is the AI-demand assumption with its
> early-warning indicator…*

That is the intended rhythm: finding → offers → your call → repeat, with an
honest map and an exit whenever you want the document instead of the
conversation.
