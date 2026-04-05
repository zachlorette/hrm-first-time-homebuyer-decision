"""
BSAD 482 - Refined Causal Loop Diagram
Halifax First-Time Homebuyer Decision (Milestone 2)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np

fig, ax = plt.subplots(figsize=(17, 13))
ax.set_xlim(0, 17)
ax.set_ylim(0, 13)
ax.axis('off')
ax.set_facecolor('#F8FAFC')
fig.patch.set_facecolor('#F8FAFC')

# ── node positions (spread out to reduce congestion) ─────────────────────────
nodes = {
    'population_growth':   (8.5, 12.2),   # top driver
    'housing_prices':      (8.5, 9.8),    # central
    'buyer_demand':        (3.5, 8.5),    # left middle
    'housing_supply':      (13.5, 8.5),   # right middle
    'buyer_confidence':    (8.5, 7.2),    # center below prices
    'affordability':       (3.5, 5.2),    # lower left
    'time_on_market':      (13.5, 5.5),   # right lower
    'mortgage_rate':       (8.5, 3.5),    # bottom center
    'boc_policy_rate':     (13.5, 2.5),   # bottom right
    'inflation':           (15.8, 4.5),   # far right
    'rental_cost':         (1.5, 5.2),    # far left
    'rental_vacancy':      (1.5, 2.8),    # far left lower
}

# ── node styling ─────────────────────────────────────────────────────────────
node_styles = {
    'housing_prices':   ('#1D4ED8', '#DBEAFE', 'Housing\nPrices'),
    'buyer_demand':     ('#15803D', '#DCFCE7', 'Buyer\nDemand'),
    'housing_supply':   ('#B45309', '#FEF3C7', 'Housing\nSupply'),
    'affordability':    ('#DC2626', '#FEE2E2', 'Affordability\n(inverse)'),
    'mortgage_rate':    ('#7C3AED', '#EDE9FE', '5-Year\nMortgage Rate'),
    'boc_policy_rate':  ('#0369A1', '#E0F2FE', 'BoC Policy\nRate'),
    'rental_vacancy':   ('#0891B2', '#CFFAFE', 'Rental\nVacancy Rate'),
    'rental_cost':      ('#B45309', '#FEF3C7', 'Rental\nCost'),
    'buyer_confidence': ('#1D4ED8', '#DBEAFE', 'Buyer\nConfidence'),
    'population_growth':('#4B5563', '#F3F4F6', 'Population\nGrowth'),
    'time_on_market':   ('#6D28D9', '#EDE9FE', 'Avg Days\non Market'),
    'inflation':        ('#9F1239', '#FFE4E6', 'Inflation'),
}

node_radius = 0.90

for key, (x, y) in nodes.items():
    edge_c, face_c, label = node_styles[key]
    circle = plt.Circle((x, y), node_radius, color=face_c,
                         ec=edge_c, linewidth=2.2, zorder=4)
    ax.add_patch(circle)
    ax.text(x, y, label, ha='center', va='center',
            fontsize=9.0, fontweight='bold', color=edge_c,
            zorder=5, linespacing=1.3)

# ── arrow helper ──────────────────────────────────────────────────────────────
def draw_arrow(ax, from_key, to_key, polarity, color,
               rad=0.0, label_offset=(0, 0)):
    x1, y1 = nodes[from_key]
    x2, y2 = nodes[to_key]
    dx, dy = x2 - x1, y2 - y1
    dist = (dx**2 + dy**2)**0.5
    ux, uy = dx/dist, dy/dist

    sx = x1 + ux * node_radius
    sy = y1 + uy * node_radius
    ex = x2 - ux * node_radius
    ey = y2 - uy * node_radius

    style = f"arc3,rad={rad}"
    arrow = FancyArrowPatch((sx, sy), (ex, ey),
                            arrowstyle='->', mutation_scale=17,
                            color=color, linewidth=1.8,
                            connectionstyle=style, zorder=3)
    ax.add_patch(arrow)

    # polarity label at midpoint with offset
    t = 0.5
    # for curved arrows approximate midpoint
    mx = (sx + ex) / 2 + label_offset[0]
    my = (sy + ey) / 2 + label_offset[1]
    sign_color = '#16A34A' if polarity == '+' else '#DC2626'
    ax.text(mx, my, polarity, fontsize=13, fontweight='black',
            color=sign_color, ha='center', va='center', zorder=6,
            bbox=dict(boxstyle='round,pad=0.18', facecolor='white',
                      edgecolor=sign_color, linewidth=1.4))


# ── causal links ──────────────────────────────────────────────────────────────
# Population drivers
draw_arrow(ax, 'population_growth', 'buyer_demand',   '+', '#4B5563', rad=-0.15, label_offset=(-0.6, 0.3))
draw_arrow(ax, 'population_growth', 'housing_supply', '+', '#4B5563', rad=0.15,  label_offset=(0.6, 0.3))
draw_arrow(ax, 'population_growth', 'rental_vacancy', '-', '#4B5563', rad=0.45,  label_offset=(-0.4, 0.3))

# R1 — Demand-Price-Confidence reinforcing loop
draw_arrow(ax, 'buyer_demand',     'housing_prices',   '+', '#1D4ED8', rad=-0.15, label_offset=(-0.6, 0.2))
draw_arrow(ax, 'housing_prices',   'buyer_confidence', '+', '#1D4ED8', rad=-0.1,  label_offset=(0.5, -0.1))
draw_arrow(ax, 'buyer_confidence', 'buyer_demand',     '+', '#1D4ED8', rad=-0.1,  label_offset=(-0.5, 0))

# B1 — Affordability balancing loop
draw_arrow(ax, 'housing_prices',  'affordability',    '-', '#DC2626', rad=0.0,   label_offset=(-0.6, 0))
draw_arrow(ax, 'affordability',   'buyer_demand',     '-', '#DC2626', rad=0.0,   label_offset=(0, 0.3))

# B3 — Supply response loop
draw_arrow(ax, 'housing_supply',  'housing_prices',   '-', '#B45309', rad=-0.15, label_offset=(0.6, 0.2))
draw_arrow(ax, 'housing_prices',  'housing_supply',   '+', '#B45309', rad=0.3,   label_offset=(1.2, 0))
draw_arrow(ax, 'housing_supply',  'time_on_market',   '+', '#6D28D9', rad=0.0,   label_offset=(0.5, 0))
draw_arrow(ax, 'time_on_market',  'housing_prices',   '-', '#6D28D9', rad=0.2,   label_offset=(0.7, -0.3))

# Mortgage / BoC rate chain
draw_arrow(ax, 'boc_policy_rate', 'mortgage_rate',    '+', '#7C3AED', rad=-0.1,  label_offset=(0, 0.4))
draw_arrow(ax, 'inflation',       'boc_policy_rate',  '+', '#9F1239', rad=-0.1,  label_offset=(0, 0.3))
draw_arrow(ax, 'mortgage_rate',   'affordability',    '-', '#7C3AED', rad=0.2,   label_offset=(0.5, 0.2))
draw_arrow(ax, 'mortgage_rate',   'buyer_demand',     '-', '#7C3AED', rad=0.3,   label_offset=(-0.6, 0))

# B2 — Rental pressure loop
draw_arrow(ax, 'rental_vacancy',  'rental_cost',      '-', '#0891B2', rad=0.0,   label_offset=(-0.5, 0))
draw_arrow(ax, 'rental_cost',     'buyer_demand',     '+', '#B45309', rad=0.0,   label_offset=(0, 0.3))
draw_arrow(ax, 'buyer_demand',    'rental_vacancy',   '-', '#0891B2', rad=0.4,   label_offset=(-1.2, 0))
draw_arrow(ax, 'rental_cost',     'affordability',    '-', '#B45309', rad=0.0,   label_offset=(-0.4, 0))

# ── loop labels (clear separate positions) ────────────────────────────────────
def loop_badge(ax, x, y, badge, bcolor, name):
    ax.text(x, y, badge, fontsize=17, fontweight='black',
            color=bcolor, ha='center', va='center', zorder=8,
            bbox=dict(boxstyle='circle,pad=0.35', facecolor='white',
                      edgecolor=bcolor, linewidth=2.2))
    ax.text(x, y - 1.0, name, fontsize=8.5, color=bcolor,
            ha='center', va='top', fontweight='bold', zorder=8,
            bbox=dict(boxstyle='round,pad=0.25', facecolor='white',
                      edgecolor=bcolor, linewidth=1.2, alpha=0.92))

loop_badge(ax, 6.0, 8.2, 'R1', '#1D4ED8', 'Demand-\nConfidence Loop')
loop_badge(ax, 4.5, 6.8, 'B1', '#DC2626', 'Affordability\nBalancing Loop')
loop_badge(ax, 1.5, 7.5, 'B2', '#0891B2', 'Rental Pressure\nLoop')
loop_badge(ax, 13.0, 7.0, 'B3', '#B45309', 'Supply\nResponse Loop')

# ── legend box ────────────────────────────────────────────────────────────────
leg_x, leg_y = 0.3, 11.5
ax.text(leg_x + 1.2, leg_y + 0.35, "Legend", fontsize=10, fontweight='bold', color='#333', ha='center')
ax.annotate("", xy=(leg_x + 0.9, leg_y),    xytext=(leg_x + 0.1, leg_y),
            arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))
ax.text(leg_x + 1.0, leg_y, '  +  Same direction', fontsize=9, color='#16A34A', va='center')
ax.annotate("", xy=(leg_x + 0.9, leg_y - 0.5), xytext=(leg_x + 0.1, leg_y - 0.5),
            arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))
ax.text(leg_x + 1.0, leg_y - 0.5, '  −  Opposite direction', fontsize=9, color='#DC2626', va='center')

# ── title ─────────────────────────────────────────────────────────────────────
ax.set_title("Refined Causal Loop Diagram: Halifax First-Time Homebuyer Decision System\n"
             "BSAD 482 Term Project — Milestone 2",
             fontsize=14, fontweight='bold', color='#1e293b', pad=14)

fig.tight_layout()
fig.savefig('/home/user/workspace/bsad482/img/cld-refined.png',
            dpi=180, bbox_inches='tight', facecolor='#F8FAFC')
plt.close()
print("CLD refined saved")
