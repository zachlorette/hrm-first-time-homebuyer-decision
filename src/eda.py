"""
BSAD 482 - Term Project: Milestone 2 EDA
Decision: Should a first-time homebuyer in HRM buy in 2026 or wait ~18 months?
Author: Zach Lorette
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import warnings
warnings.filterwarnings('ignore')

# ── style ──────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    'figure.dpi': 150,
    'font.family': 'DejaVu Sans',
    'font.size': 11,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': True,
    'grid.alpha': 0.35,
    'axes.prop_cycle': plt.cycler(color=[
        '#2563EB', '#DC2626', '#16A34A', '#D97706', '#7C3AED', '#0891B2'
    ])
})

DATA = '/home/user/workspace/bsad482/data'
IMG  = '/home/user/workspace/bsad482/img'

# ── load data ──────────────────────────────────────────────────────────────────
rates = pd.read_csv(f'{DATA}/interest_rates.csv', parse_dates=['date'])
market = pd.read_csv(f'{DATA}/halifax_housing_market.csv', parse_dates=['date'])
afford = pd.read_csv(f'{DATA}/hrm_affordability.csv')
afford['year'] = afford['year'].astype(int)

# merge market + rates on date (monthly)
df = pd.merge(market, rates, on='date', how='left')

# ══════════════════════════════════════════════════════════════════════════════
# VIZ 1 — House Price vs Policy Rate over time (dual axis, trend)
# ══════════════════════════════════════════════════════════════════════════════
fig, ax1 = plt.subplots(figsize=(12, 5.5))

color_price = '#2563EB'
color_rate  = '#DC2626'

ax1.fill_between(df['date'], df['avg_sale_price_cad'] / 1000,
                 alpha=0.12, color=color_price)
ax1.plot(df['date'], df['avg_sale_price_cad'] / 1000,
         color=color_price, linewidth=2.2, label='Avg Sale Price (left)')
ax1.set_ylabel('Average Sale Price ($000s CAD)', color=color_price, fontsize=11)
ax1.tick_params(axis='y', labelcolor=color_price)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:.0f}k'))

ax2 = ax1.twinx()
ax2.plot(df['date'], df['boc_policy_rate_pct'],
         color=color_rate, linewidth=2.2, linestyle='--', label='BoC Policy Rate (right)')
ax2.set_ylabel('BoC Policy Rate (%)', color=color_rate, fontsize=11)
ax2.tick_params(axis='y', labelcolor=color_rate)
ax2.spines['right'].set_visible(True)
ax2.spines['top'].set_visible(False)

# annotate key events
events = [
    ('2020-03-01', 0.25, 'COVID cuts'),
    ('2022-03-01', 0.50, 'Rate hike\ncycle begins'),
    ('2023-07-01', 5.00, 'Peak\n5.0%'),
    ('2024-06-01', 4.75, 'Cuts\nbegin'),
]
for edate, erate, label in events:
    edt = pd.Timestamp(edate)
    ax2.annotate(label, xy=(edt, erate),
                 xytext=(0, 22), textcoords='offset points',
                 arrowprops=dict(arrowstyle='->', color='#555', lw=1.2),
                 fontsize=8.5, ha='center', color='#333')

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=9)

ax1.set_title('Halifax Average House Price vs Bank of Canada Policy Rate\n(Jan 2015 – Dec 2025)',
              fontsize=13, fontweight='bold', pad=10)
ax1.set_xlabel('')
fig.tight_layout()
fig.savefig(f'{IMG}/viz1_price_vs_rate.png', bbox_inches='tight')
plt.close()
print("viz1 saved")

# ══════════════════════════════════════════════════════════════════════════════
# VIZ 2 — Affordability ratio & inventory over time
# ══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# Monthly market inventory (months of supply)
color_inv = '#16A34A'
axes[0].fill_between(df['date'], df['months_of_inventory'], alpha=0.15, color=color_inv)
axes[0].plot(df['date'], df['months_of_inventory'], color=color_inv, linewidth=2)
axes[0].axhline(3.0, color='#999', linestyle=':', linewidth=1.5, label="Balanced market (~3 months)")
axes[0].set_ylabel("Months of Inventory", fontsize=10)
axes[0].set_title("Halifax Housing Supply: Months of Inventory (2015–2025)", fontsize=12, fontweight='bold')
axes[0].legend(fontsize=9)
axes[0].set_ylim(0, 11)

# Affordability ratio (annual, matched to year)
afford_monthly = pd.DataFrame({
    'date': pd.date_range('2015-01-01', periods=11*12, freq='MS')
})
afford_monthly['year'] = afford_monthly['date'].dt.year
afford_monthly = afford_monthly[afford_monthly['year'] <= 2025]
afford_monthly = afford_monthly.merge(afford[['year','affordability_ratio_pct']], on='year')

color_aff = '#D97706'
axes[1].fill_between(afford_monthly['date'], afford_monthly['affordability_ratio_pct'],
                     alpha=0.15, color=color_aff)
axes[1].plot(afford_monthly['date'], afford_monthly['affordability_ratio_pct'],
             color=color_aff, linewidth=2)
axes[1].axhline(32, color='#999', linestyle=':', linewidth=1.5, label="Traditional affordability threshold (32% GDS)")
axes[1].set_ylabel("Monthly Mortgage Pmt\nas % of Monthly Income", fontsize=10)
axes[1].set_title("HRM Housing Affordability Ratio: Monthly Mortgage Payment vs Median Income (2015–2025)",
                  fontsize=12, fontweight='bold')
axes[1].legend(fontsize=9)
axes[1].set_ylim(20, 60)

fig.tight_layout(h_pad=2.5)
fig.savefig(f'{IMG}/viz2_affordability_inventory.png', bbox_inches='tight')
plt.close()
print("viz2 saved")

# ══════════════════════════════════════════════════════════════════════════════
# VIZ 3 — Scatter: Mortgage Rate vs Affordability + Units Sold (relationship)
# ══════════════════════════════════════════════════════════════════════════════
# Merge annual affordability with avg annual mortgage rates
annual_rates = rates.copy()
annual_rates['year'] = annual_rates['date'].dt.year
annual_rates_agg = annual_rates.groupby('year').agg(
    avg_mortgage=('mortgage_5yr_posted_rate_pct', 'mean'),
    avg_boc=('boc_policy_rate_pct', 'mean')
).reset_index()

annual_market = market.copy()
annual_market['year'] = annual_market['date'].dt.year
annual_market_agg = annual_market.groupby('year').agg(
    avg_price=('avg_sale_price_cad', 'mean'),
    total_units=('units_sold', 'sum')
).reset_index()

scatter_df = afford.merge(annual_rates_agg, on='year').merge(annual_market_agg, on='year')
scatter_df = scatter_df[scatter_df['year'] <= 2025]

fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))

# Left: mortgage rate vs affordability ratio
sc1 = axes[0].scatter(scatter_df['avg_mortgage'], scatter_df['affordability_ratio_pct'],
                      c=scatter_df['year'], cmap='RdYlGn_r',
                      s=120, zorder=5, edgecolors='white', linewidths=0.8)
# Label each point with year
for _, row in scatter_df.iterrows():
    axes[0].annotate(str(int(row['year'])),
                     xy=(row['avg_mortgage'], row['affordability_ratio_pct']),
                     xytext=(5, 3), textcoords='offset points', fontsize=8, color='#444')

# Regression line
m, b = np.polyfit(scatter_df['avg_mortgage'], scatter_df['affordability_ratio_pct'], 1)
xr = np.linspace(scatter_df['avg_mortgage'].min(), scatter_df['avg_mortgage'].max(), 100)
axes[0].plot(xr, m*xr + b, color='#555', linestyle='--', linewidth=1.5, alpha=0.7)

corr1 = scatter_df['avg_mortgage'].corr(scatter_df['affordability_ratio_pct'])
axes[0].set_xlabel("Average 5-Year Posted Mortgage Rate (%)", fontsize=10)
axes[0].set_ylabel("Affordability Ratio (% of income)", fontsize=10)
axes[0].set_title(f"Mortgage Rate vs Affordability\n(r = {corr1:.2f})", fontsize=11, fontweight='bold')
plt.colorbar(sc1, ax=axes[0], label='Year')

# Right: mortgage rate vs units sold
sc2 = axes[1].scatter(scatter_df['avg_mortgage'], scatter_df['total_units'],
                      c=scatter_df['year'], cmap='RdYlGn_r',
                      s=120, zorder=5, edgecolors='white', linewidths=0.8)
for _, row in scatter_df.iterrows():
    axes[1].annotate(str(int(row['year'])),
                     xy=(row['avg_mortgage'], row['total_units']),
                     xytext=(5, 3), textcoords='offset points', fontsize=8, color='#444')

m2, b2 = np.polyfit(scatter_df['avg_mortgage'], scatter_df['total_units'], 1)
axes[1].plot(xr, m2*xr + b2, color='#555', linestyle='--', linewidth=1.5, alpha=0.7)

corr2 = scatter_df['avg_mortgage'].corr(scatter_df['total_units'])
axes[1].set_xlabel("Average 5-Year Posted Mortgage Rate (%)", fontsize=10)
axes[1].set_ylabel("Annual Units Sold", fontsize=10)
axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
axes[1].set_title(f"Mortgage Rate vs Market Activity\n(r = {corr2:.2f})", fontsize=11, fontweight='bold')
plt.colorbar(sc2, ax=axes[1], label='Year')

fig.suptitle("Relationship Between Mortgage Rates and Halifax Housing Market Outcomes (2015–2025)",
             fontsize=12, fontweight='bold', y=1.02)
fig.tight_layout()
fig.savefig(f'{IMG}/viz3_rate_relationships.png', bbox_inches='tight')
plt.close()
print(f"viz3 saved  |  r(rate,afford)={corr1:.3f}  r(rate,sales)={corr2:.3f}")

# ══════════════════════════════════════════════════════════════════════════════
# VIZ 4 — Population growth, housing starts, and rent pressure
# ══════════════════════════════════════════════════════════════════════════════
fig, axes = plt.subplots(2, 1, figsize=(12, 8))

# Top: population vs housing starts
ax_pop = axes[0]
ax_starts = ax_pop.twinx()

ax_pop.bar(afford['year'], afford['hrm_population'] / 1000,
           color='#2563EB', alpha=0.5, label='Population (left, 000s)')
ax_starts.plot(afford['year'], afford['housing_starts'],
               color='#DC2626', marker='o', linewidth=2, markersize=6,
               label='Housing Starts (right)')

ax_pop.set_ylabel("HRM Population (000s)", color='#2563EB', fontsize=10)
ax_starts.set_ylabel("Annual Housing Starts (units)", color='#DC2626', fontsize=10)
ax_starts.spines['right'].set_visible(True)
ax_starts.spines['top'].set_visible(False)
ax_pop.tick_params(axis='y', labelcolor='#2563EB')
ax_starts.tick_params(axis='y', labelcolor='#DC2626')

handles1, labels1 = ax_pop.get_legend_handles_labels()
handles2, labels2 = ax_starts.get_legend_handles_labels()
ax_pop.legend(handles1 + handles2, labels1 + labels2, loc='upper left', fontsize=9)
ax_pop.set_title("HRM Population Growth vs Annual Housing Starts (2015–2025)",
                  fontsize=12, fontweight='bold')
ax_pop.set_xticks(afford['year'])

# Bottom: average rent vs vacancy rate
ax_rent = axes[1]
ax_vac = ax_rent.twinx()

ax_rent.bar(afford['year'], afford['avg_monthly_rent_2br_cad'],
            color='#D97706', alpha=0.55, label='Avg 2BR Rent (left)')
ax_vac.plot(afford['year'], afford['rental_vacancy_rate_pct'],
            color='#7C3AED', marker='s', linewidth=2, markersize=6,
            label='Rental Vacancy Rate % (right)')
ax_vac.axhline(3.0, color='#999', linestyle=':', linewidth=1.4)
ax_vac.annotate("Healthy vacancy\n(~3%)", xy=(2025, 3.0),
                xytext=(-5, 8), textcoords='offset points',
                fontsize=8.5, color='#666')

ax_rent.set_ylabel("Avg Monthly Rent, 2BR (CAD)", color='#D97706', fontsize=10)
ax_vac.set_ylabel("Rental Vacancy Rate (%)", color='#7C3AED', fontsize=10)
ax_vac.spines['right'].set_visible(True)
ax_vac.spines['top'].set_visible(False)
ax_rent.tick_params(axis='y', labelcolor='#D97706')
ax_vac.tick_params(axis='y', labelcolor='#7C3AED')

handles3, labels3 = ax_rent.get_legend_handles_labels()
handles4, labels4 = ax_vac.get_legend_handles_labels()
ax_rent.legend(handles3 + handles4, labels3 + labels4, loc='upper left', fontsize=9)
ax_rent.set_title("HRM Rental Market Pressure: Average Rent vs Vacancy Rate (2015–2025)",
                   fontsize=12, fontweight='bold')
ax_rent.set_xticks(afford['year'])

fig.tight_layout(h_pad=3)
fig.savefig(f'{IMG}/viz4_supply_rental.png', bbox_inches='tight')
plt.close()
print("viz4 saved")

# ══════════════════════════════════════════════════════════════════════════════
# VIZ 5 (BONUS) — Buy-vs-Wait 5-year total cost scenario comparison
# ══════════════════════════════════════════════════════════════════════════════

def monthly_payment(principal, annual_rate, months):
    r = annual_rate / 12 / 100
    return principal * r * (1+r)**months / ((1+r)**months - 1)

def scenario_cost(purchase_price, rate_pct, years_wait=0, rent_monthly=0,
                  price_growth_pct=3.5):
    """Total out-of-pocket cost over a 5-year window."""
    down_pct = 0.10
    amort = 25
    wait_cost = rent_monthly * 12 * years_wait
    future_price = purchase_price * (1 + price_growth_pct/100)**years_wait
    principal = future_price * (1 - down_pct)
    monthly = monthly_payment(principal, rate_pct, amort*12)
    # 5 years of mortgage payments (or 5-years_wait remaining years)
    mortgage_months = (5 - years_wait) * 12
    mortgage_cost = monthly * mortgage_months
    down_payment = future_price * down_pct
    return wait_cost + down_payment + mortgage_cost, future_price, monthly

# Scenarios
price_2026 = 530000
rent_2026 = 1790

fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))

# Scenario grid: varying rate and wait period
rates_grid = [4.54, 5.50, 6.50]  # current, medium, high
wait_years = [0, 0.5, 1.0, 1.5]
colors_sc = ['#16A34A', '#D97706', '#DC2626']
markers_sc = ['o', 's', '^']

for i, r in enumerate(rates_grid):
    totals = []
    for w in wait_years:
        cost, fp, mp = scenario_cost(price_2026, r, years_wait=w, rent_monthly=rent_2026)
        totals.append(cost / 1000)
    axes[0].plot(wait_years, totals, color=colors_sc[i], marker=markers_sc[i],
                 linewidth=2, markersize=8, label=f"{r}% rate")

axes[0].set_xlabel("Years Waited Before Buying", fontsize=10)
axes[0].set_ylabel("Total 5-Year Cost ($000s CAD)", fontsize=10)
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:.0f}k'))
axes[0].set_xticks(wait_years)
axes[0].set_xticklabels(['Buy Now', 'Wait 6mo', 'Wait 1yr', 'Wait 18mo'])
axes[0].legend(title="5-yr Mortgage Rate", fontsize=9)
axes[0].set_title("Total 5-Year Cost by Wait Period & Interest Rate\n(10% down, 25yr amort, $530k home, $1,790/mo rent)",
                   fontsize=10.5, fontweight='bold')

# Right: monthly payment sensitivity to purchase price & rate
prices = np.linspace(450000, 650000, 60)
for i, r in enumerate(rates_grid):
    pmts = [monthly_payment(p * 0.90, r, 300) for p in prices]
    axes[1].plot(prices / 1000, pmts, color=colors_sc[i], linewidth=2, label=f"{r}% rate")

axes[1].axvline(530, color='#555', linestyle=':', linewidth=1.5)
axes[1].annotate("Current avg\n$530k", xy=(530, 2700),
                 xytext=(10, 0), textcoords='offset points', fontsize=8.5, color='#555')
axes[1].set_xlabel("Home Purchase Price ($000s CAD)", fontsize=10)
axes[1].set_ylabel("Monthly Mortgage Payment (CAD)", fontsize=10)
axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
axes[1].legend(title="5-yr Rate", fontsize=9)
axes[1].set_title("Monthly Mortgage Payment Sensitivity\n(10% down, 25yr amortization)",
                   fontsize=10.5, fontweight='bold')

fig.suptitle("Buy vs. Wait Scenario Analysis for Halifax First-Time Homebuyer (2026)",
             fontsize=12, fontweight='bold', y=1.02)
fig.tight_layout()
fig.savefig(f'{IMG}/viz5_buy_vs_wait.png', bbox_inches='tight')
plt.close()
print("viz5 saved")

print("\nAll visualizations complete.")
