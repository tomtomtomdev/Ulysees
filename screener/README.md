# IDX Formula Screener

Codifies the 21 book-skills from `idx-screener-spec.md` as deterministic formula presets that operate over Stockbit's "Add Financial Metric" catalog (~250 metrics harvested from the screenshot set).

## Layout

```
screener/
├── metrics.json              # Catalog of every Stockbit metric (keys + UI labels + unit)
├── screener.py               # Formula engine + CLI
├── presets/                  # Book-skill formulas (one JSON each)
│   ├── intelligent-investor.json
│   ├── magic-formula.json
│   ├── buffett-compounder.json
│   ├── lynch-fastgrower.json
│   ├── piotroski-f.json
│   ├── klarman-deep-value.json
│   ├── bandarmology.json
│   ├── bandar-investment-style.json
│   ├── trading-bandarmology.json
│   ├── wyckoff-accum.json
│   ├── wyckoff-distribution.json
│   ├── vpa-strength.json
│   ├── livermore-pivot.json
│   ├── marks-cycle.json
│   ├── fisher-15-points.json
│   ├── dividend-aristocrat.json
│   ├── special-situation.json
│   ├── canslim.json
│   ├── charlie-munger-inversion.json
│   └── composite-value-bandar.json
└── mock/universe.json        # 6 hand-built names across diverse profiles
```

## Usage

```bash
python3 screener.py --list-presets
python3 screener.py --preset magic-formula
python3 screener.py --preset composite-value-bandar --top 10
python3 screener.py --preset bandarmology --json
```

## Formula format

Each preset is a JSON file with rules:

```json
{
  "name": "graham-margin",
  "expr": "graham_multiplier is not None and price <= graham_multiplier * 0.67",
  "weight": 1.5,
  "veto": false,
  "note": "≥33% MoS to Graham number"
}
```

- Expressions are evaluated in a sandbox containing all metric keys for the stock plus helpers (`has`, `pct_below`, `pct_above`, `min`, `max`, `abs`, `isfinite`).
- Missing metric → rule fails gracefully (recorded in `errors`).
- `veto: true` rules block the candidate entirely when they fail.
- Composite score = Σ(weight of passing rules) / Σ(all weights).

## Adding a new preset

1. Drop a JSON file into `presets/`.
2. Reference metric keys from `metrics.json`.
3. Run `python3 screener.py --preset <id>`.
