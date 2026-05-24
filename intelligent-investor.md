---
name: intelligent-investor
description: Apply Benjamin Graham's framework from The Intelligent Investor to analyze a stock or investment situation. Use this skill whenever the user asks for a value analysis, mentions Graham, defensive/enterprising investor screens, margin of safety, Mr. Market, intrinsic value vs price, or wants a disciplined valuation of a publicly traded company. Trigger even when the user just says "is this stock cheap" or "should I buy this" — Graham's lens is the default starting point for fundamental value work.
---

# The Intelligent Investor — Analysis Framework

Apply Graham's framework to evaluate whether a stock or situation is a sound investment vs. a speculation.

## Step 1: Investor type

Decide which lens applies before analyzing:
- **Defensive investor** — wants safety and freedom from effort. Apply the seven defensive criteria below strictly.
- **Enterprising investor** — willing to do work for above-average results. Looser criteria, but demand bargain prices.

Ask the user which they are if it's not obvious. Defensive is the right default.

## Step 2: Defensive investor's seven criteria

Run each criterion. Note pass/fail and the actual value.

1. **Adequate size** — not a small company. Modern equivalent: market cap > ~$2B, or annual revenue > $500M.
2. **Strong financial condition** — current assets ≥ 2× current liabilities; long-term debt < net current assets (or for industrials, debt/equity < 1).
3. **Earnings stability** — positive earnings in each of the last 10 years.
4. **Dividend record** — uninterrupted dividends for at least 20 years. (Modern relaxation: 10+ years acceptable for tech-era companies.)
5. **Earnings growth** — EPS up at least one-third over the last 10 years (using 3-year averages at start and end).
6. **Moderate P/E** — current price ≤ 15× average earnings of the past 3 years.
7. **Moderate P/B** — price ≤ 1.5× book value. **Combined test**: P/E × P/B ≤ 22.5.

## Step 3: Enterprising investor's looser screen

If defensive criteria are too strict for the situation, fall back to:
- Current assets ≥ 1.5× current liabilities; debt ≤ 110% of net current assets
- Earnings stable (no deficits in last 5 years)
- Some current dividend
- Last year's earnings higher than 5 years ago
- Price < 120% of net tangible assets

## Step 4: Intrinsic value estimate

Use Graham's formula as a sanity check, not gospel:

**V = EPS × (8.5 + 2g)** where g = expected annual growth rate over next 7–10 years.

Refined version with bond yield adjustment:
**V = [EPS × (8.5 + 2g) × 4.4] / Y** where Y = current AAA corporate bond yield.

Compare V to current price. If V > price by a meaningful margin, there's a margin of safety.

## Step 5: Margin of safety

State the margin of safety explicitly: `(Intrinsic value − Price) / Intrinsic value`. Graham wanted at least 33%, ideally closer to 50%. Below 25% is not a Graham buy.

## Step 6: Mr. Market check

Briefly note where the stock sits in the market's mood cycle. Is the price being offered by an optimistic or depressed Mr. Market? Graham's point: use the quote, don't be ruled by it.

## Output format

Structure the analysis as:

1. **Verdict** — one line: Sound investment / Speculation / Borderline, with the key reason.
2. **Defensive criteria scorecard** — table of 7 criteria, pass/fail, actual values.
3. **Intrinsic value range** — Graham formula output, plus a more conservative number.
4. **Margin of safety** — percentage.
5. **Risks and what would change the verdict** — 2–4 bullets.
6. **Graham would say** — short paragraph in the spirit of the book.

## What to avoid

- Don't pretend precision Graham himself rejected. Intrinsic value is a range, not a point.
- Don't ignore failed criteria with hand-waving. A defensive investor needs all seven; an enterprising one needs the looser set genuinely met.
- Don't recommend speculative growth stocks under a Graham banner. If the company fails on earnings stability or trades at growth multiples, say so plainly.
