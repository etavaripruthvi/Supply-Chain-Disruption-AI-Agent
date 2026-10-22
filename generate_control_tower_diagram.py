"""Generate high-resolution architecture diagram of the Meridian AI Supply Chain Control Tower."""
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

HERE = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(HERE, "output", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

fig, ax = plt.subplots(figsize=(13, 10), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

def draw_box(x, y, w, h, title, subtitle="", fc="#f8fafc", ec="#0284c7", tc="#0f172a", title_size=10, sub_size=8, lw=1.8):
    box = patches.FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=1.0", fc=fc, ec=ec, lw=lw)
    ax.add_patch(box)
    if subtitle:
        ax.text(x, y + h*0.2, title, ha="center", va="center", weight="bold", color=tc, fontsize=title_size)
        ax.text(x, y - h*0.22, subtitle, ha="center", va="center", color="#334155", fontsize=sub_size)
    else:
        ax.text(x, y, title, ha="center", va="center", weight="bold", color=tc, fontsize=title_size)

# 1. Master Header
draw_box(50, 94, 62, 7, "MERIDIAN HOME APPLIANCES: AI CONTROL TOWER", 
         "Plant 1, Chakan (Pune) · 15 Products · 10 Raw Materials · 10 Suppliers · 9 Work Centres · ₹363.9 Cr Revenue", 
         fc="#eff6ff", ec="#1d4ed8", tc="#1e3a8a", title_size=11.5, sub_size=8.5, lw=2.5)

# Connectors down from Master Header
ax.plot([50, 50], [90.5, 84], color="#2563eb", lw=2)
ax.plot([18, 82], [84, 84], color="#2563eb", lw=2)
ax.plot([18, 18], [84, 80], color="#2563eb", lw=2)
ax.plot([50, 50], [84, 80], color="#2563eb", lw=2)
ax.plot([82, 82], [84, 80], color="#2563eb", lw=2)

# Level 1: Tri-Pillar (Vendors, Procurement, Demand)
draw_box(18, 73, 28, 13, "VENDORS (S01 - S10)", 
         "• 10 SCM Partners (9 Domestic, 1 Taiwan)\n• Vadodara Wires (32.7% Spend Share)\n• Pacific Plastics (38d Lead Time)\n• Ahmedabad Coatings (Sole Source RW09)\n• OTD, Defect & Solvency Telemetry",
         fc="#f0fdf4", ec="#16a34a", tc="#14532d", title_size=10, sub_size=7.5)

draw_box(50, 73, 28, 13, "PROCUREMENT ENGINE", 
         "• ₹16,158 Lakhs RM Spend (44.4% Rev)\n• 18 Sourcing Links (Primary / Secondary)\n• Dual Sourcing Split Optimization\n• ₹4,196.8 Lakhs Spend at Risk Guarded\n• Contractual SLA & Penalty Tracking",
         fc="#f0fdf4", ec="#16a34a", tc="#14532d", title_size=10, sub_size=7.5)

draw_box(82, 73, 28, 13, "DEMAND & PRODUCTION", 
         "• 2,620,700 Units Annual Plan\n• 15 Products (Fans, Coolers, Kitchen, Heaters)\n• Seasonal Peak: Summer Apr-27 (Fans/Coolers)\n• Winter Peak: Dec-Feb (Heaters/Rods)\n• Festive Peak: Oct-Dec (Mixers/Cooktops)",
         fc="#f0fdf4", ec="#16a34a", tc="#14532d", title_size=10, sub_size=7.5)

# Connectors to Inventory Engine
ax.plot([18, 50], [66.5, 61], color="#059669", lw=1.8, linestyle="--")
ax.plot([50, 50], [66.5, 61], color="#059669", lw=2)
ax.plot([82, 50], [66.5, 61], color="#059669", lw=1.8, linestyle="--")

# Level 2: Inventory Engine
draw_box(50, 55, 76, 11, "INVENTORY ENGINE (10 RAW MATERIALS RW01 - RW10)", 
         "ABC Stratification (RW01, RW02, RW03, RW04, RW06 in Class A)  |  ₹718.9 Lakhs Stock Value (16.2 Days Spend)\nReorder Triggers: RW02 (CRCA Sheet) & RW06 (ABS Granules) REORDER NOW  |  RW03 (Aluminium ADC12) on WATCH",
         fc="#fefce8", ec="#ca8a04", tc="#713f12", title_size=10.5, sub_size=8)

# Connector to Logistics Engine
ax.annotate("", xy=(50, 44), xytext=(50, 49.5), arrowprops=dict(arrowstyle="->", lw=2.2, color="#b45309"))

# Level 3: Logistics Engine
draw_box(50, 40, 60, 7.5, "LOGISTICS & INBOUND TMS ENGINE", 
         "3,200 Shipments Analyzed  •  Multi-Modal: Road, Rail+Road, Sea+Road (Taiwan Corridor)\nCheckpoint Tracking  •  Delay Trend Creep (60d vs 120d Baseline)  •  Port Clearance Risk",
         fc="#fff7ed", ec="#ea580c", tc="#7c2d12", title_size=10, sub_size=7.5)

# Connector to Risk Engine
ax.annotate("", xy=(50, 31), xytext=(50, 36.25), arrowprops=dict(arrowstyle="->", lw=2.2, color="#c2410c"))

# Level 4: Risk Engine
draw_box(50, 27.5, 52, 6.5, "MULTI-ECHELON DISRUPTION RISK ENGINE", 
         "Inbound Delivery (35%) • Inventory Buffer (25%) • MES Production (20%) • Solvency Health (20%)\nCritical Sole-Source Floor Evaluator (S09 Enforced Floor @ 72.5)",
         fc="#fef2f2", ec="#dc2626", tc="#991b1b", title_size=10, sub_size=7.5)

# Connector to Decision Engine
ax.annotate("", xy=(50, 19.5), xytext=(50, 24.25), arrowprops=dict(arrowstyle="->", lw=2.2, color="#b91c1c"))

# Level 5: AI Decision Engine & Control Tower
draw_box(50, 15, 72, 8.5, "AI DECISION ENGINE & OPERATIONS CONTROL TOWER", 
         "Capacity Balancing: 9 Work Centres (Press, HPDC, Moulding, Winding, Powder Coat, FA-1, FA-2, FA-3, Packing)\nPeak Overload Containment: FA-1 (109% in Apr-27), FA-3 (106% in Jan-27)  |  SLA Routing (<24h, <3d, <2w)",
         fc="#faf5ff", ec="#9333ea", tc="#581c87", title_size=10.5, sub_size=8)

# Connector to Final Copilot
ax.annotate("", xy=(50, 6), xytext=(50, 10.75), arrowprops=dict(arrowstyle="->", lw=2.5, color="#7e22ce"))

# Level 6: Autonomous Copilot
draw_box(50, 3.5, 56, 5, "AUTONOMOUS SCM OPERATIONS COPILOT (LLM)", 
         "Generative RCA Diagnosis • Formal Vendor Cure Notices • Emergency PO Diversion • Plant Work-Order Rebalancing",
         fc="#fdf4ff", ec="#c026d3", tc="#701a75", title_size=10, sub_size=7.5)

plt.title("Target Macro-Architecture: Meridian Home Appliances AI Supply Chain Control Tower", fontsize=12.5, weight="bold", pad=15)
plt.tight_layout()
out_file = os.path.join(FIG_DIR, "fig8_control_tower_macro.png")
plt.savefig(out_file, bbox_inches="tight")
plt.close()
print(f"Generated Control Tower Architecture Diagram for Meridian: {out_file}")
