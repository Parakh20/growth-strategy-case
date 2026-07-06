"""
Growth Strategy Case Study — Career GPS
Funnel analysis + channel modeling + CAC/LTV by channel.

Funnel data note: Career GPS is a real deployed hackathon project but
does not have production analytics instrumentation (no Vercel Analytics/
Mixpanel wired up at hackathon stage). Funnel numbers below are
estimates built from plausible hackathon-stage traffic patterns,
explicitly labeled as such in every output. Real numbers require
adding basic event tracking (documented in Section 6).
"""
import pandas as pd
import numpy as np

# ---- Funnel stages (ESTIMATED, not measured - no analytics instrumented) ----
funnel = pd.DataFrame({
    "stage": ["Awareness (landing page visit)", "Acquisition (plan generation started)",
              "Activation (plan fully generated)", "Retention (returned within 7 days)",
              "Revenue (would-be Pro conversion, hypothetical)", "Referral (shared plan)"],
    "users": [1000, 420, 380, 95, 19, 12],
})
funnel["conversion_from_prev_pct"] = (funnel["users"] / funnel["users"].shift(1) * 100).round(1)
funnel.loc[0, "conversion_from_prev_pct"] = 100.0
funnel["absolute_drop"] = funnel["users"].shift(1) - funnel["users"]
funnel.loc[0, "absolute_drop"] = 0
funnel["cumulative_conversion_pct"] = (funnel["users"] / funnel["users"].iloc[0] * 100).round(1)

print("=" * 80)
print("FUNNEL ANALYSIS (ESTIMATED — no production analytics instrumented)")
print("=" * 80)
print(funnel.to_string(index=False))

# ---- Revenue impact of fixing each stage ----
# Assume hypothetical Pro tier at $7/mo (mid-point of PSM range from pricing study)
ARPU_PRO = 7.0
CURRENT_PRO_CONVERSIONS = funnel.loc[4, "users"]

print("\n" + "=" * 80)
print("REVENUE IMPACT OF +10% CONVERSION AT EACH STAGE")
print("=" * 80)
for i in range(1, len(funnel)-1):  # skip awareness (no prior stage) and referral (no direct $ impact modeled)
    stage = funnel.loc[i, "stage"]
    current = funnel.loc[i, "users"]
    prior = funnel.loc[i-1, "users"]
    current_rate = current / prior
    improved_rate = current_rate * 1.10
    improved_users = prior * improved_rate

    # propagate forward through remaining funnel using existing downstream conversion rates
    downstream_rate = 1.0
    for j in range(i+1, 5):  # up to Revenue stage (index 4)
        downstream_rate *= funnel.loc[j, "users"] / funnel.loc[j-1, "users"]
    new_pro_conversions = improved_users * downstream_rate
    current_pro_conversions_from_this_stage = current * downstream_rate
    delta_conversions = new_pro_conversions - current_pro_conversions_from_this_stage
    delta_revenue_monthly = delta_conversions * ARPU_PRO

    print(f"{stage:45s}  +10% here -> +{delta_conversions:5.2f} Pro conversions/mo -> +${delta_revenue_monthly:6.2f} MRR")

# ---- Bottleneck identification: not highest %-drop, but highest revenue-impact ----
print("\n--- BOTTLENECK: ranked by REVENUE IMPACT, not just %% drop-off ---")
print("(See which stage's improvement moves the most dollars, not just which has the biggest raw drop)")

# ---- Channel modeling: CAC/LTV across 3 channels ----
print("\n" + "=" * 80)
print("CHANNEL STRATEGY MODEL (12-month projection, ESTIMATED)")
print("=" * 80)

months = np.arange(1, 13)

# Referral/viral channel
K_FACTOR_SCENARIOS = [0.3, 0.5, 0.8]
EXTERNAL_SEED_PER_MONTH = 20  # new users arriving from other channels each month, feeding the loop
print("\nViral growth simulation (single-generation invite-decay model, "
      f"external seed={EXTERNAL_SEED_PER_MONTH}/mo):")
for k in K_FACTOR_SCENARIOS:
    new_this_month = 0
    total = 0
    trajectory = []
    for m in months:
        new_this_month = EXTERNAL_SEED_PER_MONTH + new_this_month * k
        total += new_this_month
        trajectory.append(total)
    regime = "sub-critical (K<1): decays toward a bounded run-rate, does not compound without bound" if k < 1 else "critical/super-critical: compounds without bound"
    print(f"  K={k}: Month 1={trajectory[0]:.0f} cumulative -> Month 12={trajectory[-1]:.0f} cumulative  [{regime}]")

# Content/SEO channel
articles_per_month = 4
avg_monthly_traffic_per_article_at_maturity = 150  # after 3-month SEO ramp
conversion_to_signup = 0.15
print(f"\nContent/SEO channel (assumptions: {articles_per_month} articles/mo, "
      f"{avg_monthly_traffic_per_article_at_maturity} monthly visits/article at maturity, "
      f"{conversion_to_signup*100:.0f}% visit-to-signup):")
cumulative_articles = 0
cumulative_signups = 0
for m in months:
    cumulative_articles += articles_per_month
    mature_articles = max(0, cumulative_articles - 3*articles_per_month)  # 3-month ramp to maturity
    monthly_traffic = mature_articles * avg_monthly_traffic_per_article_at_maturity
    monthly_signups = monthly_traffic * conversion_to_signup
    cumulative_signups += monthly_signups
print(f"  Projected cumulative signups by month 12: {cumulative_signups:.0f}")
content_cac = 0  # time cost only, no paid spend assumed
print(f"  CAC: ~$0 direct spend (time cost only, founder-authored content)")

# Community/partnerships channel
partnerships_per_quarter = 2
users_per_partnership = 40
print(f"\nCommunity/partnerships channel (assumptions: {partnerships_per_quarter} partnerships/quarter, "
      f"{users_per_partnership} users/partnership):")
total_partnership_users = partnerships_per_quarter * 4 * users_per_partnership
print(f"  Projected 12-month users: {total_partnership_users}")

