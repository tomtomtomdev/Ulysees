"""IDX Formula Screener — evaluates Stockbit-style metric expressions over a stock universe.

A formula is a list of rules. Each rule has:
    - name: short label
    - expr: a Python expression using metric keys (see metrics.json)
    - weight: contribution to the composite when the rule passes (default 1.0)
    - veto:  if true, a failure blocks the candidate regardless of score

The expression namespace includes:
    - all metric keys for the stock being evaluated (None if missing)
    - helpers: abs, min, max, isfinite, has(key), pct_below(a,b), pct_above(a,b)

Run:
    python screener.py --preset value-compounder
    python screener.py --formula my_rules.json
"""

from __future__ import annotations

import argparse
import json
import math
import operator
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

HERE = Path(__file__).parent


# ---------- Safe expression evaluator ----------

_ALLOWED_BUILTINS = {
    "abs": abs, "min": min, "max": max, "round": round,
    "len": len, "sum": sum, "all": all, "any": any,
    "True": True, "False": False, "None": None,
}


def _make_env(metrics: dict[str, Any]) -> dict[str, Any]:
    def has(key: str) -> bool:
        return metrics.get(key) is not None

    def pct_below(a, b):
        if a is None or b is None or b == 0:
            return None
        return (b - a) / b * 100

    def pct_above(a, b):
        if a is None or b is None or b == 0:
            return None
        return (a - b) / b * 100

    env = dict(_ALLOWED_BUILTINS)
    env["isfinite"] = lambda x: x is not None and isinstance(x, (int, float)) and math.isfinite(x)
    env["has"] = has
    env["pct_below"] = pct_below
    env["pct_above"] = pct_above
    env.update(metrics)
    return env


def evaluate(expr: str, metrics: dict[str, Any]) -> tuple[Any, str | None]:
    """Evaluate expr against the stock's metrics. Returns (value, error_or_None)."""
    env = _make_env(metrics)
    try:
        return eval(expr, {"__builtins__": {}}, env), None  # noqa: S307 — sandboxed
    except TypeError:
        return None, "missing-data"
    except ZeroDivisionError:
        return None, "division-by-zero"
    except NameError as e:
        return None, f"unknown-metric:{e}"
    except Exception as e:  # noqa: BLE001
        return None, f"error:{type(e).__name__}:{e}"


# ---------- Rules and presets ----------

@dataclass
class Rule:
    name: str
    expr: str
    weight: float = 1.0
    veto: bool = False
    note: str = ""

    @classmethod
    def from_dict(cls, d: dict) -> "Rule":
        return cls(
            name=d["name"],
            expr=d["expr"],
            weight=float(d.get("weight", 1.0)),
            veto=bool(d.get("veto", False)),
            note=d.get("note", ""),
        )


@dataclass
class Preset:
    id: str
    name: str
    description: str
    rules: list[Rule]

    @classmethod
    def from_dict(cls, d: dict) -> "Preset":
        return cls(
            id=d["id"],
            name=d["name"],
            description=d.get("description", ""),
            rules=[Rule.from_dict(r) for r in d["rules"]],
        )


# ---------- Screener runner ----------

@dataclass
class StockResult:
    code: str
    name: str
    score: float
    max_score: float
    pct: float
    passed: list[str]
    failed: list[str]
    vetoed_by: list[str]
    errors: dict[str, str] = field(default_factory=dict)

    @property
    def blocked(self) -> bool:
        return bool(self.vetoed_by)


def run_preset(preset: Preset, universe: list[dict]) -> list[StockResult]:
    results: list[StockResult] = []
    for stock in universe:
        metrics = stock.get("metrics", {})
        passed, failed, vetoed, errors = [], [], [], {}
        score, max_score = 0.0, 0.0
        for rule in preset.rules:
            max_score += rule.weight
            value, err = evaluate(rule.expr, metrics)
            if err is not None:
                errors[rule.name] = err
                failed.append(rule.name)
                continue
            if bool(value):
                passed.append(rule.name)
                score += rule.weight
            else:
                failed.append(rule.name)
                if rule.veto:
                    vetoed.append(rule.name)
        results.append(StockResult(
            code=stock["code"],
            name=stock.get("name", stock["code"]),
            score=round(score, 2),
            max_score=round(max_score, 2),
            pct=round(100 * score / max_score, 1) if max_score else 0.0,
            passed=passed,
            failed=failed,
            vetoed_by=vetoed,
            errors=errors,
        ))
    results.sort(key=lambda r: (r.blocked, -r.pct))
    return results


# ---------- IO ----------

def load_presets() -> dict[str, Preset]:
    presets_dir = HERE / "presets"
    out: dict[str, Preset] = {}
    for path in sorted(presets_dir.glob("*.json")):
        data = json.loads(path.read_text())
        preset = Preset.from_dict(data)
        out[preset.id] = preset
    return out


def load_universe(path: Path) -> list[dict]:
    return json.loads(path.read_text())["stocks"]


def print_results(preset: Preset, results: list[StockResult], top: int = 20) -> None:
    print(f"\n=== Preset: {preset.name} ({preset.id}) ===")
    print(preset.description)
    print()
    print(f"{'Rank':>4}  {'Code':<6}  {'Name':<28}  {'Score':>10}  {'Pass/Total':>11}  Status")
    print("-" * 90)
    for i, r in enumerate(results[:top], 1):
        status = f"BLOCKED ({', '.join(r.vetoed_by)})" if r.blocked else ""
        print(
            f"{i:>4}  {r.code:<6}  {r.name[:28]:<28}  "
            f"{r.pct:>9.1f}%  {len(r.passed):>4}/{len(r.passed)+len(r.failed):<6}  {status}"
        )
    if results:
        print()
        top1 = results[0]
        print(f"Top: {top1.code} — passed: {', '.join(top1.passed) or '(none)'}")
        if top1.failed:
            print(f"     failed: {', '.join(top1.failed)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="IDX formula screener over Stockbit-style metrics.")
    parser.add_argument("--preset", help="Preset id (see presets/)")
    parser.add_argument("--list-presets", action="store_true")
    parser.add_argument("--universe", default=str(HERE / "mock" / "universe.json"))
    parser.add_argument("--top", type=int, default=20)
    parser.add_argument("--json", action="store_true", help="Emit JSON results")
    args = parser.parse_args()

    presets = load_presets()
    if args.list_presets or not args.preset:
        for p in presets.values():
            print(f"  {p.id:<28}  {p.name}")
        if not args.preset:
            return

    if args.preset not in presets:
        raise SystemExit(f"Unknown preset: {args.preset}")
    preset = presets[args.preset]
    universe = load_universe(Path(args.universe))
    results = run_preset(preset, universe)

    if args.json:
        print(json.dumps([r.__dict__ for r in results], indent=2))
    else:
        print_results(preset, results, top=args.top)


if __name__ == "__main__":
    main()
