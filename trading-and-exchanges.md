---
name: trading-and-exchanges
description: Apply Larry Harris's Trading and Exchanges framework to analyze a stock or market situation through market microstructure — understanding who the players are (informed traders, liquidity traders, market makers, parasitic traders), how their interactions shape prices, and what the order book and trading activity reveal. Use this skill whenever the user asks about market microstructure, order types, liquidity, market impact, why a stock moves the way it does, or how to think about a trading situation structurally. Trigger for phrases like "who's trading this", "why did it move on no news", "market impact", "liquidity", or any microstructure question.
---

# Trading and Exchanges — Harris Framework

Harris's framework: understand any trading situation by identifying the players, their motives, and how the market mechanism aggregates their orders into prices. Most surface phenomena (price moves, volume patterns, spreads) are explainable once the player taxonomy is clear.

## Step 1: Identify the trader taxonomy

For the situation in question, identify who is plausibly active and why:

**Informed traders**
- Have private information or superior analysis
- Buy when they think price is below value, sell when above
- Trade size limited by market impact — they hide
- Their footprint: persistent one-sided pressure that moves price toward value

**Value-motivated investors**
- Long-term fundamental investors (Graham, Buffett style)
- Trade infrequently, less concerned with execution price within reason
- Their footprint: large blocks, often facilitated through dealers or dark pools

**Liquidity traders**
- Trade to meet cash needs, rebalance, dollar-cost-average
- Not informed; do not want to move price
- Their footprint: predictable patterns (month-end, index rebalance, paycheck cycles)

**Market makers and dealers**
- Provide liquidity, profit from spread
- Quote bid and offer; trade against incoming orders
- Their footprint: tight spreads in liquid stocks, wider in illiquid

**Parasitic traders**
- Profit by trading ahead of or against other traders
- Front-runners, quote matchers, certain HFT strategies, manipulators
- Their footprint: behavior tightly correlated with detectable order flow patterns

**Pseudo-informed traders**
- Believe they have an edge but don't (most retail and many professionals)
- Provide liquidity to informed traders without knowing it

State which players are most likely active in this situation and why.

## Step 2: Read the order book and tape

Microstructure analysis works from observable evidence:

- **Bid-ask spread** — tight spread implies competitive market making and active informed traders; wide spread implies illiquid name or perceived informational asymmetry.
- **Depth at the top of book** — how much size at best bid and offer; thin depth = small trades move price.
- **Order book imbalance** — heavier on one side suggests directional pressure (but can be misleading if iceberg orders are hidden).
- **Trade prints** — sequence of executions, at bid vs. at offer, lot sizes. Aggressive buying (executions at offer) vs. aggressive selling (executions at bid).
- **Block trades** — large facilitated trades, usually between informed/value players and dealers. Off-exchange prints indicate institutional involvement.

## Step 3: Liquidity vs. information

A central Harris distinction: price moves either because new information arrived or because someone needed liquidity. Diagnose:

- **Information-driven move** — price changes, spread temporarily widens, then narrows at a new equilibrium. Volume sustained at new level.
- **Liquidity-driven move** — price moves on heavy one-side pressure with no news, then mean-reverts as opportunistic liquidity providers step in.

This distinction matters: a liquidity-driven dislocation is an opportunity; an information-driven move is the market doing its job.

## Step 4: Market impact and execution

For any non-trivial trade:

- **Bid-ask spread cost** — pay half-spread to be aggressive
- **Market impact cost** — moving the price against yourself by taking liquidity
- **Opportunity cost** — letting the order rest and missing the move
- **Permanent vs. temporary impact** — informed buying creates permanent impact; uninformed buying creates mostly temporary impact

Address how the size being traded interacts with available liquidity. A 100-share order in Apple is invisible; the same order in a microcap is the market.

## Step 5: Volatility and what it reveals

Different volatility regimes have different microstructure causes:
- **Information volatility** — earnings, news, surprise events
- **Liquidity volatility** — gaps caused by withdrawal of market makers in stress
- **Microstructure noise** — high-frequency oscillation between bid and offer
- **Persistent volatility** — disagreement between informed traders

State which regime the situation appears to be in.

## Step 6: Asymmetric information and adverse selection

Market makers protect themselves against trading with informed traders by widening spreads. Adverse selection insight:
- If you're consistently filled instantly at your price, you're the uninformed counterparty
- If you have to chase the price to get filled, you may be the informed one and impact reflects that
- Persistent fade after your fills suggests parasitic traders are detecting your flow

## Step 7: Mechanism and venue considerations

Where and how to trade affects outcome:
- **Lit exchanges** — full pre-trade transparency, but signals your intent
- **Dark pools** — no pre-trade transparency, less impact, but execution uncertain
- **Block desks** — for large size, accept information leakage for executed size
- **Order types** — market vs. limit, hidden vs. displayed, time-in-force; each has a tradeoff between price and certainty

## Output format

1. **Player taxonomy** — who's likely active in this situation and why.
2. **Order book and tape read** — spread, depth, imbalance, recent prints.
3. **Information vs. liquidity diagnosis** — what's driving the current move.
4. **Market impact estimate** — for the trade size considered.
5. **Execution recommendation** — venue, order type, urgency tradeoffs.
6. **Microstructure risks** — adverse selection, parasitic flow, regime shifts.
7. **What the structure can't tell you** — the limits of microstructure analysis.

## What to avoid

- Don't read pure microstructure signals as fundamental signals. Liquidity-driven moves mean-revert; that's the point.
- Don't ignore parasitic flow. If you have a pattern, someone is detecting it.
- Don't trade size in illiquid names without modeling market impact. The price you see is not the price you'll get.
- Don't confuse displayed depth with available liquidity. Iceberg and reserve orders hide size.
- Don't use this framework alone for investment decisions. It's a complement to fundamental analysis, not a substitute.
