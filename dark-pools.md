---
name: dark-pools
description: Apply Scott Patterson's Dark Pools framework — analyzing how the modern fragmented, algorithmically-driven market structure (dark pools, HFT, order routing, market fragmentation) affects a stock or trade, and what hidden institutional activity may be inferred from observable signals. Use this skill whenever the user asks about dark pool activity, HFT impact, order fragmentation, hidden institutional flow, or how modern market structure might be affecting price action they observe. Trigger for phrases like "dark pool prints", "HFT", "is institutions buying", "fragmented liquidity", or any modern-microstructure question.
---

# Dark Pools — Patterson Framework

Patterson's narrative reveals how modern markets fragment trade across lit exchanges and dark venues, with HFT firms intermediating between them. Apply the framework as a structural lens: when looking at a stock, what does the modern market structure mean for what you see and don't see?

## Step 1: Understand the venues

Modern equity trading happens across dozens of venues. Categorize:

**Lit exchanges**
- NYSE, NASDAQ, others
- Pre-trade transparency (visible order book)
- Post-trade transparency (immediate reporting)
- Where most price discovery occurs

**Dark pools**
- Operated by broker-dealers (Goldman Sigma X, Credit Suisse Crossfinder, etc.) or independents
- No pre-trade transparency
- Post-trade reporting to consolidated tape, sometimes delayed
- Designed for institutional block execution with minimal market impact

**Internalizers / wholesalers**
- Citadel, Virtu, others
- Retail order flow routed here for "price improvement"
- Operator profits from spread and informational advantage
- Often the destination for retail brokerage orders ("payment for order flow")

**ATSs and other venues**
- Various alternative trading systems
- Each with specific matching rules, fee/rebate structures, participant restrictions

## Step 2: What's visible vs. hidden

The displayed order book on a lit exchange is a fraction of the real picture:

- **Iceberg / reserve orders** — displayed quantity is smaller than actual; large orders are sliced
- **Dark pool resting orders** — invisible until matched
- **Algos working orders** — VWAP, TWAP, implementation shortfall algorithms placing small slices across venues over time
- **Conditional orders** — sit dormant until a contra-side appears; never display

The takeaway: the order book is an indication, not a true measure of liquidity.

## Step 3: Reading dark prints

Trades executed in dark pools print to the consolidated tape, usually with a venue identifier or "off-exchange" flag (often called "TRF" — trade reporting facility):

- **Off-exchange volume share** — for many large-caps, 35–50% of volume is off-exchange. Useful to track in absolute and relative terms.
- **Block prints** — single large prints reported off-exchange suggest institutional crossing. Track size relative to ADV.
- **Print clusters** — multiple large dark prints in a short window indicate concentrated institutional activity.
- **Price relative to lit market** — dark prints near the midpoint suggest neutral institutional crossing; near the bid or offer suggests directional pressure.

These signals are noisy but useful in aggregate, especially when concentrated.

## Step 4: HFT activity and its effects

Patterson's book is partly about HFT's role. Practical effects to consider:

- **Spread compression** — HFTs provide tight quotes in liquid names; spreads have narrowed dramatically since their rise
- **Depth illusion** — quoted depth can disappear instantly when meaningful flow arrives; HFTs cancel quotes faster than humans can react
- **Adverse selection** — HFTs detect order flow patterns and trade ahead; institutional orders that aren't carefully sliced get picked off
- **Latency arbitrage** — HFTs profit from microsecond-level differences between venues; mostly irrelevant to investors but explains some intraday phenomena
- **Quote stuffing and other manipulative patterns** — alleged in the book and elsewhere; relevant to understanding flash crashes and weird intraday action

## Step 5: Routing and execution implications

For any non-trivial trade:

- **Where does your broker route?** Different brokers have different routing logic; many route retail orders to internalizers for payment for order flow
- **What execution quality are you getting?** Price improvement statistics vary widely; the "free" trading model has costs in execution
- **For institutions** — algo selection, venue access, smart order routing all affect realized execution cost
- **Information leakage** — large orders worked over time leak intent; minimizing leakage is a major institutional concern

## Step 6: Inferring institutional intent

Despite fragmentation, footprints exist. Look for:

- **Sustained off-exchange volume share above norm** — institutions are active
- **Block prints at specific prices** — informed crossing levels
- **Price action that absorbs visible offers without retracing** — hidden buying eating through displayed depth
- **Unusual quote behavior** — order book repeatedly refilling on the bid with no price movement = sustained absorption of supply
- **Closing auction imbalances** — large closing-auction orders are often institutional rebalancing or end-of-day positioning

These signals are tendencies, not certainties. Use as a complementary lens.

## Step 7: Risks the structure creates

Patterson's underlying critique: the structure introduces fragilities:

- **Flash crashes** — automated liquidity withdrawal under stress
- **Adverse selection for the uninformed** — retail order flow systematically routed to interested counterparties
- **Two-tier market** — speed-and-data haves vs. have-nots
- **Conflicts of interest** — broker-dealers operating dark pools while also executing customer flow

For investors, these risks rarely affect long-term outcomes but matter for execution and short-term phenomena.

## Step 8: What the framework cannot tell you

- Specific identity of institutional buyers/sellers is rarely knowable in real time
- Whether a block print is initiating a position or unwinding one is often ambiguous
- HFT-driven price action often reverses; reading it as fundamental signal is a mistake
- The structure is dynamic — venues change, rules evolve, dominant players shift

## Output format

1. **Structure snapshot** — off-exchange share, block print activity, venue notes if available.
2. **Lit book read** — what's displayed, what's likely hidden, spread and depth context.
3. **Inferred institutional activity** — directional, neutral crossing, absorption, or quiet.
4. **HFT and microstructure caveats** — what might be noise vs. signal.
5. **Execution implications** — for trade sizes relevant to this user.
6. **Risks and limits** — what this lens does and doesn't show.

## What to avoid

- Don't treat dark prints as proof of institutional buying or selling. They're tendencies.
- Don't ignore HFT effects on intraday price action — much of it isn't signal.
- Don't use this framework alone for investment decisions. It's about market structure, not value.
- Don't trust displayed depth in liquid names. It can vanish in milliseconds.
- Don't assume your retail broker is routing for your best execution. It probably isn't.
