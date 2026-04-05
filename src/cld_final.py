"""
BSAD 482 - Final Causal Loop Diagram (Milestone 4)
Halifax First-Time Homebuyer Decision System
- Same 12 variables as refined CLD
- Leverage point (housing supply) highlighted visually
- Cleaner layout, consistent notation
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import matplotlib.patheffects as pe

fig, ax = plt.subplots(figsize=(18, 13))
ax.set_xlim(0, 18)
ax.set_ylim(0, 13)
ax.axis('off')
ax.set_facecolor('#FFFFFF')
fig.patch.set_facecolor('#FFFFFF')

# ── node positions ─────────────────────────────────────────────────────────
nodes = {
    'population_growth':   (9.0, 12.2),
    'housing_prices':      (9.0, 9.8),
    'buyer_demand':        (3.8, 8.5),
    'housing_supply':      (14.2, 8.5),   # leverage point
    'buyer_confidence':    (9.0, 7.2),
    'affordability':       (3.8, 5.2),
    'time_on_market':      (14.2, 5.5),
    'mortgage_rate':       (9.0, 3.5),
    'boc_policy_rate':     (14.2, 2.5),
    'inflation':           (16.5, 4.5),
    'rental_cost':         (1.5, 5.2),
    'rental_vacancy':      (1.5, 2.8),
}

LEVERAGE = 'housing_supply'
node_radius = 0.92

# ── node styles ─────────────────────────────────────────────────────────────
node_styles = {
    'housing_prices':   ('#1D4ED8', '#DBEAFE', 'Housing\nPrices'),
    'buyer_demand':     ('#15803D', '#DCFCE7', 'Buyer\nDemand'),
    'housing_supply':   ('#166534', '#BBF7D0', 'Housing\nSupply'),   # leverage — greener
    'affordability':    ('#B91C1C', '#FEE2E2', 'Affordability\n(inverse)'),
    'mortgage_rate':    ('#6D28D9', '#EDE9FE', '5-Year\nMortgage Rate'),
    'boc_policy_rate':  ('#0369A1', '#E0F2FE', 'BoC Policy\nRate'),
    'rental_vacancy':   ('#0E7490', '#CFFAFE', 'Rental\nVacancy Rate'),
    'rental_cost':      ('#92400E', '#FEF3C7', 'Rental\nCost'),
    'buyer_confidence': ('#1D4ED8', '#DBEAFE', 'Buyer\nConfidence'),
    'population_growth':('#374151', '#F3F4F6', 'Population\nGrowth'),
    'time_on_market':   ('#5B21B6', '#EDE9FE', 'Avg Days\non Market'),
    'inflation':        ('#9F1239', '#FFE4E6', 'Inflation'),
}

for key, (x, y) in nodes.items():
    edge_c, face_c, label = node_styles[key]
    lw = 3.5 if key == LEVERAGE else 2.0

    circle = plt.Circle((x, y), node_radius, color=face_c,
                         ec=edge_c, linewidth=lw, zorder=4)
    ax.add_patch(circle)

    # leverage point gets a star badge
    if key == LEVERAGE:
        ax.text(x + node_radius * 0.72, y + node_radius * 0.72,
                '★', fontsize=14, color='#166534', zorder=7,
                ha='center', va='center', fontweight='bold')

    ax.text(x, y, label, ha='center', va='center',
            fontsize=9.2, fontweight='bold', color=edge_c,
            zorder=5, linespacing=1.3)


# ── arrow helper ────────────────────────────────────────────────────────────
def arrow(from_k, to_k, polarity, color, rad=0.0, loffset=(0, 0)):
    x1, y1 = nodes[from_k]
    x2, y2 = nodes[to_k]
    dx, dy = x2 - x1, y2 - y1
    dist = (dx**2 + dy**2) ** 0.5
    ux, uy = dx / dist, dy / dist
    sx, sy = x1 + ux * node_radius, y1 + uy * node_radius
    ex, ey = x2 - ux * node_radius, y2 - uy * node_radius

    patch = FancyArrowPatch(
        (sx, sy), (ex, ey),
        arrowstyle='->', mutation_scale=17,
        color=color, linewidth=1.9,
        connectionstyle=f'arc3,rad={rad}', zorder=3
    )
    ax.add_patch(patch)

    mx = (sx + ex) / 2 + loffset[0]
    my = (sy + ey) / 2 + loffset[1]
    sc = '#15803D' if polarity == '+' else '#B91C1C'
    ax.text(mx, my, polarity, fontsize=13, fontweight='black',
            color=sc, ha='center', va='center', zorder=6,
            bbox=dict(boxstyle='round,pad=0.18', facecolor='white',
                      edgecolor=sc, linewidth=1.4))


# ── causal links ─────────────────────────────────────────────────────────────
# Population drivers
arrow('population_growth', 'buyer_demand',    '+', '#374151', rad=-0.15, loffset=(-0.6, 0.3))
arrow('population_growth', 'housing_supply',  '+', '#374151', rad=0.15,  loffset=(0.6, 0.3))
arrow('population_growth', 'rental_vacancy',  '-', '#374151', rad=0.45,  loffset=(-0.4, 0.3))

# R1 — Demand-Price-Confidence
arrow('buyer_demand',      'housing_prices',  '+', '#1D4ED8', rad=-0.15, loffset=(-0.6, 0.2))
arrow('housing_prices',    'buyer_confidence','+', '#1D4ED8', rad=-0.1,  loffset=(0.5, -0.1))
arrow('buyer_confidence',  'buyer_demand',    '+', '#1D4ED8', rad=-0.1,  loffset=(-0.5, 0))

# B1 — Affordability
arrow('housing_prices',    'affordability',   '-', '#B91C1C', rad=0.0,   loffset=(-0.6, 0))
arrow('affordability',     'buyer_demand',    '-', '#B91C1C', rad=0.0,   loffset=(0, 0.3))

# B3 — Supply (leverage loop)
arrow('housing_supply',    'housing_prices',  '-', '#166534', rad=-0.15, loffset=(0.6, 0.2))
arrow('housing_prices',    'housing_supply',  '+', '#166534', rad=0.3,   loffset=(1.2, 0))
arrow('housing_supply',    'time_on_market',  '+', '#5B21B6', rad=0.0,   loffset=(0.5, 0))
arrow('time_on_market',    'housing_prices',  '-', '#5B21B6', rad=0.2,   loffset=(0.7, -0.3))

# Mortgage / BoC chain
arrow('boc_policy_rate',   'mortgage_rate',   '+', '#6D28D9', rad=-0.1,  loffset=(0, 0.4))
arrow('inflation',         'boc_policy_rate', '+', '#9F1239', rad=-0.1,  loffset=(0, 0.3))
arrow('mortgage_rate',     'affordability',   '-', '#6D28D9', rad=0.2,   loffset=(0.5, 0.2))
arrow('mortgage_rate',     'buyer_demand',    '-', '#6D28D9', rad=0.3,   loffset=(-0.6, 0))

# B2 — Rental pressure
arrow('rental_vacancy',    'rental_cost',     '-', '#0E7490', rad=0.0,   loffset=(-0.5, 0))
arrow('rental_cost',       'buyer_demand',    '+', '#92400E', rad=0.0,   loffset=(0, 0.3))
arrow('buyer_demand',      'rental_vacancy',  '-', '#0E7490', rad=0.4,   loffset=(-1.2, 0))
arrow('rental_cost',       'affordability',   '-', '#92400E', rad=0.0,   loffset=(-0.4, 0))


# ── loop badges ──────────────────────────────────────────────────────────────
def badge(x, y, letter, bcolor, name):
    ax.text(x, y, letter, fontsize=17, fontweight='black',
            color=bcolor, ha='center', va='center', zorder=8,
            bbox=dict(boxstyle='circle,pad=0.35', facecolor='white',
                      edgecolor=bcolor, linewidth=2.4))
    ax.text(x, y - 1.05, name, fontsize=8.5, color=bcolor,
            ha='center', va='top', fontweight='bold', zorder=8,
            bbox=dict(boxstyle='round,pad=0.28', facecolor='white',
                      edgecolor=bcolor, linewidth=1.2, alpha=0.95))

badge(6.3,  8.2,  'R1', '#1D4ED8', 'Demand–\nConfidence Loop')
badge(4.6,  6.8,  'B1', '#B91C1C', 'Affordability\nBalancing Loop')
badge(1.8,  7.6,  'B2', '#0E7490', 'Rental\nPressure Loop')
badge(13.2, 7.0,  'B3', '#166534', 'Supply\nResponse Loop\n(Leverage Point)')


# ── leverage point note ───────────────────────────────────────────────────────
ax.annotate(
    '★  LEVERAGE POINT\n     Accelerate housing supply\n     to dampen price growth',
    xy=(nodes[LEVERAGE][0], nodes[LEVERAGE][1] - node_radius),
    xytext=(14.2, 10.8),
    fontsize=8.5, color='#166534', fontweight='bold',
    ha='center', zorder=9,
    bbox=dict(boxstyle='round,pad=0.4', facecolor='#F0FDF4',
              edgecolor='#166534', linewidth=1.5),
    arrowprops=dict(arrowstyle='->', color='#166534', lw=1.4)
)


# ── legend ────────────────────────────────────────────────────────────────────
lx, ly = 0.25, 11.6
ax.text(lx + 1.3, ly + 0.4, 'Legend', fontsize=10, fontweight='bold', color='#111', ha='center')
ax.annotate('', xy=(lx + 0.95, ly), xytext=(lx + 0.1, ly),
            arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))
ax.text(lx + 1.05, ly, '  +  Increases', fontsize=9, color='#15803D', va='center')
ax.annotate('', xy=(lx + 0.95, ly - 0.55), xytext=(lx + 0.1, ly - 0.55),
            arrowprops=dict(arrowstyle='->', color='#333', lw=1.5))
ax.text(lx + 1.05, ly - 0.55, '  −  Decreases', fontsize=9, color='#B91C1C', va='center')
ax.text(lx + 0.55, ly - 1.15,
        '★  = Leverage point\nThick border = key node',
        fontsize=8.5, color='#374151', va='top')


# ── title ─────────────────────────────────────────────────────────────────────
ax.set_title(
    'Final Causal Loop Diagram — Halifax First-Time Homebuyer Decision System\n'
    'BSAD 482 Term Project',
    fontsize=14, fontweight='bold', color='#111827', pad=14
)

fig.tight_layout()
fig.savefig('/home/user/workspace/bsad482/img/cld-final.png',
            dpi=180, bbox_inches='tight', facecolor='white')
plt.close()
print("cld-final.png saved")
