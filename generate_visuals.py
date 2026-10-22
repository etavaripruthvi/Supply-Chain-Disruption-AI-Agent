"""Generate publication-quality figures for Meridian Home Appliances SCM Disruption Solution."""
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output")
FIG_DIR = os.path.join(OUT, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

# Load data
scores = pd.read_csv(os.path.join(OUT, "supplier_risk_scores.csv"))
mat = pd.read_csv(os.path.join(OUT, "material_risk.csv"))
trends = pd.read_csv(os.path.join(OUT, "weekly_delay_trend.csv"))
with open(os.path.join(OUT, "metrics.json"), "r") as f:
    metrics = json.load(f)

# Colors
C_CRIT = "#dc2626"  # Red
C_HIGH = "#ea580c"  # Orange
C_MED  = "#eab308"  # Yellow
C_LOW  = "#16a34a"  # Green
C_BLUE = "#2563eb"  # Primary Blue
C_DARK = "#1e293b"  # Slate Dark

# -------------------------------------------------------------
# 1. Figure 1: Agentic System Architecture Diagram
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 7), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

# Layer 1: Data Sources
rect1 = patches.FancyBboxPatch((3, 68), 20, 25, boxstyle="round,pad=1.5", fc="#eff6ff", ec="#3b82f6", lw=2)
ax.add_patch(rect1)
ax.text(13, 90, "MERIDIAN TELEMETRY\n& DATA INGESTION", ha="center", va="center", weight="bold", color="#1e40af", fontsize=10.5)
ax.text(13, 78, "• Deliveries: 3,200 (TMS)\n• Inventory: 10 SKUs (WMS)\n• MES: 15 Products / 9 WCs\n• ERP: 10 Suppliers S01-S10\n• Port & Transit Corridor Feeds", 
        ha="center", va="center", fontsize=8.5, color="#1e293b")

# Layer 2: Feature Engineering
rect2 = patches.FancyBboxPatch((27, 68), 20, 25, boxstyle="round,pad=1.5", fc="#f8fafc", ec="#64748b", lw=2)
ax.add_patch(rect2)
ax.text(37, 90, "SYNTHESIZER\nAGENT", ha="center", va="center", weight="bold", color="#334155", fontsize=10.5)
ax.text(37, 78, "• 60d vs 120d Delay Trend\n• Runway vs Lead Time (Days)\n• Assembly Yield Shortfalls\n• Sole-Source / HHI Factors\n• Dynamic Renormalization", 
        ha="center", va="center", fontsize=8.5, color="#1e293b")

# Layer 3: Risk Scoring & Inference
rect3 = patches.FancyBboxPatch((51, 68), 21, 25, boxstyle="round,pad=1.5", fc="#fef2f2", ec="#ef4444", lw=2)
ax.add_patch(rect3)
ax.text(61.5, 90, "AI RISK ENGINE\n(Scoring & Anomaly)", ha="center", va="center", weight="bold", color="#b91c1c", fontsize=10.5)
ax.text(61.5, 78, "• Delivery Weight: 35%\n• Inventory Weight: 25%\n• Production Weight: 20%\n• Vendor Health: 20%\n• Critical Sole-Source Floor", 
        ha="center", va="center", fontsize=8.5, color="#1e293b")

# Layer 4: Autonomous Mitigation Agent
rect4 = patches.FancyBboxPatch((76, 68), 21, 25, boxstyle="round,pad=1.5", fc="#faf5ff", ec="#a855f7", lw=2)
ax.add_patch(rect4)
ax.text(86.5, 90, "AUTONOMOUS LLM\nMITIGATION COPILOT", ha="center", va="center", weight="bold", color="#6b21a8", fontsize=10.5)
ax.text(86.5, 78, "• Executive RCA Diagnosis\n• Vendor Legal Cure Notices\n• PO Dual-Sourcing Routing\n• Line Balancing Directives\n• ERP Action Dispatch", 
        ha="center", va="center", fontsize=8.5, color="#1e293b")

# Arrows top layer
ax.annotate("", xy=(27, 80), xytext=(23, 80), arrowprops=dict(arrowstyle="->", lw=2.5, color="#2563eb"))
ax.annotate("", xy=(51, 80), xytext=(47, 80), arrowprops=dict(arrowstyle="->", lw=2.5, color="#2563eb"))
ax.annotate("", xy=(76, 80), xytext=(72, 80), arrowprops=dict(arrowstyle="->", lw=2.5, color="#2563eb"))

# Bottom Layer: Dispatch & Action Execution
rect5 = patches.FancyBboxPatch((8, 12), 84, 44, boxstyle="round,pad=2", fc="#f0fdf4", ec="#22c55e", lw=2)
ax.add_patch(rect5)
ax.text(50, 50, "MERIDIAN CHAKAN PLANT: CLOSED-LOOP SLA DISPATCH & ORCHESTRATION", ha="center", va="center", weight="bold", color="#15803d", fontsize=11.5)

# Action boxes
boxes = [
    ("CRITICAL (>=70)", "Owner: Plant Mgr + Head SC\nSLA: < 24 Hours\nAction: S09 Emergency PO, Air Freight", "#fecaca", "#dc2626", 18),
    ("HIGH (50 - 69)", "Owner: Category Lead\nSLA: < 3 Days\nAction: S08 Taiwan Resin Shift, Expedite PO", "#fed7aa", "#ea580c", 39),
    ("MEDIUM (30 - 49)", "Owner: SRM Lead\nSLA: < 2 Weeks\nAction: S05 Concentration / S10 Review", "#fef08a", "#ca8a04", 60),
    ("LOW (<30)", "Owner: Automated Sentinel\nSLA: Weekly Audit\nAction: Continuous Audit Scan (S01, S02, S03)", "#bbf7d0", "#16a34a", 81),
]

for title, desc, bg, bd, x in boxes:
    b_rect = patches.FancyBboxPatch((x-9, 16), 18, 28, boxstyle="round,pad=1", fc=bg, ec=bd, lw=1.5)
    ax.add_patch(b_rect)
    ax.text(x, 40, title, ha="center", va="center", weight="bold", color=bd, fontsize=9.5)
    ax.text(x, 28, desc, ha="center", va="center", fontsize=8, color="#1f2937")

# Connector from LLM to Action Layer
ax.annotate("", xy=(50, 56), xytext=(86.5, 68), arrowprops=dict(arrowstyle="->", lw=2.5, color="#7c3aed", connectionstyle="angle,angleA=0,angleB=90,rad=10"))

plt.title("Meridian Home Appliances: End-to-End AI Supply Chain Disruption Architecture", fontsize=13, weight="bold", pad=20)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig1_system_architecture.png"), bbox_inches="tight")
plt.close()

# -------------------------------------------------------------
# 2. Figure 2: Risk Distribution vs Spend at Risk
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
palette = {"Critical": C_CRIT, "High": C_HIGH, "Medium": C_MED, "Low": C_LOW}

sns.scatterplot(
    data=scores,
    x="composite_risk",
    y="annual_spend_inr_lakh",
    hue="risk_band",
    palette=palette,
    size="recent_delay",
    sizes=(80, 500),
    alpha=0.9,
    ax=ax
)

ax.axvline(70, color=C_CRIT, linestyle="--", alpha=0.7, label="Critical Threshold (70)")
ax.axvline(50, color=C_HIGH, linestyle="--", alpha=0.7, label="High Risk Threshold (50)")
ax.axvline(30, color=C_MED, linestyle="--", alpha=0.5, label="Medium Risk Threshold (30)")

# Annotate suppliers
for idx, row in scores.iterrows():
    offset_y = 120 if row["annual_spend_inr_lakh"] < 3000 else -250
    ax.annotate(f"{row['supplier_id']}: {row['short_name']} (₹{row['annual_spend_inr_lakh']:.0f}L)", 
                xy=(row['composite_risk'], row['annual_spend_inr_lakh']),
                xytext=(row['composite_risk'] + 0.9, row['annual_spend_inr_lakh'] + offset_y),
                fontsize=8, weight='bold', color="#1e293b",
                arrowprops=dict(arrowstyle="->", color="#64748b", lw=0.8))

ax.set_title("Meridian Home Appliances: Supplier Risk vs Spend Matrix (₹16,158 Lakhs RM Portfolio)", fontsize=12, weight="bold", pad=12)
ax.set_xlabel("Composite Disruption Risk Score (0 - 100)", fontsize=10.5, weight="bold")
ax.set_ylabel("Annual Raw Material Spend (₹ Lakhs)", fontsize=10.5, weight="bold")
ax.legend(title="Risk Band & Delay Days", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig2_risk_distribution.png"), bbox_inches="tight")
plt.close()

# -------------------------------------------------------------
# 3. Figure 3: Weekly Delivery Delay Trend (Early Warning Deterioration)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 5.5), dpi=300)
trends["week_dt"] = pd.to_datetime(trends["week"])
ax.plot(trends["week_dt"], trends["flagged"], color=C_CRIT, lw=2.8, marker="o", markersize=4, label="Flagged Disrupted Suppliers (S09, S06, S04, S08)")
ax.plot(trends["week_dt"], trends["unflagged"], color=C_BLUE, lw=2, linestyle="-.", marker="s", markersize=3, label="Resilient Normal Suppliers (S01, S02, S03, S05, S07, S10)")

ax.axhline(3.0, color="#64748b", linestyle=":", label="Acceptable Delay Benchmark (3 Days)")
ax.fill_between(trends["week_dt"], trends["unflagged"], trends["flagged"], color=C_CRIT, alpha=0.12)

ax.set_title("Meridian Chakan Plant: 9-Month Inbound Delivery Delay Trajectory (Early Deterioration)", fontsize=12, weight="bold", pad=12)
ax.set_xlabel("Timeline (Weekly Dispatch Batches, Jan - Oct 2026)", fontsize=10.5, weight="bold")
ax.set_ylabel("Average Delivery Delay (Days)", fontsize=10.5, weight="bold")
ax.legend(loc="upper left", frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig3_weekly_delay_trend.png"), bbox_inches="tight")
plt.close()

# -------------------------------------------------------------
# 4. Figure 4: Confusion Matrix & Performance Metrics
# -------------------------------------------------------------
conf = metrics["confusion"]
cm_matrix = np.array([[conf["TN"], conf["FP"]],
                      [conf["FN"], conf["TP"]]])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), gridspec_kw={'width_ratios': [1.1, 1.2]}, dpi=300)

sns.heatmap(cm_matrix, annot=True, fmt="d", cmap="Blues", cbar=False,
            xticklabels=["Predicted Normal", "Predicted Disrupted"],
            yticklabels=["Actual Normal", "Actual Disrupted"], ax=ax1,
            annot_kws={"size": 18, "weight": "bold"})
ax1.set_title("Confusion Matrix (Meridian Ground Truth Audit)", fontsize=11.5, weight="bold")

kpis = [
    ("Disruption Recall", f"{metrics['recall']*100:.1f}%", "All 4 troubled suppliers caught early (Zero missed lines)"),
    ("Precision", f"{metrics['precision']*100:.1f}%", "Zero false alarms across total 10 supplier portfolio"),
    ("F1-Score", f"{metrics['f1']:.3f}", "Optimal harmonic balance between detection & accuracy"),
    ("Overall Accuracy", f"{metrics['accuracy']*100:.1f}%", "10 out of 10 supplier classifications verified"),
    ("Spend at Risk Caught", f"₹ {metrics['spend_at_risk_inr_lakh']:,.1f} L", f"{metrics['spend_at_risk_pct']:.1f}% of ₹ 16,158.0 L total RM spend safeguarded"),
    ("Plant Revenue", f"₹ {metrics['annual_revenue_inr_crore']} Cr", "2,620,700 appliances across 15 products protected")
]

ax2.axis("off")
table_data = [[k[0], k[1], k[2]] for k in kpis]
tbl = ax2.table(cellText=table_data, colLabels=["Evaluation Metric", "Result", "Operational Significance"],
                cellLoc="left", loc="center", colColours=["#e2e8f0", "#bfdbfe", "#e2e8f0"])
tbl.auto_set_font_size(False)
tbl.set_fontsize(8.5)
tbl.scale(1.05, 2.0)
ax2.set_title("Operational Validation Benchmarks", fontsize=11.5, weight="bold", pad=15)

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig4_confusion_matrix.png"), bbox_inches="tight")
plt.close()

# -------------------------------------------------------------
# 5. Figure 5: Inventory Days of Cover vs Supplier Quoted Lead Time
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 5.5), dpi=300)
x_indices = np.arange(len(mat))
bar_width = 0.38

rects1 = ax.bar(x_indices - bar_width/2, mat["days_cover"], bar_width, label="On-Hand Buffer Cover (Days)", color="#ef4444")
rects2 = ax.bar(x_indices + bar_width/2, mat["quoted_lead_time_days"], bar_width, label="Replenishment Lead Time (Days)", color="#3b82f6")

ax.set_xticks(x_indices)
ax.set_xticklabels(mat["material_id"] + "\n(" + mat["short_name"] + ")", fontsize=8, rotation=0)
ax.set_ylabel("Days", fontsize=10.5, weight="bold")
ax.set_title("Meridian Chakan Plant: Stockout Vulnerability (Days of Cover vs Replenishment Lead Time)", fontsize=11.5, weight="bold")
ax.legend(loc="upper right")
ax.axhline(7, color="#dc2626", linestyle=":", label="7-Day Safety Stock Floor")

# Annotate reorder now
for i, row in enumerate(mat.itertuples()):
    if row.status == "REORDER NOW":
        ax.text(i, max(row.days_cover, row.quoted_lead_time_days) + 2.0, "REORDER NOW", ha="center", fontsize=7.5, color="#b91c1c", weight="bold")

plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig5_inventory_cover.png"), bbox_inches="tight")
plt.close()

# -------------------------------------------------------------
# 6. Figure 6: Multi-Dimensional Radar Chart (Critical vs Resilient)
# -------------------------------------------------------------
categories_radar = ['Delivery Risk', 'Inventory Buffer Risk', 'Production Impact Risk', 'Supplier Health Risk']
N = len(categories_radar)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True), dpi=300)

# S09 (Critical: Ahmedabad Coatings)
s09_row = scores[scores['supplier_id'] == 'S09'].iloc[0]
values_s09 = [s09_row['delivery_risk'], s09_row['inventory_risk'], s09_row['production_risk'], s09_row['supplier_risk']]
values_s09 += values_s09[:1]

# S02 (Resilient: Pune Coil Processing)
s02_row = scores[scores['supplier_id'] == 'S02'].iloc[0]
values_s02 = [s02_row['delivery_risk'], s02_row['inventory_risk'], s02_row['production_risk'], s02_row['supplier_risk']]
values_s02 += values_s02[:1]

ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)
plt.xticks(angles[:-1], categories_radar, color="#1e293b", size=9.5, weight="bold")
ax.set_rlabel_position(0)
plt.yticks([20, 40, 60, 80, 100], ["20", "40", "60", "80", "100"], color="#64748b", size=8)
plt.ylim(0, 100)

ax.plot(angles, values_s09, linewidth=2.5, linestyle='solid', color=C_CRIT, label=f'Critical Vendor: S09 Ahmedabad Coatings (Score: {s09_row["composite_risk"]:.1f})')
ax.fill(angles, values_s09, color=C_CRIT, alpha=0.25)

ax.plot(angles, values_s02, linewidth=2, linestyle='solid', color=C_LOW, label=f'Resilient Vendor: S02 Pune Coil Proc. (Score: {s02_row["composite_risk"]:.1f})')
ax.fill(angles, values_s02, color=C_LOW, alpha=0.2)

plt.title("Meridian Supplier Disruption Radar: S09 vs S02 Risk Profiles", size=12, weight="bold", pad=20)
plt.legend(loc='lower right', bbox_to_anchor=(1.25, -0.1))
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig6_radar_chart.png"), bbox_inches="tight")
plt.close()

# -------------------------------------------------------------
# 7. Figure 7: Operational Decision Flowchart
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 8), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

def draw_node(x, y, w, h, text, color, ec):
    box = patches.FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=1.2", fc=color, ec=ec, lw=2)
    ax.add_patch(box)
    ax.text(x, y, text, ha="center", va="center", fontsize=8.5, weight="bold", color="#1e293b")

draw_node(20, 88, 30, 10, "1. INGESTION ENGINE\nTMS (3,200 dlv), WMS (10 SKUs),\nMES (15 Products), ERP (10 Sups)", "#e0f2fe", "#0284c7")
draw_node(65, 88, 30, 10, "2. SIGNAL SYNTHESIZER\n60d Recent vs 120d Baseline\nLead-Time Runway vs Quoted L/T", "#e0f2fe", "#0284c7")

draw_node(65, 68, 32, 12, "3. MULTI-VECTOR RISK ENGINE\nDelivery(35%), Inv(25%), Prod(20%), Sup(20%)\nDynamic Renormalization for Missing Feeds", "#fef3c7", "#d97706")
draw_node(20, 68, 30, 10, "SAFETY OVERRIDE EVALUATOR\nSole Source & Distressed (Score < 65)?\nConcentration >= 20% RM Spend?", "#fee2e2", "#dc2626")

draw_node(20, 42, 30, 10, "4. MERIDIAN BAND CLASSIFICATION\nCritical (>=70) | High (>=50)\nMedium (>=30) | Low (<30)", "#f3e8ff", "#9333ea")
draw_node(65, 42, 32, 10, "5. LLM MITIGATION COPILOT\nRoot-Cause Analysis + Legal Cure Notice\nPO Re-routing & Line Re-sequencing", "#f3e8ff", "#9333ea")

draw_node(65, 16, 32, 12, "6. AUTONOMOUS ERP DISPATCH\nDual-Sourcing PO Shift, VMI Buffer Update,\nExpress Air/Road Freight Conversion", "#dcfce7", "#16a34a")
draw_node(20, 16, 30, 12, "7. SLA ORCHESTRATION\n<24h (Plant Mgr), <3d (Category Lead),\n<2w (SRM Lead), Weekly Sentinel", "#dcfce7", "#16a34a")

# Arrows
ax.annotate("", xy=(50, 88), xytext=(35, 88), arrowprops=dict(arrowstyle="->", lw=2, color="#0369a1"))
ax.annotate("", xy=(65, 74), xytext=(65, 83), arrowprops=dict(arrowstyle="->", lw=2, color="#0369a1"))
ax.annotate("", xy=(35, 68), xytext=(49, 68), arrowprops=dict(arrowstyle="->", lw=2, color="#d97706"))
ax.annotate("", xy=(20, 47), xytext=(20, 63), arrowprops=dict(arrowstyle="->", lw=2, color="#dc2626"))
ax.annotate("", xy=(49, 42), xytext=(35, 42), arrowprops=dict(arrowstyle="->", lw=2, color="#9333ea"))
ax.annotate("", xy=(65, 22), xytext=(65, 37), arrowprops=dict(arrowstyle="->", lw=2, color="#9333ea"))
ax.annotate("", xy=(35, 16), xytext=(49, 16), arrowprops=dict(arrowstyle="->", lw=2, color="#16a34a"))

plt.title("Meridian Chakan Plant: Micro-Level AI Decision Flowchart (Section 4 Flowchart)", fontsize=12, weight="bold", pad=20)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig7_agentic_flowchart.png"), bbox_inches="tight")
plt.close()

print("All 7 publication-quality figures successfully updated for Meridian Home Appliances!")
