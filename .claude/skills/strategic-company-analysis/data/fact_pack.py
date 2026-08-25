"""fact_pack.py — live FMP figures for a strategic analysis, as labeled markdown.

The strategic-company-analysis skill forbids stating financial figures from
model memory ("read, don't recall"). This program is the mechanism: it reads
the figures a strategic analysis leans on — trend, margins, returns, capital
allocation, segments, peers — and prints them as a labeled markdown block with
one as-of timestamp, so the analysis can cite them as Facts.

    ./.venv/Scripts/python.exe .claude/skills/strategic-company-analysis/data/fact_pack.py \
        SYMBOL --peers A,B,C [--years 5] [--out FILE]

Peers are CHOSEN, not defaulted — pick the comparators the positioning module
named. Without --peers the peer table is omitted and says so.

The output carries live market data and differs on every run: it is an
artifact. NEVER commit it, wherever it was written.

What it deliberately does NOT do:
  - estimate a cost of capital (that is an analyst Assumption, not a read);
  - convert currencies (reportedCurrency is printed instead);
  - cache anything (a pack describes one stated moment; ~13 calls, pay it).
"""

import argparse
import sys
from datetime import datetime

from client import FmpClient, FmpError
from credentials import describe, environment

# ---------------------------------------------------------------- formatting

def _m(v):
    """Raw currency units -> millions, or None."""
    return None if v is None else v / 1e6


def fmt(v, decimals=0):
    """Millions with thousands separators; '·' for absent — absent must stay
    visibly absent, never become a plausible 0."""
    if v is None:
        return "·"
    try:
        # FMP serves some counts (e.g. fullTimeEmployees) as strings.
        return f"{float(v):,.{decimals}f}"
    except (TypeError, ValueError):
        return str(v)


def pct(numerator, denominator):
    """A percentage as 'x.x%', or '·' when either side is missing/zero."""
    if numerator is None or not denominator:
        return "·"
    return f"{100 * numerator / denominator:.1f}%"


def pct_of(ratio):
    """A ratio (0.19) as '19.0%', or '·'."""
    return "·" if ratio is None else f"{100 * ratio:.1f}%"


def year_of(row):
    """A statement row's fiscal-year label: fiscalYear if FMP sent one, else
    the date's year — statements and key-metrics must join on the same key."""
    fy = row.get("fiscalYear")
    return str(fy) if fy else str(row.get("date", "?"))[:4]


def chron(rows):
    """Oldest first. FMP returns newest first; every table here reads
    left-to-right in time."""
    return sorted(rows, key=lambda r: r.get("date") or "")


# ------------------------------------------------------------------ sections

def annual_table(inc, cf, km, years):
    """The multi-year read: growth, margins, intensity, cash, returns."""
    inc, cf = chron(inc)[-years - 1:], chron(cf)
    km_by_year = {year_of(r): r for r in km}
    cf_by_year = {year_of(r): r for r in cf}

    lines = ["| FY | revenue | growth | gross | operating | net | R&D/rev | FCF | ROIC |",
             "|---|---|---|---|---|---|---|---|---|"]
    prev_rev = None
    for row in inc:
        rev = row.get("revenue")
        year = year_of(row)
        growth = (f"{100 * (rev - prev_rev) / prev_rev:+.1f}%"
                  if rev is not None and prev_rev else "·")
        fcf = _m((cf_by_year.get(year) or {}).get("freeCashFlow"))
        roic = (km_by_year.get(year) or {}).get("returnOnInvestedCapital")
        lines.append(f"| {year} | {fmt(_m(rev))} | {growth} "
                     f"| {pct(row.get('grossProfit'), rev)} "
                     f"| {pct(row.get('operatingIncome'), rev)} "
                     f"| {pct(row.get('netIncome'), rev)} "
                     f"| {pct(row.get('researchAndDevelopmentExpenses'), rev)} "
                     f"| {fmt(fcf)} | {pct_of(roic)} |")
        prev_rev = rev

    revs = [r.get("revenue") for r in inc if r.get("revenue")]
    if len(revs) >= 3 and revs[0] > 0 and revs[-1] > 0:
        n = len(revs) - 1
        cagr = (revs[-1] / revs[0]) ** (1 / n) - 1
        lines.append(f"\nRevenue CAGR over the {n} shown periods: "
                     f"**{100 * cagr:+.1f}%**")
    return "\n".join(lines)


def ttm_section(inc_q, cf_q, inc_annual, cf_annual):
    """TTM, reconstructed and labeled — the TTM endpoints are plan-gated, and
    an annual figure standing in for a trailing one is the documented trap."""
    inc_q = sorted(inc_q, key=lambda r: r.get("date") or "", reverse=True)
    cf_q = sorted(cf_q, key=lambda r: r.get("date") or "", reverse=True)
    if len(inc_q) < 4 or len(cf_q) < 4:
        return ("_TTM omitted: fewer than four reported quarters available — "
                "state trailing figures only from a source that has them._")

    def q_sum(rows, key):
        vals = [r.get(key) for r in rows[:4]]
        return None if any(v is None for v in vals) else sum(vals)

    latest_fy = chron(inc_annual)[-1]
    latest_cf_fy = chron(cf_annual)[-1]
    lines = [f"**RECONSTRUCTED**: sum of the four quarters ending "
             f"{inc_q[0].get('date', '?')} (TTM endpoints are plan-gated). "
             f"Latest full FY ({year_of(latest_fy)}) beside it for drift:",
             "",
             "| line | TTM (reconstructed) | latest FY |",
             "|---|---|---|"]
    for label, key, rows, fy_val in [
            ("revenue", "revenue", inc_q, latest_fy.get("revenue")),
            ("operating income", "operatingIncome", inc_q, latest_fy.get("operatingIncome")),
            ("net income", "netIncome", inc_q, latest_fy.get("netIncome")),
            ("operating cash flow", "operatingCashFlow", cf_q,
             latest_cf_fy.get("operatingCashFlow")),
            ("free cash flow", "freeCashFlow", cf_q,
             latest_cf_fy.get("freeCashFlow"))]:
        lines.append(f"| {label} | {fmt(_m(q_sum(rows, key)))} "
                     f"| {fmt(_m(fy_val))} |")

    if len(inc_q) >= 5:
        q0, q4 = inc_q[0].get("revenue"), inc_q[4].get("revenue")
        if q0 and q4:
            lines.append(f"\nLatest quarter ({inc_q[0].get('date', '?')}) revenue "
                         f"YoY: **{100 * (q0 - q4) / q4:+.1f}%**")
    return "\n".join(lines)


def balance_section(bs):
    row = chron(bs)[-1]
    cash = row.get("cashAndShortTermInvestments", row.get("cashAndCashEquivalents"))
    debt = row.get("totalDebt")
    equity = row.get("totalStockholdersEquity", row.get("totalEquity"))
    net_debt = debt - cash if debt is not None and cash is not None else None
    return "\n".join([
        f"As at {row.get('date', '?')} (annual statement):",
        "",
        f"- cash & short-term investments: {fmt(_m(cash))}",
        f"- total debt: {fmt(_m(debt))}  →  net debt: {fmt(_m(net_debt))}",
        f"- total equity: {fmt(_m(equity))}",
        f"- total assets: {fmt(_m(row.get('totalAssets')))}"])


def capital_allocation(cf, years):
    """Where the money actually went — the ledger the management module reads
    against the narrative. FMP reports outflows negative; shown as magnitudes."""
    cf = chron(cf)[-years:]

    def total(*keys):
        vals = []
        for row in cf:
            v = next((row.get(k) for k in keys if row.get(k) is not None), None)
            if v is not None:
                vals.append(abs(v))
        return sum(vals) if vals else None

    span = f"{year_of(cf[0])}–{year_of(cf[-1])}" if cf else "?"
    fcf_total = sum(r.get("freeCashFlow") or 0 for r in cf)
    return "\n".join([
        f"Cumulative over FY{span} (magnitudes; outflows reported negative by FMP):",
        "",
        "| destination | cumulative |",
        "|---|---|",
        f"| capital expenditure | {fmt(_m(total('capitalExpenditure')))} |",
        f"| buybacks | {fmt(_m(total('commonStockRepurchased')))} |",
        f"| dividends | {fmt(_m(total('netDividendsPaid', 'dividendsPaid')))} |",
        f"| acquisitions (net) | {fmt(_m(total('acquisitionsNet')))} |",
        f"| _free cash flow generated_ | {fmt(_m(fcf_total))} |"])


def segments_section(seg):
    rows = sorted(seg, key=lambda r: r.get("fiscalYear") or 0)
    latest = rows[-1]
    data = latest.get("data") or {}
    if not data:
        return "_Segmentation returned no data rows._"
    total = sum(v for v in data.values() if v) or None
    lines = [f"FY{latest.get('fiscalYear', '?')} revenue by segment "
             f"(FMP publishes revenue only — no segment profit here):",
             "", "| segment | revenue | share |", "|---|---|---|"]
    for name, value in sorted(data.items(), key=lambda kv: -(kv[1] or 0)):
        lines.append(f"| {name} | {fmt(_m(value))} | {pct(value, total)} |")
    return "\n".join(lines)


def peers_section(km_self, peers, symbol):
    lines = ["Latest annual key-metrics; the subject first. Peers are the ones "
             "ASKED FOR — relevance was the caller's judgment, not a screen.",
             "",
             "| company | ROIC | capex/rev | R&D/rev | SBC/rev | EV/EBITDA |",
             "|---|---|---|---|---|---|"]

    def cells(m):
        # `researchAndDevelopementToRevenue` is FMP's spelling — see endpoints.md.
        ev = m.get("evToEBITDA")
        return (f"| {pct_of(m.get('returnOnInvestedCapital'))} "
                f"| {pct_of(m.get('capexToRevenue'))} "
                f"| {pct_of(m.get('researchAndDevelopementToRevenue'))} "
                f"| {pct_of(m.get('stockBasedCompensationToRevenue'))} "
                f"| {fmt(ev, 1) if ev is not None else '·'} |")

    lines.append(f"| **{symbol}** {cells(chron(km_self)[-1])}")
    for ticker, metrics in peers.items():
        if metrics is None:
            # The reason is already in the warnings block; the row just stays
            # visibly absent rather than silently dropped.
            lines.append(f"| {ticker} | · | · | · | · | · |")
        else:
            lines.append(f"| {ticker} {cells(metrics[0])}")
    return "\n".join(lines)


# ---------------------------------------------------------------------- main

def build(symbol, peer_list, years):
    client = FmpClient()
    print(f"fact_pack: environment {environment()!r}, {describe()}",
          file=sys.stderr)

    p = client.get_many([
        ("profile", {"symbol": symbol}),
        ("quote", {"symbol": symbol}),
        ("income-statement", {"symbol": symbol, "period": "annual", "limit": years + 1}),
        ("balance-sheet-statement", {"symbol": symbol, "period": "annual", "limit": 2}),
        ("cash-flow-statement", {"symbol": symbol, "period": "annual", "limit": years + 1}),
        ("key-metrics", {"symbol": symbol, "period": "annual", "limit": years + 1}),
        ("financial-scores", {"symbol": symbol}),
    ])
    p["inc_q"] = client.get("income-statement", symbol=symbol, period="quarter", limit=5)
    p["cf_q"] = client.get("cash-flow-statement", symbol=symbol, period="quarter", limit=4)

    warnings = []
    # Segmentation legitimately fails for some issuers (banks, some foreign
    # filers) — a warning, not a dead pack. Everything above is load-bearing
    # and fails the whole run loudly instead.
    try:
        p["seg"] = client.get("revenue-product-segmentation", symbol=symbol,
                              period="annual")
    except FmpError as exc:
        p["seg"] = None
        warnings.append(f"segmentation unavailable: {exc}")

    p["peers"] = {}
    for peer in peer_list:
        try:
            p["peers"][peer] = client.get("key-metrics", symbol=peer,
                                          period="annual", limit=1)
        except FmpError as exc:
            p["peers"][peer] = None
            warnings.append(f"peer {peer}: {exc}")

    return p, warnings, client.calls_made


def render(symbol, p, warnings, calls, peer_list, years):
    profile, quote = p["profile"][0], p["quote"][0]
    scores = p["financial-scores"][0]
    currency = (chron(p["income-statement"])[-1].get("reportedCurrency")
                or profile.get("currency") or "?")
    stamp = datetime.now().isoformat(timespec="seconds")

    out = [f"# FMP fact pack — {symbol} — {stamp}", ""]
    out.append(f"Every figure below was READ from the FMP API at the timestamp "
               f"above; nothing is recalled or estimated. Monetary figures in "
               f"millions of {currency}. Rows marked RECONSTRUCTED are summed "
               f"from reported quarters. This output is an artifact carrying "
               f"live data — never commit it.")
    if warnings:
        out += ["", "**Warnings (missing pieces, said loudly):**"]
        out += [f"- {w}" for w in warnings]

    out += ["", "## Identity", "",
            f"- {profile.get('companyName', symbol)} — "
            f"{profile.get('exchange', '?')}: {symbol}",
            f"- sector / industry: {profile.get('sector', '·')} / "
            f"{profile.get('industry', '·')}",
            f"- country: {profile.get('country', '·')}; employees: "
            f"{fmt(profile.get('fullTimeEmployees'))}",
            f"- market cap: {fmt(_m(quote.get('marketCap')))}  ·  price: "
            f"{quote.get('price', '·')}  ·  beta: {profile.get('beta', '·')}"]

    out += ["", f"## Annual trend (up to {years}y + base year)", "",
            annual_table(p["income-statement"], p["cash-flow-statement"],
                         p["key-metrics"], years)]
    out += ["", "## Trailing twelve months", "",
            ttm_section(p["inc_q"], p["cf_q"], p["income-statement"],
                        p["cash-flow-statement"])]
    out += ["", "## Balance sheet snapshot", "", balance_section(p["balance-sheet-statement"])]
    out += ["", "## Capital allocation", "",
            capital_allocation(p["cash-flow-statement"], years)]

    out += ["", "## Segments", ""]
    out.append(segments_section(p["seg"]) if p["seg"]
               else "_Segmentation unavailable for this issuer — see warnings._")

    z_score = scores.get("altmanZScore")
    out += ["", "## Composite scores", "",
            f"- Altman Z: {fmt(z_score, 2)}   ·   Piotroski: "
            f"{scores.get('piotroskiScore', '·')}",
            "",
            "> `financial-scores` computes with its OWN marketCap and EBIT,",
            "> which differ from key-metrics and the statements for the same",
            "> fiscal year — as-of different moments, neither wrong. Say which",
            "> source a number came from if it matters."]

    out += ["", "## Peer comparison", ""]
    out.append(peers_section(p["key-metrics"], p["peers"], symbol) if peer_list
               else "_No peers requested. Peers are chosen, not defaulted — "
                    "rerun with --peers using the comparators the positioning "
                    "module named._")

    out += ["", "## For the value-creation test", "",
            "ROIC above is READ. Cost of capital is deliberately NOT provided "
            "— estimate it explicitly in the analysis and label it an "
            "Assumption; the pack does not invent one.",
            "",
            f"---", f"_{calls} API calls · environment {environment()!r} · "
            f"generated {stamp} · artifact: do not commit._"]
    return "\n".join(out) + "\n"


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(
        description="Live FMP figures for a strategic analysis, as labeled markdown.")
    parser.add_argument("symbol", help="ticker, e.g. AAPL")
    parser.add_argument("--peers", default="",
                        help="comma-separated tickers — chosen, not defaulted")
    parser.add_argument("--years", type=int, default=5,
                        help="annual window (default 5)")
    parser.add_argument("--out", help="write to this file instead of stdout "
                                      "(an artifact either way — never commit it)")
    args = parser.parse_args()

    symbol = args.symbol.upper()
    peer_list = [t.strip().upper() for t in args.peers.split(",") if t.strip()]

    try:
        payloads, warnings, calls = build(symbol, peer_list, args.years)
    except FmpError as exc:
        raise SystemExit(f"fact_pack: {exc}")

    document = render(symbol, payloads, warnings, calls, peer_list, args.years)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(document)
        print(f"fact_pack: wrote {args.out} ({calls} calls)", file=sys.stderr)
    else:
        print(document)


if __name__ == "__main__":
    main()
