
"""Supply Chain Disruption Risk Engine and Mitigation Decision Support.

Case study: Meridian Home Appliances Pvt Ltd
Location: Plant 1, Chakan (Pune), Maharashtra

Pipeline:
Data ingestion -> Feature engineering -> Risk scoring -> Safety overrides
-> Driver diagnostics -> Mitigation routing -> Output generation.

IMPORTANT:
Supplier master and inventory planning inputs are read from Manufacturing_Plant_Model.xlsx.
Delivery/production histories and disruption labels are synthetic case-study data.
Evaluation metrics indicate agreement with supplied synthetic labels only.
They are not evidence of independently validated predictive performance.
"""

import json
import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "output")

os.makedirs(OUT, exist_ok=True)

AS_OF = pd.Timestamp("2026-10-20")

# ================================================================
# 1. BUSINESS RULES AND PARAMETERS
# ================================================================

WEIGHTS = {
    "delivery": 0.35,
    "inventory": 0.25,
    "production": 0.20,
    "supplier": 0.20,
}

BANDS = [
    (70, "Critical"),
    (50, "High"),
    (30, "Medium"),
    (0, "Low"),
]

RECENT_DAYS = 60
BASE_DAYS = 120


def clip01(values):
    """Restrict numeric values to the interval [0, 1]."""
    return np.clip(values, 0, 1)


def band(score):
    """Convert a 0-100 composite score into a risk category."""
    for threshold, name in BANDS:
        if score >= threshold:
            return name
    return "Low"


def safe_mean(series, default=0.0):
    """Return a finite mean, using a default for empty data."""
    if series.empty:
        return float(default)

    value = series.mean()

    if pd.isna(value) or not np.isfinite(value):
        return float(default)

    return float(value)


# ================================================================
# 2. DATA INGESTION AND VALIDATION
# ================================================================

WORKBOOK_PATH = os.path.join(HERE, "Manufacturing_Plant_Model.xlsx")
SUPPLIER_CSV = os.path.join(DATA, "suppliers.csv")
DELIVERY_CSV = os.path.join(DATA, "deliveries.csv")
PRODUCTION_CSV = os.path.join(DATA, "production_orders.csv")

if not os.path.exists(WORKBOOK_PATH):
    raise FileNotFoundError(
        "Manufacturing_Plant_Model.xlsx was not found beside risk_engine.py. "
        "Place the supplied workbook in the project root."
    )

for required_path, label in [
    (SUPPLIER_CSV, "synthetic supplier-label/geo assumptions"),
    (DELIVERY_CSV, "synthetic delivery history"),
    (PRODUCTION_CSV, "synthetic production-order history"),
]:
    if not os.path.exists(required_path):
        raise FileNotFoundError(f"Missing {label}: {required_path}")

# The workbook is the source of truth for supplier master data and inventory.
# Delivery/production histories and the future-disruption labels remain synthetic.
sheet_sup = pd.read_excel(
    WORKBOOK_PATH, sheet_name="Suppliers", header=0, engine="openpyxl"
)
sheet_inv = pd.read_excel(
    WORKBOOK_PATH, sheet_name="Inventory", header=3, engine="openpyxl"
)
sheet_source = pd.read_excel(
    WORKBOOK_PATH, sheet_name="Sourcing", header=0, engine="openpyxl"
)
sheet_materials = pd.read_excel(
    WORKBOOK_PATH, sheet_name="RawMaterials", header=0, engine="openpyxl"
)

sheet_sup = sheet_sup[
    sheet_sup["Supplier ID"].astype(str).str.fullmatch(r"S\d+", na=False)
].copy()
sheet_inv = sheet_inv[
    sheet_inv["RM ID"].astype(str).str.fullmatch(r"RW\d+", na=False)
].copy()
sheet_source = sheet_source[
    sheet_source["RM ID"].astype(str).str.fullmatch(r"RW\d+", na=False)
    & sheet_source["Supplier ID"].astype(str).str.fullmatch(r"S\d+", na=False)
].copy()

# Retain the synthetic future-labels and illustrative geographic-risk assumption
# from the generated case data, joined only by supplier ID.
synthetic_sup = pd.read_csv(SUPPLIER_CSV)
synthetic_label_cols = [c for c in ["supplier_id", "geo_risk", "disrupted_next_30d"]
                        if c in synthetic_sup.columns]
synthetic_labels = synthetic_sup[synthetic_label_cols].drop_duplicates("supplier_id")

sup = pd.DataFrame({
    "supplier_id": sheet_sup["Supplier ID"].astype(str),
    "supplier_name": sheet_sup["Supplier (fictional)"].astype(str),
    "short_name": sheet_sup["Short name"].astype(str),
    "city_state": sheet_sup["City / state"].astype(str),
    "region": sheet_sup["City / state"].astype(str),
    "country": sheet_sup["Country"].astype(str),
    "supplier_type": sheet_sup["Supplier type"].astype(str),
    "annual_spend_inr_lakh": pd.to_numeric(sheet_sup["Annual spend (₹ lakh)"], errors="coerce"),
    "share_of_rm_spend": pd.to_numeric(sheet_sup["Share of RM spend"], errors="coerce"),
    "financial_health_score": pd.to_numeric(sheet_sup["Financial health score (0-100)"], errors="coerce"),
    "is_sole_source": pd.to_numeric(sheet_sup["Sole-source materials (#)"], errors="coerce").fillna(0).gt(0),
    "watch_list_reasons": sheet_sup["Watch-list reasons"].fillna("None").astype(str),
})
sup = sup.merge(synthetic_labels, on="supplier_id", how="left")
# Geography is an illustrative assumption because the workbook does not include
# a numeric geo-risk score. Prefer the existing synthetic case assumption.
sup["geo_risk"] = pd.to_numeric(sup.get("geo_risk"), errors="coerce")
sup["geo_risk"] = sup["geo_risk"].fillna(
    pd.Series(np.where(sup["country"].str.lower().ne("india"), 0.65, 0.15), index=sup.index)
)
sup["disrupted_next_30d"] = pd.to_numeric(
    sup.get("disrupted_next_30d"), errors="coerce"
).fillna(0).astype(int)

# The workbook has one inventory row per raw material. Link each material to
# its primary supplier (or sole supplier) for supplier-level exposure roll-up.
primary_links = sheet_source[
    sheet_source["Role"].astype(str).str.strip().str.lower().isin(["primary", "sole source"])
].drop_duplicates("RM ID", keep="first")[["RM ID", "Supplier ID"]]
inv = sheet_inv.merge(primary_links, on="RM ID", how="left")
inv = inv.rename(columns={
    "RM ID": "material_id",
    "Raw material": "material_name",
    "Std price (₹ / kg)": "std_price_inr_per_kg",
    "On hand (kg)": "on_hand_units",
    "On order (kg)": "on_order_units",
    "Avg daily usage, next 3 months (kg / day)": "avg_daily_usage",
    "Days of cover (on hand)": "days_cover",
    "Days of cover (incl. on order)": "days_cover_total",
    "Weighted lead time (days)": "quoted_lead_time_days",
    "Safety stock (kg)": "safety_stock_units",
    "Reorder point (kg)": "reorder_point_units",
    "Status": "status",
    "Suggested order (kg)": "suggested_order_kg",
    "Suggested order value (₹ lakh)": "suggested_order_lakh",
    "Inventory value (₹ lakh)": "inventory_value_lakh",
    "Annual spend (₹ lakh)": "annual_spend_inr_lakh",
    "ABC class": "abc_class",
    "Supplier ID": "supplier_id",
})
inv["short_name"] = inv["material_name"].astype(str)
material_categories = sheet_materials[["RM ID", "Category"]].drop_duplicates("RM ID")
inv = inv.merge(material_categories, left_on="material_id", right_on="RM ID", how="left")
inv["category"] = inv["Category"].fillna("Unclassified").astype(str)
inv = inv.drop(columns=["RM ID", "Category"], errors="ignore")
inv["primary_supplier_id"] = inv["supplier_id"]
inv["is_sole_source"] = inv["material_id"].isin(
    sheet_source.loc[
        sheet_source["Role"].astype(str).str.strip().str.lower().eq("sole source"), "RM ID"
    ].astype(str)
)

# Delivery and production history are synthetic generated case records.
dlv = pd.read_csv(
    DELIVERY_CSV,
    parse_dates=["order_date", "promised_date", "actual_date"],
)
prd = pd.read_csv(PRODUCTION_CSV, parse_dates=["start_date"])

if sup.empty:
    raise ValueError("The Suppliers sheet contains no supplier records.")
if inv.empty:
    raise ValueError("The Inventory sheet contains no material records.")
if dlv.empty:
    raise ValueError("The synthetic deliveries.csv contains no records.")
if prd.empty:
    raise ValueError("The synthetic production_orders.csv contains no records.")
if sup["supplier_id"].duplicated().any():
    raise ValueError("Duplicate supplier IDs found in the workbook Suppliers sheet.")
if (pd.to_numeric(inv["avg_daily_usage"], errors="coerce") <= 0).any():
    raise ValueError("Workbook inventory average daily usage must be positive.")
if (pd.to_numeric(prd["planned_units"], errors="coerce") <= 0).any():
    raise ValueError("planned_units must be greater than zero.")
if not np.isclose(sum(WEIGHTS.values()), 1.0):
    raise ValueError("Risk weights must sum to 1.0.")

# Save an explicit provenance note alongside generated outputs.
provenance = {
    "supplier_master": "Manufacturing_Plant_Model.xlsx / Suppliers sheet",
    "inventory_master": "Manufacturing_Plant_Model.xlsx / Inventory sheet",
    "sourcing_mapping": "Manufacturing_Plant_Model.xlsx / Sourcing sheet; primary or sole source assigned per material",
    "delivery_history": "Synthetic case-study records in data/deliveries.csv",
    "production_history": "Synthetic case-study records in data/production_orders.csv",
    "future_disruption_labels": "Synthetic labels joined by supplier ID from data/suppliers.csv",
    "geo_risk": "Illustrative numeric assumption; workbook does not provide a numeric geo-risk score",
    "evaluation": "Agreement with supplied synthetic labels only; not independent predictive validation",
}
with open(os.path.join(OUT, "data_provenance.json"), "w", encoding="utf-8") as provenance_file:
    json.dump(provenance, provenance_file, indent=2)

# ================================================================
# 3. DELIVERY RISK FEATURES
# ================================================================

dlv["late"] = (dlv["delay_days"] > 2).astype(int)

recent_cutoff = AS_OF - pd.Timedelta(days=RECENT_DAYS)
baseline_cutoff = AS_OF - pd.Timedelta(
    days=RECENT_DAYS + BASE_DAYS
)

recent = dlv[
    dlv["actual_date"] > recent_cutoff
].copy()

base = dlv[
    (dlv["actual_date"] <= recent_cutoff)
    & (dlv["actual_date"] > baseline_cutoff)
].copy()

supplier_columns = [
    "supplier_id",
    "supplier_name",
    "short_name",
    "city_state",
    "region",
    "country",
    "supplier_type",
    "annual_spend_inr_lakh",
    "share_of_rm_spend",
    "financial_health_score",
    "geo_risk",
    "is_sole_source",
    "disrupted_next_30d",
    "watch_list_reasons",
]

missing_columns = [
    column for column in supplier_columns
    if column not in sup.columns
]

if missing_columns:
    raise ValueError(
        "Missing supplier columns: " + ", ".join(missing_columns)
    )

f = sup[supplier_columns].copy()

recent_features = recent.groupby("supplier_id").agg(
    recent_delay=("delay_days", "mean"),
    recent_late_pct=("late", "mean"),
    recent_defect=("defect_rate", "mean"),
    recent_n=("delivery_id", "count"),
).reset_index()

baseline_features = base.groupby("supplier_id").agg(
    base_delay=("delay_days", "mean"),
    base_defect=("defect_rate", "mean"),
).reset_index()

f = f.merge(
    recent_features,
    on="supplier_id",
    how="left",
)

f = f.merge(
    baseline_features,
    on="supplier_id",
    how="left",
)

delivery_defaults = {
    "recent_delay": 0.0,
    "recent_late_pct": 0.0,
    "recent_defect": 0.0,
    "recent_n": 0,
    "base_delay": 0.0,
    "base_defect": 0.0,
}

f = f.fillna(delivery_defaults)

f["delay_trend"] = f["recent_delay"] - f["base_delay"]

delivery_risk = (
    0.40 * clip01(f["recent_delay"] / 8.0)
    + 0.30 * clip01(f["recent_late_pct"] / 0.65)
    + 0.30 * clip01(
        np.maximum(0, f["delay_trend"]) / 4.5
    )
)

f["delivery_risk"] = np.round(delivery_risk * 100, 1)

# ================================================================
# 4. INVENTORY RISK FEATURES
# ================================================================

inv["days_cover"] = (
    inv["on_hand_units"] / inv["avg_daily_usage"]
)

inv["effective_cover"] = (
    inv["on_hand_units"]
    + inv["on_order_units"] * 0.5
) / inv["avg_daily_usage"]

inv["cover_vs_lead_time"] = (
    inv["days_cover"] / inv["quoted_lead_time_days"]
)

inv["below_safety"] = (
    inv["on_hand_units"] < inv["safety_stock_units"]
).astype(int)

inv["below_reorder"] = (
    inv["status"] == "REORDER NOW"
).astype(int)

inv["inventory_risk"] = np.round(
    100 * (
        0.50 * clip01(
            np.maximum(0, 1.15 - inv["cover_vs_lead_time"])
        )
        + 0.25 * inv["below_safety"]
        + 0.25 * inv["below_reorder"]
    ),
    1,
)

inventory_by_supplier = inv.groupby("supplier_id").agg(
    inventory_risk=("inventory_risk", "max"),
    min_days_cover=("days_cover", "min"),
    n_materials=("material_id", "count"),
    n_below_reorder=("below_reorder", "sum"),
).reset_index()

f = f.merge(
    inventory_by_supplier,
    on="supplier_id",
    how="left",
)

f["inventory_risk"] = f["inventory_risk"].fillna(15.0)
f["min_days_cover"] = f["min_days_cover"].fillna(99.0)
f["n_materials"] = f["n_materials"].fillna(0).astype(int)
f["n_below_reorder"] = (
    f["n_below_reorder"].fillna(0).astype(int)
)

# ================================================================
# 5. PRODUCTION RISK FEATURES
# ================================================================

prd["shortfall"] = (
    1.0 - prd["produced_units"] / prd["planned_units"]
).clip(lower=0)

production_features = prd.groupby("supplier_id").agg(
    prod_delay_rate=("delayed_flag", "mean"),
    avg_shortfall=("shortfall", "mean"),
    prod_orders=("po_id", "count"),
).reset_index()

f = f.merge(
    production_features,
    on="supplier_id",
    how="left",
)

f = f.fillna({
    "prod_delay_rate": 0.08,
    "avg_shortfall": 0.03,
    "prod_orders": 0,
})

f["production_risk"] = np.round(
    100 * (
        0.60 * clip01(f["prod_delay_rate"] / 0.45)
        + 0.40 * clip01(f["avg_shortfall"] / 0.18)
    ),
    1,
)

# ================================================================
# 6. SUPPLIER HEALTH RISK
# ================================================================

f["quality_trend"] = (
    f["recent_defect"] - f["base_defect"]
)

supplier_risk = (
    0.45 * clip01(
        (100.0 - f["financial_health_score"]) / 45.0
    )
    + 0.25 * clip01(f["geo_risk"] / 0.50)
    + 0.15 * f["is_sole_source"].astype(int)
    + 0.15 * clip01(
        np.maximum(0, f["quality_trend"]) / 0.015
    )
)

f["supplier_risk"] = np.round(supplier_risk * 100, 1)

# ================================================================
# 7. COMPOSITE RISK AND SAFETY OVERRIDES
# ================================================================

f["has_inventory"] = (f["n_materials"] > 0).astype(int)
f["has_production"] = (f["prod_orders"] > 0).astype(int)

available = {
    "delivery": f["recent_n"] > 0,
    "inventory": f["has_inventory"] == 1,
    "production": f["has_production"] == 1,
    "supplier": pd.Series(True, index=f.index),
}

numerator = sum(
    WEIGHTS[key]
    * f[f"{key}_risk"]
    * available[key].astype(int)
    for key in WEIGHTS
)

denominator = sum(
    WEIGHTS[key] * available[key].astype(int)
    for key in WEIGHTS
)

f["composite_risk"] = np.round(
    numerator / denominator.replace(0, np.nan)
    if isinstance(denominator, pd.Series)
    else numerator / denominator,
    1,
)

f["composite_risk"] = (
    f["composite_risk"].fillna(f["supplier_risk"])
)

f["signals_available"] = sum(
    available[key].astype(int)
    for key in WEIGHTS
)

# Rule 1: Sole-source supplier with financial distress
# or severe inventory buffer risk receives a Critical floor.
override_sole_critical = (
    f["is_sole_source"].astype(bool)
    & (
        (f["financial_health_score"] < 65)
        | (f["min_days_cover"] < 10)
    )
)

f.loc[
    override_sole_critical & (f["composite_risk"] < 70),
    "composite_risk",
] = 72.5

# Rule 2: Other sole-source suppliers receive a Medium floor.
override_sole_medium = (
    f["is_sole_source"].astype(bool)
    & ~override_sole_critical
)

f.loc[
    override_sole_medium & (f["composite_risk"] < 32),
    "composite_risk",
] = 32.0

# Rule 3: High spend concentration receives a Medium floor.
override_concentration = f["share_of_rm_spend"] >= 0.20

f.loc[
    override_concentration & (f["composite_risk"] < 35),
    "composite_risk",
] = 35.0

f["override_applied"] = (
    override_sole_critical
    | override_sole_medium
    | override_concentration
).astype(int)

f["risk_band"] = f["composite_risk"].apply(band)
f["predicted_flag"] = (f["composite_risk"] >= 50.0).astype(int)

# ================================================================
# 8. DRIVER DIAGNOSTICS AND MITIGATION ROUTING
# ================================================================

def top_driver(row):
    components = {
        key: WEIGHTS[key] * row[f"{key}_risk"]
        for key in WEIGHTS
    }

    if row["has_inventory"] == 0:
        components.pop("inventory", None)

    if row["has_production"] == 0:
        components.pop("production", None)

    return max(components, key=components.get)


f["top_driver"] = f.apply(top_driver, axis=1)

ROUTING = {
    "Critical": (
        "Head of Supply Chain + Plant Operations Manager (Chakan)",
        "Within 24 hours",
    ),
    "High": (
        "Category Procurement Lead (Electrical & Metal)",
        "Within 3 days",
    ),
    "Medium": (
        "Supplier Relationship Manager (SRM)",
        "Within 2 weeks",
    ),
    "Low": (
        "Automated Sentinel Background Monitoring",
        "Weekly Audit Cycle",
    ),
}

PLAYBOOK = {
    "delivery": [
        "Issue a formal delay notice and request an expedited transit plan.",
        "Activate a pre-qualified alternate supplier where approved.",
        "Conduct daily dispatch milestone reviews with the carrier.",
    ],
    "inventory": [
        "Review replenishment requirements against actual lead time.",
        "Prioritise production using available material buffers.",
        "Review safety-stock parameters with the inventory owner.",
    ],
    "production": [
        "Resequence production to protect critical products.",
        "Evaluate additional shifts or overtime subject to approval.",
        "Review subassembly buffers for constrained components.",
    ],
    "supplier": [
        "Begin alternate supplier qualification where necessary.",
        "Review supplier financial and tier-two supply exposure.",
        "Evaluate vendor-managed inventory or local buffer options.",
    ],
}


def build_actions(row):
    driver = row["top_driver"]

    action_count = (
        2 if row["risk_band"] in ("Critical", "High") else 1
    )

    actions = list(PLAYBOOK[driver][:action_count])

    if row["is_sole_source"]:
        actions.append(
            "Sole-source exposure: initiate alternate supplier "
            "qualification and assess transition risks."
        )

    if (
        row["has_inventory"] == 1
        and row["min_days_cover"] < 18
        and row["risk_band"] in ("Critical", "High")
    ):
        actions.append(
            f"Stockout warning: approximately "
            f"{row['min_days_cover']:.0f} days of material cover; "
            "review expedited replenishment."
        )

    if row["supplier_id"] == "S08":
        actions.append(
            "Assess import corridor exposure and evaluate an "
            "approved domestic sourcing alternative."
        )

    if row["supplier_id"] == "S05":
        actions.append(
            "Review spend concentration and assess dual-sourcing "
            "options with qualified suppliers."
        )

    return actions


f["owner"] = f["risk_band"].map(
    lambda value: ROUTING[value][0]
)

f["sla"] = f["risk_band"].map(
    lambda value: ROUTING[value][1]
)

f["recommended_actions"] = f.apply(
    lambda row: (
        " | ".join(build_actions(row))
        if row["risk_band"] != "Low"
        else "Continue monitoring; no immediate escalation indicated."
    ),
    axis=1,
)


def brief(row):
    if row["risk_band"] == "Low":
        return (
            f"{row['supplier_name']} ({row['supplier_id']}) is "
            f"currently classified Low Risk with a composite score "
            f"of {row['composite_risk']:.1f}/100. Continue monitoring."
        )

    cover_description = (
        f"weakest linked material has approximately "
        f"{row['min_days_cover']:.0f} days of cover"
        if row["has_inventory"]
        else "no linked inventory records"
    )

    production_description = (
        f"{row['prod_delay_rate'] * 100:.0f}% of linked production "
        "orders experienced delays"
        if row["has_production"]
        else "no linked production records"
    )

    return (
        f"{row['supplier_name']} ({row['supplier_id']}, "
        f"{row['supplier_type']}, {row['region']}) is classified "
        f"{row['risk_band'].upper()} with a composite score of "
        f"{row['composite_risk']:.1f}/100. Main risk driver: "
        f"{row['top_driver'].upper()}. Recent average delivery "
        f"delay: {row['recent_delay']:.1f} days; change versus "
        f"baseline: {row['delay_trend']:+.1f} days. "
        f"Inventory: {cover_description}. Production: "
        f"{production_description}. Supplier financial health: "
        f"{row['financial_health_score']:.0f}/100. "
        f"Suggested owner: {row['owner']}. SLA target: "
        f"{row['sla']}. Recommended actions: "
        f"{row['recommended_actions']}"
    )


f["agent_brief"] = f.apply(brief, axis=1)

f = f.sort_values(
    "composite_risk",
    ascending=False,
).reset_index(drop=True)

# ================================================================
# 9. SYNTHETIC RULE-ALIGNMENT EVALUATION
# ================================================================
# These labels are generated for this simulated case study.
# The results are descriptive diagnostics, NOT an independent
# model test or evidence of future real-world performance.

y = f["disrupted_next_30d"].astype(int)
yh = f["predicted_flag"].astype(int)

tp = int(((y == 1) & (yh == 1)).sum())
fp = int(((y == 0) & (yh == 1)).sum())
fn = int(((y == 1) & (yh == 0)).sum())
tn = int(((y == 0) & (yh == 0)).sum())

precision = tp / (tp + fp) if (tp + fp) else 0.0
recall = tp / (tp + fn) if (tp + fn) else 0.0

f1 = (
    2 * precision * recall / (precision + recall)
    if (precision + recall)
    else 0.0
)

accuracy = (tp + tn) / len(f) if len(f) else 0.0

spend_at_risk = float(
    f.loc[
        f["risk_band"].isin(["Critical", "High"]),
        "annual_spend_inr_lakh",
    ].sum()
)

total_spend = float(f["annual_spend_inr_lakh"].sum())

flagged_ids = set(
    f.loc[f["predicted_flag"] == 1, "supplier_id"]
)

flagged_recent = recent[
    recent["supplier_id"].isin(flagged_ids)
]["delay_days"]

unflagged_recent = recent[
    ~recent["supplier_id"].isin(flagged_ids)
]["delay_days"]

metrics = {
    "as_of": str(AS_OF.date()),
    "company": "Meridian Home Appliances Pvt Ltd",
    "plant": "Plant 1, Chakan (Pune), Maharashtra",

    "n_suppliers": int(len(f)),
    "n_materials": int(len(inv)),
    "n_products": 15,
    "n_work_centres": 9,
    "n_deliveries": int(len(dlv)),
    "n_production_orders": int(len(prd)),

    # These values are illustrative case-study assumptions.
    # They must not be presented as audited company results.
    "annual_production_units": 2620700,
    "annual_revenue_inr_lakh": 36387.62,
    "annual_revenue_inr_crore": 363.88,
    "total_spend_inr_lakh": round(total_spend, 2),
    "total_spend_inr_crore": 161.58,
    "gross_margin_pct": 29.59,
    "gross_profit_inr_crore": 107.66,

    "band_counts": (
        f["risk_band"]
        .value_counts()
        .reindex(["Critical", "High", "Medium", "Low"])
        .fillna(0)
        .astype(int)
        .to_dict()
    ),

    "confusion": {
        "TP": tp,
        "FP": fp,
        "FN": fn,
        "TN": tn,
    },

    "precision": round(precision, 3),
    "recall": round(recall, 3),
    "f1": round(f1, 3),
    "accuracy": round(accuracy, 3),

    "evaluation_type": "synthetic_rule_alignment",
    "evaluation_status": "not_independently_validated",
    "evaluation_note": (
        "The disruption labels are synthetic. Metrics describe "
        "agreement between rule-based risk classifications and "
        "the supplied labels. They do not establish independently "
        "validated predictive performance or future accuracy."
    ),

    "spend_at_risk_inr_lakh": round(spend_at_risk, 2),
    "spend_at_risk_pct": round(
        spend_at_risk / total_spend * 100,
        1,
    ) if total_spend else 0.0,

    "materials_below_reorder": int(inv["below_reorder"].sum()),
    "materials_below_safety": int(inv["below_safety"].sum()),

    "avg_delay_all_days": round(
        safe_mean(dlv["delay_days"]), 2
    ),
    "avg_delay_recent_days": round(
        safe_mean(recent["delay_days"]), 2
    ),
    "avg_delay_flagged_recent": round(
        safe_mean(flagged_recent), 2
    ),
    "avg_delay_unflagged_recent": round(
        safe_mean(unflagged_recent), 2
    ),

    "weights": WEIGHTS,
}

# ================================================================
# 10. EXPORT OUTPUT FILES
# ================================================================

supplier_columns_to_save = [
    "supplier_id",
    "supplier_name",
    "short_name",
    "city_state",
    "region",
    "country",
    "supplier_type",
    "annual_spend_inr_lakh",
    "share_of_rm_spend",
    "financial_health_score",
    "geo_risk",
    "is_sole_source",
    "recent_delay",
    "recent_late_pct",
    "delay_trend",
    "min_days_cover",
    "n_below_reorder",
    "prod_delay_rate",
    "delivery_risk",
    "inventory_risk",
    "production_risk",
    "supplier_risk",
    "composite_risk",
    "risk_band",
    "top_driver",
    "owner",
    "sla",
    "recommended_actions",
    "agent_brief",
    "override_applied",
    "disrupted_next_30d",
    "predicted_flag",
]

f[supplier_columns_to_save].round(3).to_csv(
    os.path.join(OUT, "supplier_risk_scores.csv"),
    index=False,
)

inv.sort_values(
    "inventory_risk",
    ascending=False,
).round(2).to_csv(
    os.path.join(OUT, "material_risk.csv"),
    index=False,
)

f.loc[
    f["risk_band"] != "Low",
    [
        "supplier_id",
        "supplier_name",
        "risk_band",
        "composite_risk",
        "top_driver",
        "owner",
        "sla",
        "recommended_actions",
    ],
].to_csv(
    os.path.join(OUT, "action_queue.csv"),
    index=False,
)

with open(
    os.path.join(OUT, "metrics.json"),
    "w",
    encoding="utf-8",
) as metrics_file:
    json.dump(metrics, metrics_file, indent=2)

# ================================================================
# 11. WEEKLY DELIVERY DELAY TREND
# ================================================================

dlv["week"] = (
    dlv["actual_date"]
    .dt.to_period("W")
    .dt.start_time
)

dlv["flagged"] = dlv["supplier_id"].isin(flagged_ids)

weekly = (
    dlv.groupby(["week", "flagged"])["delay_days"]
    .mean()
    .unstack()
)

weekly = weekly.rename(
    columns={
        False: "unflagged",
        True: "flagged",
    }
)

for column in ["unflagged", "flagged"]:
    if column not in weekly.columns:
        weekly[column] = np.nan

weekly = weekly[["unflagged", "flagged"]].round(2)

weekly.index = weekly.index.strftime("%Y-%m-%d")

weekly = weekly.ffill().fillna(0.0)

weekly.reset_index().rename(
    columns={"index": "week"}
).to_csv(
    os.path.join(OUT, "weekly_delay_trend.csv"),
    index=False,
)

# ================================================================
# 12. EXECUTION LOG
# ================================================================

run_log_content = (
    json.dumps(metrics, indent=2)
    + "\n\n"
    + f[
        [
            "supplier_id",
            "short_name",
            "composite_risk",
            "risk_band",
            "top_driver",
            "disrupted_next_30d",
            "predicted_flag",
        ]
    ].to_string(index=False)
)

with open(
    os.path.join(HERE, "run_log.txt"),
    "w",
    encoding="utf-8",
) as log_file:
    log_file.write(run_log_content)

print("Supply Chain Risk Engine execution completed.")
print("Evaluation type: synthetic rule alignment.")
print("Independent predictive validation: NOT PERFORMED.")
print(f"Supplier records processed: {len(f)}")
print(f"Action queue records: {(f['risk_band'] != 'Low').sum()}")
print(f"Output directory: {OUT}")
print(run_log_content)
