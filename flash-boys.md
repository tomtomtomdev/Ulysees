---
name: flash-boys
description: Apply Michael Lewis's Flash Boys framework — understanding how HFT and modern market structure affect execution, what predatory order flow detection looks like, and how to protect a trade from front-running and adverse selection. Use this skill whenever the user asks about HFT impact on their trades, front-running, latency arbitrage, execution quality, dark pool fairness, or how to think about modern market microstructure from an execution-fairness perspective. Trigger for phrases like "am I getting front-run", "HFT taking my edge", "execution fairness", "latency arbitrage", or any question about modern market structure's effect on the individual trader's execution.
---

# Flash Boys — Lewis Framework

Lewis's narrative (built around Brad Katsuyama and IEX) makes a specific claim: the modern market structure is rigged in favor of speed advantages held by HFT firms, and unsophisticated participants pay for that advantage in execution costs they don't see. Apply the framework as a lens on execution fairness and trade protection.

## Step 1: Identify the structural problem

The Flash Boys thesis in brief:
- HFT firms colocate servers at exchange data centers, achieving microsecond latency advantages
- They subscribe to direct exchange feeds (faster than the consolidated SIP feed)
- When a large order arrives at one exchange, HFTs detect it and race to the other exchanges to trade ahead
- The original order arrives at the other venues to find prices already moved
- The cost is paid by the original order (worse fill prices), captured as HFT profit

Whether you accept the full framing or not, the mechanics described are real. The question is the practical effect on your trades.

## Step 2: When does this matter

It matters most when:
- You are sending orders larger than displayed depth at any single venue
- You are using market orders or aggressive limit orders that cross the spread
- You are trading in fragmented, fast names where HFTs are active
- Your broker routes for rebates rather than execution quality

It matters less when:
- You are trading small size (less than visible depth at the touch)
- You are using patient limit orders that don't reveal intent
- You are an individual investor with small notional and long holding periods
- The name is illiquid enough that HFTs aren't structurally engaged

Be honest about which case applies before assigning blame for poor execution.

## Step 3: Recognize the symptoms of being picked off

Patterns suggestive of HFT detection of your order flow:
- **Phantom liquidity** — depth disappears the instant before your order arrives
- **Reach-through** — you see size at a price and try to take it; it's gone, price has moved up a tick
- **Persistent slippage on patterns** — if you trade the same setup repeatedly and slippage is systematic, your pattern may be detected
- **Cancel rates around your activity** — high cancel rates near your price suggest active participants are testing your intent
- **Worse fills than the displayed book suggested** — quoted spread of 1 cent but realized cost of 3+ cents

These are not proof of HFT predation — fragmented markets just behave this way — but they're symptoms worth diagnosing.

## Step 4: Defenses available

The book's heroes built IEX with structural defenses (the "speed bump"). Practical defenses available to most traders:

**For institutions**
- Smart order routers with anti-gaming logic
- Use of dark pools with reputational quality (and aware of their owners' conflicts)
- IEX or other speed-bumped venues
- Algos designed to minimize signaling (randomization, conditional placement)

**For active retail traders**
- Use limit orders, not market orders
- Avoid the open and close auctions for large fills unless using the auction mechanisms intentionally
- Trade liquid names where HFT activity narrows spreads more than it costs in adverse selection
- Be aware of your broker's routing — payment for order flow brokers route to internalizers, which has both costs and benefits

**For long-term investors**
- The framework barely matters at multi-year holding periods; basis-point execution costs are noise
- Don't optimize what doesn't matter

## Step 5: Don't overweight the narrative

Lewis's framing is powerful storytelling but has limits:
- HFT compresses spreads, which benefits most retail and institutional orders
- The "rigged" framing is contested; many academic studies find mixed effects
- Internalizers offering price improvement to retail are not pure villains; the price-improvement statistics matter
- Some of the most aggressive practices described in 2014 have been curtailed by regulation and venue innovation

Use the framework as a sensitivity, not a worldview.

## Step 6: Execution analysis for a specific trade

For a trade in question, ask:

- **Size vs. liquidity** — what fraction of displayed depth and ADV does the order represent?
- **Order type** — market, marketable limit, passive limit?
- **Urgency** — must execute now, or can work patiently?
- **Venue control** — does your broker let you direct routing, or is it black-box?
- **Information leakage** — is this order part of a recognizable pattern?

The combination determines whether HFT-driven costs are likely material.

## Step 7: When to use this framework

This is an execution-quality lens. Use it when:
- The user reports unexpectedly bad fills
- The user is sizing up to institutional-relevant volumes
- The user is asking about broker quality or routing
- The user wants to understand why intraday price action looks the way it does

Do not use it when:
- The user is asking about fundamental investment decisions
- The trade is small enough that execution costs are immaterial
- The holding period is long enough that basis points don't matter

## Output format

1. **Relevance check** — does HFT-style execution cost actually matter for this trade?
2. **Symptom diagnosis** — if execution has been poor, what patterns suggest the cause.
3. **Defenses applicable** — concrete steps the user can take (order types, venues, broker choice).
4. **What's overblown vs. real** — honest framing of where the narrative oversells.
5. **Specific recommendation** — for the situation described.

## What to avoid

- Don't blame HFT for every bad fill. Most slippage has more boring explanations.
- Don't use this framework for investment decisions. It's about execution, not value.
- Don't recommend complex defenses to retail investors trading small size. The costs they care about are commissions, taxes, and bid-ask spread — not microsecond races.
- Don't ignore the framework when it does apply. Mid-cap institutional orders genuinely face this; pretending otherwise is unhelpful.
- Don't pretend the narrative is undisputed. There's a real academic debate about HFT's net effect.
