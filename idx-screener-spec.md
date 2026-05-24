# IDX Screener & Paper Trading System — Spec

A macOS-native application that runs codified book-derived skills as deterministic scorers over IDX stocks, surfaces ranked candidates, and supports a full paper-trading lifecycle from analysis to exit.

---

## 1. Goals and non-goals

### Goals
- Run quantitative + qualitative screens over the IDX universe (or a watchlist) using rules codified from the 21 book skills.
- Combine fundamental, bandar-flow, and tape signals into a single composable scoring engine.
- Provide a paper-trading workflow: thesis → entry → monitor → exit, with all decisions journaled.
- Be inspectable: every score, every signal, every recommendation traces back to a rule and a data field.
- Run locally on macOS with a native Swift/SwiftUI front-end and a Python analytical backend.

### Non-goals
- Real broker execution (paper only).
- Real-time tick data ingestion (works on end-of-day + intraday snapshots).
- ML / model training. Rules are deterministic and human-readable.
- Multi-market support in v1. IDX only.

---

## 2. Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  macOS app (Swift + SwiftUI)                                │
│  - Universe browser, screener UI, stock detail, journal     │
│  - Charts (Swift Charts), broker-flow visualizations        │
│  - Talks to Python engine via local HTTP (loopback)         │
└─────────────────────────────────────────────────────────────┘
                            │ HTTP/JSON
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Python engine (FastAPI, runs as launchd background agent)  │
│  - Data adapter (reads mock JSON; later: real data)         │
│  - Skill modules (one .py per SKILL.md)                     │
│  - Composite scorer, screener runner                        │
│  - Paper portfolio + trade lifecycle                        │
│  - SQLite for state                                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Data layer                                                 │
│  - JSON mock today (universe list, market snapshot, detail) │
│  - SQLite for portfolio, journals, signal history           │
│  - Pluggable adapter for future real-time sources           │
└─────────────────────────────────────────────────────────────┘
```

**Why this split.** SwiftUI gives a fast, native macOS feel and good charting. Python is where the analytical libraries live (pandas, numpy) and where the skill rules are easy to express. The two communicate over local HTTP so the engine can be developed and tested independently of the UI.

---

## 3. Data contracts

The system assumes three primary inputs (mocked as JSON today, real data later). All schemas are normalized to these contracts; adapters convert from whatever source format.

### 3.1 Universe list (`universe.json`)

The output of an upstream screener — list of stock codes plus minimal metadata to drive batch operations.

```json
{
  "as_of": "2026-05-23T16:00:00+07:00",
  "exchange": "IDX",
  "stocks": [
    {
      "code": "BBCA",
      "name": "Bank Central Asia",
      "sector": "Financial",
      "subsector": "Banks",
      "market_cap_idr": 1250000000000000,
      "adv_20d_idr": 450000000000,
      "free_float_pct": 45.2,
      "included_in": ["LQ45", "IDX30", "IDX80"]
    }
  ]
}
```

### 3.2 Market snapshot (`market.json`)

Index-level and breadth context. Drives "cycle" / Marks-style analysis and market regime gating.

```json
{
  "as_of": "2026-05-23T16:00:00+07:00",
  "indices": {
    "IHSG": { "close": 7340.5, "change_pct": 0.42, "ytd_pct": 8.1 },
    "LQ45": { "close": 1085.2, "change_pct": 0.31, "ytd_pct": 6.4 }
  },
  "breadth": {
    "advancers": 312,
    "decliners": 245,
    "unchanged": 88,
    "new_highs_52w": 42,
    "new_lows_52w": 18,
    "pct_above_200ma": 58.3
  },
  "flows": {
    "foreign_net_buy_idr": -120000000000,
    "foreign_net_buy_5d_idr": 480000000000,
    "foreign_net_buy_20d_idr": -1200000000000
  },
  "rates": {
    "bi_rate_pct": 5.75,
    "id_10y_govt_yield_pct": 6.82,
    "aaa_corp_yield_pct": 7.15
  },
  "valuation": {
    "ihsg_pe": 14.2,
    "ihsg_pe_5y_avg": 16.8,
    "ihsg_pb": 2.1
  }
}
```

### 3.3 Stock detail (`detail/{code}.json`)

The per-stock payload. Each section maps to one or more skills.

```json
{
  "code": "BBCA",
  "as_of": "2026-05-23T16:00:00+07:00",
  "key_stats": {
    "price": 9850,
    "market_cap_idr": 1250000000000000,
    "shares_outstanding": 126700000000,
    "pe_ttm": 24.5,
    "pe_5y_avg": 22.1,
    "pb": 5.2,
    "pb_5y_avg": 4.8,
    "ev_ebit": 18.3,
    "dividend_yield_pct": 2.4,
    "roe_ttm_pct": 22.1,
    "roe_5y_avg_pct": 21.0,
    "roic_ttm_pct": 18.5,
    "debt_to_equity": 0.12,
    "current_ratio": 1.45,
    "interest_coverage": 12.5,
    "beta_1y": 0.95,
    "high_52w": 10200,
    "low_52w": 8400
  },
  "financials": {
    "annual": [
      {
        "year": 2025,
        "revenue_idr": 95000000000000,
        "operating_income_idr": 58000000000000,
        "net_income_idr": 48000000000000,
        "eps": 379,
        "dps": 235,
        "operating_cash_flow_idr": 62000000000000,
        "capex_idr": 8000000000000,
        "maintenance_capex_idr": 5000000000000,
        "total_assets_idr": 1450000000000000,
        "total_equity_idr": 215000000000000,
        "long_term_debt_idr": 25000000000000,
        "current_assets_idr": 1180000000000000,
        "current_liabilities_idr": 820000000000000
      }
    ],
    "quarterly": [ /* trailing 8 quarters, same fields */ ]
  },
  "broker_summary": {
    "window_days": 20,
    "daily": [
      {
        "date": "2026-05-23",
        "total_volume": 45000000,
        "total_value_idr": 443250000000,
        "vwap": 9846,
        "by_broker": [
          {
            "broker_code": "RG",
            "broker_name": "Mandiri Sekuritas",
            "is_foreign": false,
            "buy_vol": 5200000,
            "sell_vol": 2100000,
            "buy_value_idr": 51200000000,
            "sell_value_idr": 20700000000,
            "net_value_idr": 30500000000,
            "buy_avg_price": 9846,
            "sell_avg_price": 9857
          }
        ]
      }
    ],
    "aggregated": {
      "top_5_net_buyers_20d": [
        { "broker_code": "RG", "net_value_idr": 280000000000, "days_as_top_buyer": 12 }
      ],
      "top_5_net_sellers_20d": [],
      "foreign_net_value_20d_idr": -45000000000,
      "concentration_hhi": 0.18
    }
  },
  "insider_activity": [
    {
      "date": "2026-05-15",
      "insider_name": "John Doe",
      "role": "President Director",
      "action": "buy",
      "shares": 1000000,
      "price": 9750,
      "value_idr": 9750000000
    }
  ],
  "news": [
    {
      "date": "2026-05-20",
      "headline": "BBCA announces share buyback program",
      "source": "IDX",
      "sentiment": "positive",
      "categories": ["buyback", "capital_allocation"]
    }
  ],
  "price_history": {
    "daily": [
      {
        "date": "2026-05-23",
        "open": 9800,
        "high": 9900,
        "low": 9790,
        "close": 9850,
        "volume": 45000000,
        "value_idr": 443250000000,
        "foreign_buy_vol": 12000000,
        "foreign_sell_vol": 14500000
      }
    ]
  },
  "corporate_actions": [
    { "date": "2025-12-01", "type": "dividend", "amount": 235, "ex_date": "2025-11-25" }
  ]
}
```

The mock JSON for the prototype can be hand-built for 5–10 stocks across diverse profiles (one classic value name, one fast grower, one bandar-active name, one cyclical, one distressed, etc.) to exercise every skill.

---

## 4. Codified skills — module structure

Each SKILL.md becomes a Python module exposing a uniform interface. The skill text guides the rule encoding; the module is what runs.

### 4.1 Skill interface

```python
# skills/base.py
from dataclasses import dataclass
from typing import Literal

@dataclass
class SignalResult:
    skill_id: str                          # e.g., "intelligent-investor"
    verdict: Literal["pass", "concern", "fail", "n/a"]
    score: float                           # 0..100, comparable across skills
    confidence: float                      # 0..1, how well the data supported the rules
    summary: str                           # one-line takeaway
    evidence: dict                         # rule-by-rule pass/fail with values
    triggers: list[str]                    # rules that fired (positive or negative)
    metadata: dict                         # skill-specific extras (target prices, phases, etc.)

class Skill:
    skill_id: str
    category: Literal["fundamental", "flow", "tape", "structural", "macro"]
    requires: list[str]                    # data sections needed ("financials", "broker_summary", ...)

    def applicable(self, detail: dict, market: dict) -> bool: ...
    def analyze(self, detail: dict, market: dict) -> SignalResult: ...
```

### 4.2 Skill modules — one-line summary per book

Each module turns the framework into rules. The codified version is necessarily a subset of the book — pick the rules that are objectively checkable. Keep the qualitative ones as narrative prompts surfaced in the UI for the user's own judgment.

| Skill | Category | Codifiable rules |
|---|---|---|
| `intelligent-investor` | fundamental | 7 defensive criteria + Graham V formula + margin-of-safety calc |
| `security-analysis` | fundamental | Earning power normalization, coverage tests, asset-value floor |
| `margin-of-safety` | fundamental | Multi-method valuation triangulation, downside scenarios, catalyst presence |
| `little-book-value-investing` | fundamental | P/E, P/B, P/CF, EV/EBIT, owner-earnings yield, safety, insider flag |
| `stock-market-genius` | structural | Detect corporate events (spin/M&A) from news+actions; analyze post-event |
| `most-important-thing` | macro | Cycle position from market.json; consensus vs. value gap |
| `common-stocks-uncommon-profits` | fundamental | Quantitative proxies for 15 points (R&D intensity, margins trend, etc.) |
| `essays-of-warren-buffett` | fundamental | Owner earnings, ROE/ROIC durability, capital allocation track |
| `poor-charlies-almanack` | fundamental | Inversion: 5 quantifiable failure-mode checks; moat proxy scoring |
| `one-up-on-wall-street` | fundamental | Six-category classifier; PEG; Lynch checklist signals |
| `bandarmology` | flow | Broker concentration, persistence, foreign vs. domestic, accumulation phase |
| `bandarmology-investment-style` | flow | Multi-month broker accumulation + fundamental floor combined |
| `trading-bandarmology` | flow | Daily flow shifts, setup typing, short-term confirmation |
| `trading-and-exchanges` | tape | Order-book proxies, liquidity-vs-info diagnosis where data permits |
| `dark-pools` | tape | Off-exchange volume share, block-print detection (limited on IDX) |
| `flash-boys` | tape | Execution cost estimation given trade size vs. ADV |
| `wyckoff-methodology` | tape | Phase identification from price/volume; spring/UTAD detection; P&F cause count |
| `trades-about-to-happen` | tape | Bar-by-bar effort/result diagnosis, Weis wave volumes |
| `volume-price-analysis` | tape | Spread+close+volume three-factor read; climactic-bar detection |
| `reminiscences-stock-operator` | tape | Trend strength, pivot-point detection, line of least resistance |
| `mind-over-markets` | tape | Market profile (POC/VAH/VAL); initiative vs. responsive activity |

### 4.3 Example: codifying `intelligent-investor`

```python
# skills/intelligent_investor.py
from .base import Skill, SignalResult

class IntelligentInvestor(Skill):
    skill_id = "intelligent-investor"
    category = "fundamental"
    requires = ["key_stats", "financials", "market"]

    def applicable(self, detail, market):
        return len(detail.get("financials", {}).get("annual", [])) >= 5

    def analyze(self, detail, market):
        ks = detail["key_stats"]
        annual = detail["financials"]["annual"]
        eps_series = [y["eps"] for y in annual if y.get("eps")]

        criteria = {}
        # 1. Adequate size — IDR 30T market cap as IDX threshold
        criteria["adequate_size"] = ks["market_cap_idr"] >= 30_000_000_000_000

        # 2. Financial strength
        latest = annual[0]
        criteria["financial_strength"] = (
            latest["current_assets_idr"] >= 2 * latest["current_liabilities_idr"]
            and latest["long_term_debt_idr"] <
                (latest["current_assets_idr"] - latest["current_liabilities_idr"])
        )

        # 3. Earnings stability — 10y positive
        criteria["earnings_stability"] = (
            len(annual) >= 10 and all(y["net_income_idr"] > 0 for y in annual[:10])
        )

        # 4. Dividend record — IDX-relaxed to 10y uninterrupted
        criteria["dividend_record"] = (
            len(annual) >= 10 and all(y.get("dps", 0) > 0 for y in annual[:10])
        )

        # 5. Earnings growth — 33% over 10y on 3y averages
        if len(eps_series) >= 10:
            start_avg = sum(eps_series[-3:]) / 3
            end_avg = sum(eps_series[:3]) / 3
            criteria["earnings_growth"] = end_avg >= 1.33 * start_avg
        else:
            criteria["earnings_growth"] = None

        # 6. Moderate P/E
        avg_eps_3y = sum(eps_series[:3]) / 3 if len(eps_series) >= 3 else None
        pe_on_3y = ks["price"] / avg_eps_3y if avg_eps_3y else None
        criteria["moderate_pe"] = pe_on_3y is not None and pe_on_3y <= 15

        # 7. Combined P/E x P/B
        criteria["combined_22_5"] = (pe_on_3y or 99) * ks["pb"] <= 22.5

        # Graham intrinsic value (need growth estimate)
        g = self._estimate_growth(eps_series)
        eps_ttm = eps_series[0]
        bond_yield = market["rates"]["aaa_corp_yield_pct"]
        v = eps_ttm * (8.5 + 2 * g) * 4.4 / bond_yield
        mos = (v - ks["price"]) / v if v > 0 else -1

        passed = sum(1 for v in criteria.values() if v is True)
        total = sum(1 for v in criteria.values() if v is not None)

        if passed == total and mos >= 0.33:
            verdict = "pass"
        elif passed >= total - 2 and mos >= 0.20:
            verdict = "concern"
        else:
            verdict = "fail"

        return SignalResult(
            skill_id=self.skill_id,
            verdict=verdict,
            score=min(100, (passed / total) * 70 + max(0, mos) * 30),
            confidence=min(1.0, len(annual) / 10),
            summary=f"{passed}/{total} defensive criteria, MoS {mos*100:.0f}%",
            evidence={
                "criteria": criteria,
                "graham_value": v,
                "current_price": ks["price"],
                "margin_of_safety_pct": mos * 100,
                "implied_growth_used": g,
            },
            triggers=[k for k, v in criteria.items() if v is False],
            metadata={"investor_type": "defensive"},
        )

    def _estimate_growth(self, eps_series):
        # Conservative CAGR over available window, capped
        if len(eps_series) < 5: return 5.0
        years = min(len(eps_series), 10) - 1
        if eps_series[-years-1] <= 0: return 5.0
        cagr = (eps_series[0] / eps_series[-years-1]) ** (1/years) - 1
        return max(0, min(15, cagr * 100))
```

The other skills follow the same pattern: extract the codifiable rules from the SKILL.md, leave qualitative judgment as narrative prompts.

### 4.4 Tape skills — what's possible without intraday

Several skills (Wyckoff, Weis, VPA, Market Profile) want intraday data ideally. With end-of-day OHLCV + daily volume only:

- **Possible**: trend identification, pullback detection, climactic-volume bars, weekly Wyckoff phases, daily VPA bar reads, Weis wave on daily.
- **Degraded**: bar-by-bar tape reading, intraday auction phases, Market Profile POC/VAH/VAL (need intraday TPO data).
- **Plan**: implement what works on daily; mark intraday-dependent rules as `n/a` when data is missing; design adapter to plug in intraday data later without changing skill code.

### 4.5 Bandarmology skills — IDX advantage

This is where IDX wins relative to US markets. Broker summary data lets the three bandar skills run at full strength:

- **Concentration scoring** — HHI of net buy across brokers
- **Persistence** — count of consecutive sessions same broker is net buyer
- **Phase mapping** — overlay Wyckoff phase detection with broker concentration
- **Foreign/domestic divergence** — broker classification flag drives this

Designed as the most differentiating part of the system; deserves the most polish.

---

## 5. Composite scoring

Skills produce comparable scores; the composite scorer combines them into a ranked recommendation.

### 5.1 Scoring tiers

```
tier 1 — Fundamental quality        (fund. skills, weighted)
tier 2 — Flow & smart money         (bandar + insider, weighted)
tier 3 — Tape / structure           (Wyckoff, VPA, Weis, profile)
tier 4 — Macro / cycle context      (Marks framework)
```

### 5.2 Composite logic

The composite is configurable, not hardcoded. Default presets:

**"Value compounder" preset** (Graham + Buffett + Fisher + Lynch stalwart):
- 60% fundamental tier
- 10% flow (insider buying weight, mild bandar)
- 20% tape (entry timing only — don't override fundamentals)
- 10% macro

**"Bandar trader" preset** (Filbert + Wyckoff + Weis + VPA):
- 15% fundamental (just survivability check)
- 55% flow (bandarmology heavy)
- 25% tape
- 5% macro

**"Special situation" preset** (Greenblatt + Klarman):
- 40% fundamental of post-event entity
- 20% flow
- 15% tape
- 25% macro (catalyst presence weighted here)

User-configurable: add custom presets with skill weights.

### 5.3 Hard filters

Some rules veto regardless of score:
- Insider selling persistent + price near 52w high → block "buy" recommendation
- Fundamental fail on key safety criteria (interest coverage < 1, negative equity) → block
- ADV too low for intended trade size → block

### 5.4 Output

```json
{
  "code": "BBCA",
  "composite_score": 72.4,
  "recommendation": "watchlist",
  "preset_used": "value-compounder",
  "tier_scores": {
    "fundamental": 78,
    "flow": 65,
    "tape": 70,
    "macro": 60
  },
  "top_positive_signals": [
    {"skill": "essays-of-warren-buffett", "signal": "owner earnings yield 5.2%, above corp bond yield"},
    {"skill": "intelligent-investor", "signal": "6/7 defensive criteria pass"}
  ],
  "top_negative_signals": [
    {"skill": "most-important-thing", "signal": "IHSG above 5y avg P/E; cycle late"}
  ],
  "blocked_by": [],
  "explainability_url": "/explain/BBCA"
}
```

---

## 6. Workflows

### 6.1 Screener workflow

```
1. User picks universe source (LQ45, IDX30, custom list)
2. User picks preset (or custom skill weights)
3. Engine loads universe + market snapshot
4. For each stock:
   a. Load stock detail
   b. Run all skills with .applicable() == True
   c. Compute composite score
5. Return ranked list with top signals
6. UI shows table — sort, filter, drill into any row
```

Run modes:
- **Full scan** — all universe stocks, takes ~minutes; runs nightly via launchd
- **Quick re-rank** — uses cached signals from last full scan + fresh tape/flow data
- **Single stock** — full skill run on demand

### 6.2 Stock-detail workflow

When user clicks a stock from the screener:

```
1. Show summary header: composite score, recommendation, key signals
2. Tabs:
   - Overview: composite breakdown by tier
   - Fundamentals: each fundamental skill's evidence dict, rendered as table
   - Bandar Flow: broker concentration chart, top buyers/sellers, persistence
   - Tape: price chart with Wyckoff phase overlay, Weis wave volume, VPA bars
   - Macro: where IHSG sits in cycle, sector rotation context
   - News & Insiders: timeline view
   - Skills Run: list of every skill executed, with raw output (debug/inspection)
3. Action buttons: "Add to watchlist" / "Paper buy" / "Set alert"
```

### 6.3 Paper trading workflow

```
1. User initiates paper buy from stock detail
2. Pre-trade dialog:
   - Quantity, price (limit or market-at-close)
   - Skill-derived suggestions: entry zone, stop, targets
   - Required: thesis text (1-3 sentences), expected hold horizon, sell triggers
3. Trade enters portfolio at fill price; cash deducted
4. Daily mark-to-market against close
5. Engine re-runs skills on holdings nightly:
   - Flag if thesis signals deteriorating
   - Flag if stop hit
   - Flag if target reached
6. User actions:
   - Add notes (journal)
   - Adjust stop/target
   - Paper sell (partial or full) — requires reason
7. On close, trade moves to history with:
   - P&L
   - Holding period
   - Original thesis vs. actual outcome
   - Skill signals at entry vs. at exit
```

### 6.4 Review workflow

Periodic review (weekly/monthly):
- Closed trades by skill that originated them — which skills produced winners, which produced losers
- Win rate, average winner, average loser, expectancy by preset
- Thesis adherence: did exits happen for stated reasons?
- Calibration: when skill X said "pass" with confidence 0.8, what was the realized outcome?

This is the system's learning loop. The skills don't update themselves, but the user does — adjusting weights, dropping skills that underperform, tightening rules.

---

## 7. macOS UI structure

### 7.1 Top-level navigation

Sidebar with sections:
- **Screener** — universe browser + filtered/ranked lists
- **Watchlist** — saved stocks
- **Portfolio** — open paper positions
- **Trade History** — closed positions
- **Journal** — chronological notes
- **Skills** — view/edit skill weights, see skill performance
- **Settings** — data sources, presets, alerts

### 7.2 Screener view

- Top: preset selector, universe selector, "Re-run" button, last-run timestamp
- Main: sortable table — code, name, sector, composite score, tier breakdown, top signal, change vs. last run
- Filters: sector, min score, must-pass-skill, exclude-blocked
- Right side panel: when row selected, preview of the analysis (deep dive on double-click)

### 7.3 Stock detail view

Multi-tab layout per workflow 6.2. Charts use Swift Charts — candlestick + volume + overlays for Wyckoff phases, MA lines, broker-flow shading.

Bandar Flow tab is the showcase visualization:
- Stacked area chart of cumulative net buy by top brokers over the window
- Heatmap of broker concentration daily
- Foreign vs. domestic flow line
- Annotations for detected accumulation/distribution phases

### 7.4 Portfolio view

- Open positions table: code, qty, avg cost, current price, P&L, days held, current composite score, alerts
- Cash balance and total portfolio value
- Each row clickable into position detail (history, journal, current signals)

### 7.5 Notifications

macOS native notifications for:
- Stop hit on open position
- Target reached
- Skill verdict change on holding (was "pass", now "fail")
- New high-conviction screener candidates after nightly run

---

## 8. State and persistence

SQLite for everything except market data. Schema:

```sql
-- portfolios
CREATE TABLE portfolios (
  id INTEGER PRIMARY KEY,
  name TEXT, starting_cash INTEGER,
  cash_idr INTEGER, created_at TIMESTAMP
);

-- positions (open)
CREATE TABLE positions (
  id INTEGER PRIMARY KEY,
  portfolio_id INTEGER,
  code TEXT, quantity INTEGER, avg_cost INTEGER,
  thesis TEXT, expected_horizon_days INTEGER,
  sell_triggers TEXT,                     -- JSON
  stop_loss INTEGER, target INTEGER,
  preset_at_entry TEXT,
  opened_at TIMESTAMP
);

-- trades (entries and exits)
CREATE TABLE trades (
  id INTEGER PRIMARY KEY,
  portfolio_id INTEGER, position_id INTEGER,
  code TEXT, side TEXT, qty INTEGER, price INTEGER,
  value_idr INTEGER, reason TEXT,
  signals_snapshot TEXT,                  -- JSON
  executed_at TIMESTAMP
);

-- journal_entries
CREATE TABLE journal_entries (
  id INTEGER PRIMARY KEY,
  portfolio_id INTEGER, position_id INTEGER,
  code TEXT, body TEXT, tags TEXT,
  created_at TIMESTAMP
);

-- signal_history (every skill run, every stock, every date — the audit trail)
CREATE TABLE signal_history (
  id INTEGER PRIMARY KEY,
  code TEXT, skill_id TEXT, run_at TIMESTAMP,
  verdict TEXT, score REAL, confidence REAL,
  evidence TEXT                           -- JSON
);

CREATE INDEX idx_signal_code_skill_time ON signal_history(code, skill_id, run_at);

-- screener_runs
CREATE TABLE screener_runs (
  id INTEGER PRIMARY KEY,
  preset TEXT, universe TEXT, run_at TIMESTAMP,
  results TEXT                            -- JSON of ranked list
);
```

This schema is the source of truth for the review workflow and the calibration analysis.

---

## 9. Phased build plan

### Phase 1 — Engine spike (1–2 weeks)
- Python project setup, SQLite schema, data adapter for mock JSON
- Implement 5 skills end-to-end to validate the interface:
  - `intelligent-investor` (fundamental)
  - `bandarmology` (flow)
  - `wyckoff-methodology` (tape)
  - `most-important-thing` (macro)
  - `essays-of-warren-buffett` (fundamental)
- Composite scorer with one preset
- CLI: `screener run --preset value-compounder --universe LQ45.json`

Goal: prove the interface works and the mock JSON drives meaningful, inspectable output.

### Phase 2 — Full skill library (3–4 weeks)
- Implement remaining 16 skills
- Refine score normalization (the hardest part — making skills' scores actually comparable)
- Multiple presets
- Hard filters
- Signal history persistence

Goal: full analytical engine working from CLI; every book represented; outputs inspectable.

### Phase 3 — macOS UI (3–4 weeks)
- SwiftUI app skeleton, FastAPI client
- Screener view (table, filters, presets)
- Stock detail (tabs, evidence rendering, basic charts)
- Watchlist persistence

Goal: usable as a research tool, even without paper trading.

### Phase 4 — Paper trading (2–3 weeks)
- Portfolio + position model
- Trade lifecycle UI (buy dialog, position detail, sell dialog)
- Nightly re-evaluation of holdings
- Journal entries
- Notifications

Goal: full paper-trading loop working.

### Phase 5 — Review and calibration (1–2 weeks)
- Trade history analytics
- Skill performance dashboard
- Calibration plots (predicted score vs. realized outcome)
- Preset performance comparison

Goal: the learning loop.

### Phase 6 — Polish + real data adapter (open-ended)
- Replace mock JSON with real IDX data sources
- Intraday data integration (improves tape skills)
- Charts improved (Wyckoff overlays, broker-flow visualization)
- Export/import portfolios

---

## 10. Open design questions

These should be resolved before Phase 1 starts:

1. **Score normalization across skills.** Different skills naturally produce different score distributions. How aggressively do we calibrate? Options: leave raw and let weights handle it, or rank-normalize within each skill nightly across the universe.

2. **Skill confidence handling.** Some skills will produce low-confidence outputs (e.g., a stock with only 3 years of data running through `intelligent-investor`). Should low confidence reduce score weight in composite, or surface as caveat only?

3. **How quantitative should qualitative skills be?** `common-stocks-uncommon-profits` has 15 points, mostly qualitative. Codifying as proxies (R&D / revenue, margin trends, etc.) captures part of it but loses the scuttlebutt soul. Option: render the qualitative prompts in UI for user to score manually, persist as part of the stock's evidence.

4. **Bandar phase detection threshold.** Wyckoff phase boundaries are judgment calls. Need to choose a default ruleset (e.g., spring = price closes back above support within 3 days of breach) and let the user tune in settings.

5. **Mock data design.** The 5–10 mock stocks should be chosen to exercise edge cases — small-cap with thin float, classic compounder, cyclical at bottom, distressed turnaround, recent IPO with limited history. Without this, the engine looks like it works but breaks on real data.

---

## 11. What this spec deliberately leaves out

- ML / quant signals beyond the books
- Options, futures, derivatives
- Multi-currency / multi-market
- Real broker integration
- Mobile app (macOS-only v1)
- Collaborative features (single-user)
- Backtesting against historical data — the review workflow is forward-looking on paper trades only; full backtesting would be a separate project

These are deferred, not rejected.
