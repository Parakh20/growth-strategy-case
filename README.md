# Growth Strategy Case Study
### User Acquisition Funnel & Channel Strategy — Career GPS

---

## Honesty Note on Data

Career GPS is a real, deployed hackathon project, but it has **no production analytics instrumentation** (no Vercel Analytics, Mixpanel, or event tracking wired up at hackathon stage). Every funnel number below is a **labeled estimate** built from plausible hackathon-stage traffic patterns, not measured production data. Section 6 specifies exactly what instrumentation to add to replace these estimates with real numbers.

---

## 1. Funnel Definition

| Stage | Users (estimated) | Conversion from prev. | Absolute drop | Cumulative conversion |
|---|---|---|---|---|
| Awareness (landing page visit) | 1,000 | 100.0% | — | 100.0% |
| Acquisition (plan generation started) | 420 | 42.0% | 580 | 42.0% |
| Activation (plan fully generated) | 380 | 90.5% | 40 | 38.0% |
| Retention (returned within 7 days) | 95 | 25.0% | 285 | 9.5% |
| Revenue (hypothetical Pro conversion) | 19 | 20.0% | 76 | 1.9% |
| Referral (shared their plan) | 12 | 63.2% | 7 | 1.2% |

---

## 2. The Naive Bottleneck Read (and why it's incomplete)

The naive read of this table says: **Acquisition is the bottleneck** — it has the largest absolute drop (580 users, a 58% loss from Awareness). This is the number most growth analyses would headline.

**That read is incomplete, and here's the actual finding this analysis surfaces:**

---

## 3. The Real Finding: Equal Proportional Impact Across Stages

I modeled the revenue impact of a **+10% conversion-rate improvement** at each stage of the funnel (holding all other stages fixed), propagating the effect forward to the Revenue stage:

| Stage improved by +10% | Additional Pro conversions/month | Additional MRR |
|---|---|---|
| Acquisition | +1.90 | +$13.30 |
| Activation | +1.90 | +$13.30 |
| Retention | +1.90 | +$13.30 |
| Revenue (direct) | +1.90 | +$13.30 |

**Every stage produces the identical dollar impact from an identical proportional improvement.** This is not a coincidence or a modeling error — it is a mathematical property of any purely multiplicative funnel: final output = initial_users × (rate₁ × rate₂ × rate₃ × ... × rateₙ). A 10% increase in any single rateᵢ increases the whole product by exactly 10%, regardless of which stage it came from.

**This directly contradicts the naive "biggest drop = most important stage" intuition**, and it's the single most useful thing this analysis produces: **the stage with the biggest raw percentage drop is not automatically the highest-leverage stage to fix.** In a multiplicative funnel, what actually differentiates stages isn't potential impact — every stage has the same potential impact per percentage point — it's **the cost and difficulty of achieving that percentage-point improvement.**

**The correct prioritization question is therefore: which stage is cheapest to move by 10%, not which stage has the biggest drop.** For Career GPS specifically:
- Improving **Activation** (90.5% → higher) is likely cheapest: it's already a high-conversion stage, meaning the remaining drop is probably a handful of specific, fixable UX bugs (recall: this exact stage had the *known, directly-observed* empty-output-section bugs identified in the Feature Prioritization case — fixing F01/F02/F03 plausibly moves this exact number)
- Improving **Retention** (25%) is likely the most expensive to move meaningfully, since it requires building an actual reason to return (notifications, new content, follow-up value) rather than fixing a bug
- Improving **Acquisition** (42%) sits in between — likely requires landing-page/positioning work, moderate effort

**Recommendation: fix Activation first.** Not because it has the biggest funnel drop (it doesn't — Acquisition and Retention both drop more in absolute terms), but because the known, already-diagnosed bugs there (from the Feature Prioritization case study) make it the cheapest 10% to capture, and the dollar value of that 10% is identical to any other stage.

---

## 4. Channel Strategy Model (12-Month Projection)

### Channel 1 — Referral/Viral

Modeled as a **single-generation invite-decay loop**: each month, a fixed external seed of new users (20/month, assumed to arrive via other channels) enters the loop; each cohort of new users generates a wave of referred users at rate K, and *that* wave generates a further wave at rate K², and so on — decaying geometrically for K<1, rather than compounding the entire cumulative user base forever (a modeling mistake that produces unrealistic unbounded growth even for sub-critical K values).

| K-factor | Month 1 (cumulative) | Month 12 (cumulative) | Regime |
|---|---|---|---|
| 0.3 | 20 | 331 | Sub-critical — decays toward a bounded run-rate |
| 0.5 | 20 | 440 | Sub-critical — decays toward a bounded run-rate |
| 0.8 | 20 | 827 | Sub-critical — decays toward a bounded run-rate |

**Key insight:** all three realistic K-factor scenarios (0.3-0.8) are **sub-critical** — none of them produce self-sustaining exponential growth on their own. Referral is a **multiplier on other channels**, not a standalone growth engine, until K exceeds 1.0 (which is rare for most products without a strong built-in sharing incentive). This matters strategically: Career GPS should not expect referral alone to drive growth — it should be layered on top of a channel that provides the external seed.

### Channel 2 — Content/SEO

Assumptions: 4 articles/month, each reaching 150 monthly visits at maturity (after a 3-month SEO ramp), 15% visit-to-signup conversion, $0 direct spend (founder-authored content, time cost only).

**Projected cumulative signups by Month 12: ~4,050**

This is the highest-volume channel in the model, and it's the only one with genuinely near-zero marginal cost — CAC is effectively $0 in cash terms (though not in founder time, which has a real opportunity cost not captured in this $ figure).

### Channel 3 — Community/Partnerships

Assumptions: 2 partnerships/quarter (IITB clubs, other student communities), 40 users per partnership.

**Projected 12-month users: 320**

Lower volume than content/SEO, but highest quality per user (direct community trust transfer) and fastest to activate (no 3-month SEO ramp).

---

## 5. Recommended Channel Mix & 30/60/90 Day Plan

**Recommended mix:** Content/SEO as the primary volume driver (near-zero cash cost, compounds over 12 months), Community/Partnerships for fast, high-trust early cohorts, Referral as a passive multiplier layered on top of both — not pursued as a standalone strategy given its sub-critical K-factor in all realistic scenarios.

**30 days:** Fix the known Activation-stage bugs (F01-F03 from the Feature Prioritization case — this is the same root cause, addressed once, paying off in both frameworks). Publish first 4 SEO articles. Secure first 1-2 community partnerships.

**60 days:** Continue content cadence (8 articles cumulative). Measure actual Activation conversion post-bug-fix against the 90.5% estimate above — this is the first real data point this entire case study should generate. Instrument basic funnel analytics (see Section 6) to replace remaining estimates.

**90 days:** Evaluate real funnel data against the estimates in this document. Reallocate effort based on which stage's real cost-to-improve turns out lowest, using the same "cost, not just size" logic from Section 3 — likely to shift as real bug-fix and content-performance data arrives.

---

## 6. North Star Metric & Required Instrumentation

**Recommended North Star Metric: Weekly Activated Users (users who complete a full plan generation within the week).**

Rationale: Awareness is too shallow (visits, not intent), and Revenue is too far downstream to be a useful weekly signal at this stage. Activation is the first point where a user has received genuine value, and it's the stage most directly actionable in the next 30 days per the plan above.

**To replace every estimate in this document with real data, instrument:**
1. Page-view event on landing (Awareness)
2. "Generate Plan" click event (Acquisition)
3. Successful plan-generation completion event (Activation) — critically, distinguish *attempted* from *successful* generation, since the known Activation bugs (empty sections) mean some "successful" generations are actually broken outputs
4. Return-visit tracking via a simple cookie/localStorage timestamp check (Retention)
5. A real pricing page + checkout flow, once the Pricing Strategy Study's real survey data (see that case) justifies an actual price point (Revenue)
6. Share-button click event (Referral)

Any of Vercel Analytics, Plausible, or a simple custom event log to Supabase would cover this — no need for a heavyweight tool at this stage.

---

## Files
- `funnel_analysis.py` — full working funnel + channel model, reproducible with `python3 funnel_analysis.py`
