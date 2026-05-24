---
name: bandarmology
description: Apply Ryan Filbert's Bandarmology framework to analyze a stock by tracking the footprints of large players ("bandar") — broker accumulation patterns, volume spikes, foreign vs. domestic flows, and price-action confirmation. Use this skill whenever the user mentions bandarmology, bandar, big-player flow, broker summary analysis, accumulation/distribution by major brokers, or wants to know whether smart money is accumulating or distributing a stock — especially on Indonesian or other Southeast Asian exchanges where broker-level transaction data is available. Trigger for phrases like "is the bandar buying", "broker summary", "who's accumulating", or any question demanding broker-flow analysis.
---

# Bandarmology — Filbert Framework

Bandarmology is the practice of tracking large-player ("bandar") activity through broker summary and transaction data. Strongest on exchanges that publish broker-level data (IDX, KLSE, SET, HKEX-style); useful as a complementary lens elsewhere via volume and tape reading.

The thesis: large operators leave footprints — concentrated accumulation by specific brokers, unusual volume against quiet price, distribution disguised as strength — and detecting these footprints early gives a window before the move.

## Step 1: Define the question

Bandarmology answers a specific question: **is a large player accumulating, distributing, or absent?** It does not answer whether the company is undervalued. Combine with fundamental analysis for a complete view, but here, focus on flow.

## Step 2: Broker summary analysis

The core tool. For the stock and time window in question, examine:

- **Net buy by broker** — which broker codes have largest net buy and net sell over the period?
- **Concentration** — is buying concentrated in a small number of brokers, or distributed across many?
- **Same-broker persistence** — does the same broker appear as top net buyer day after day?
- **Average buying price vs. average selling price by broker** — top accumulating brokers buying at lower prices is the classic accumulation pattern.
- **Foreign vs. domestic flow** — foreign brokers (often institutional) net flow vs. local retail-heavy brokers.
- **Block transactions** — large negotiated trades and which brokers facilitated them.

Concentrated, persistent net buying by a small set of brokers at average prices near or below current price is the bandar accumulation signature.

## Step 3: Volume and price action

Broker data is more meaningful when read alongside volume and price:

- **Quiet accumulation** — rising or steady price on heavy volume, but no breakout (the bandar buying without revealing the hand).
- **Volume spike without follow-through** — possibly distribution disguised as enthusiasm.
- **Breakout with broker-concentration confirmation** — the most actionable pattern: accumulation finishes, breakout begins, the same accumulating brokers continue buying.
- **Shakeout patterns** — sharp drop on lower volume than the prior accumulation, designed to flush retail; broker data should show top accumulators still net buyers.

## Step 4: Wyckoff overlay (compatible)

Bandarmology's price logic maps cleanly onto Wyckoff's accumulation/distribution phases:

- **Accumulation (Phase A–E)**: selling climax, automatic rally, secondary test, spring, sign of strength, last point of support. Broker data should show top accumulators buying through these phases.
- **Markup**: price advances on continued broker concentration.
- **Distribution (Phase A–E)**: buying climax, automatic reaction, upthrust, sign of weakness, last point of supply. Broker data should show prior accumulators flipping to net sellers, often disguised through multiple broker accounts.
- **Markdown**: price falls; broker concentration may show short-side activity or absence.

Identify the likely phase and the broker-flow evidence supporting that phase.

## Step 5: Confirmation checks

Before concluding accumulation:

- **Time horizon** — broker accumulation typically runs weeks to months. Single-day net buying is noise.
- **Float adjustment** — accumulated shares vs. tradable float; large bandar interest is meaningful only against float.
- **Retail sentiment** — strong bandar accumulation often runs against retail apathy or fear. If retail is also enthusiastic, the bandar may already be distributing.
- **News absence** — quietest accumulation often happens before news, not after.

## Step 6: Risks and what bandarmology cannot tell you

- Concentrated broker activity can be a single large client hedging, not directional positioning.
- Algos and ETFs create broker-level flow that looks like accumulation but isn't directional.
- Bandar pattern recognition is more art than science, especially without long-term data history.
- A real bandar move can reverse if the underlying business deteriorates; bandar buying does not override fundamentals.
- Some "bandar signatures" are after-the-fact pattern matching. Be honest about base rates.

## Step 7: Trade construction

If accumulation is identified:
- **Entry zone** — near the average accumulation price of top broker buyers.
- **Stop** — below the accumulation range; a clean break below suggests the move failed.
- **Target** — depends on accumulated volume and prior resistance; many bandarmology practitioners size targets to 1.5–3× the accumulation range height.
- **Position size** — the more confident the pattern and the broader the broker concentration, the larger; never bet the farm on a single broker-flow read.

## Output format

1. **Verdict** — accumulation / distribution / sideways / unclear.
2. **Phase** — Wyckoff phase if identifiable.
3. **Broker concentration table** — top net buyers and sellers, with persistence and avg price notes.
4. **Volume/price reading** — what the tape says alongside the broker data.
5. **Confirmation checks** — time horizon, float, retail sentiment, news context.
6. **What could invalidate this** — clean failure conditions.
7. **Trade construction** — if actionable: entry zone, stop, target, sizing approach.

## What to avoid

- Don't read one day's broker summary as a trend. Bandar moves play out over weeks.
- Don't ignore fundamentals. Bandarmology is a flow lens, not a complete analysis.
- Don't trust pattern matching without checking base rates; confirmation bias is heavy in this style.
- Don't assume the bandar is always right. Operators get caught and forced out too.
- Don't apply this framework without broker-level data; it degrades to ordinary volume analysis without it.
