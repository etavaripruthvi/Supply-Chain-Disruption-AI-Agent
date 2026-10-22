"""Synthetic Manufacturing Supply-Chain Dataset Generator for Meridian Home Appliances Pvt Ltd.

Based on: Plant 1, Chakan (Pune), Maharashtra
15 Products (P01-P15), 10 Raw Materials (RW01-RW10), 10 Suppliers (S01-S10), 9 Work Centres (WC01-WC09).
Course: AI Agents & Autonomous Business Operations (IA-3, Problem 8: Supply Chain Disruption Prediction).
Evaluation Horizon: Snapshot as of 2026-10-20.
"""
import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
os.makedirs(DATA, exist_ok=True)

rng = np.random.default_rng(42)

AS_OF = pd.Timestamp("2026-10-20")
START = pd.Timestamp("2026-01-01")

# ==============================================================================
# 1. SUPPLIERS TABLE (S01 - S10)
# ==============================================================================
suppliers_data = [
    {
        "supplier_id": "S01",
        "supplier_name": "Kalinga Electrical Steels Pvt Ltd",
        "short_name": "Kalinga Steels",
        "city_state": "Rourkela, Odisha",
        "region": "Odisha",
        "country": "India",
        "supplier_type": "Steel mill",
        "certifications": "ISO 9001, ISO 14001, BIS licence",
        "on_time_delivery": 0.910,
        "avg_delay_when_late_days": 4.5,
        "rejection_rate": 0.008,
        "lead_time_std_dev": 4.0,
        "financial_health_score": 84.0,
        "payment_terms_days": 21,
        "materials_supplied": 2,
        "sole_source_materials": 0,
        "avg_lead_time_days": 19.5,
        "annual_spend_inr_lakh": 1540.78,
        "share_of_rm_spend": 0.0954,
        "domestic_import": "Domestic",
        "geo_risk": 0.20,
        "is_sole_source": False,
        "disrupted_next_30d": 0,
        "watch_list_reasons": "None"
    },
    {
        "supplier_id": "S02",
        "supplier_name": "Pune Coil Processing Pvt Ltd",
        "short_name": "Pune Coil Proc.",
        "city_state": "Chakan, Pune, Maharashtra",
        "region": "Maharashtra-West",
        "country": "India",
        "supplier_type": "Steel service centre",
        "certifications": "ISO 9001",
        "on_time_delivery": 0.955,
        "avg_delay_when_late_days": 2.0,
        "rejection_rate": 0.009,
        "lead_time_std_dev": 2.0,
        "financial_health_score": 74.0,
        "payment_terms_days": 45,
        "materials_supplied": 3,
        "sole_source_materials": 0,
        "avg_lead_time_days": 6.33,
        "annual_spend_inr_lakh": 1813.19,
        "share_of_rm_spend": 0.1122,
        "domestic_import": "Domestic",
        "geo_risk": 0.12,
        "is_sole_source": False,
        "disrupted_next_30d": 0,
        "watch_list_reasons": "None"
    },
    {
        "supplier_id": "S03",
        "supplier_name": "Deccan Aluminium Alloys Ltd",
        "short_name": "Deccan Aluminium",
        "city_state": "Hyderabad, Telangana",
        "region": "Telangana",
        "country": "India",
        "supplier_type": "Secondary aluminium smelter",
        "certifications": "ISO 9001, IATF 16949",
        "on_time_delivery": 0.900,
        "avg_delay_when_late_days": 3.5,
        "rejection_rate": 0.014,
        "lead_time_std_dev": 3.0,
        "financial_health_score": 69.0,
        "payment_terms_days": 30,
        "materials_supplied": 1,
        "sole_source_materials": 0,
        "avg_lead_time_days": 10.0,
        "annual_spend_inr_lakh": 1453.50,
        "share_of_rm_spend": 0.0900,
        "domestic_import": "Domestic",
        "geo_risk": 0.18,
        "is_sole_source": False,
        "disrupted_next_30d": 0,
        "watch_list_reasons": "None"
    },
    {
        "supplier_id": "S04",
        "supplier_name": "Bharat Metal Traders",
        "short_name": "Bharat Metal Traders",
        "city_state": "Mumbai, Maharashtra",
        "region": "Maharashtra-West",
        "country": "India",
        "supplier_type": "Metal trader / stockist",
        "certifications": "GST-registered trader",
        "on_time_delivery": 0.930,
        "avg_delay_when_late_days": 2.5,
        "rejection_rate": 0.011,
        "lead_time_std_dev": 2.5,
        "financial_health_score": 61.0,
        "payment_terms_days": 15,
        "materials_supplied": 3,
        "sole_source_materials": 0,
        "avg_lead_time_days": 4.33,
        "annual_spend_inr_lakh": 1417.57,
        "share_of_rm_spend": 0.0877,
        "domestic_import": "Domestic",
        "geo_risk": 0.15,
        "is_sole_source": False,
        "disrupted_next_30d": 1,
        "watch_list_reasons": "Weak financial score"
    },
    {
        "supplier_id": "S05",
        "supplier_name": "Vadodara Winding & Resistance Wires Ltd",
        "short_name": "Vadodara Wires",
        "city_state": "Vadodara, Gujarat",
        "region": "Gujarat",
        "country": "India",
        "supplier_type": "Winding & resistance wire maker",
        "certifications": "ISO 9001, ISO 14001",
        "on_time_delivery": 0.960,
        "avg_delay_when_late_days": 1.5,
        "rejection_rate": 0.003,
        "lead_time_std_dev": 1.5,
        "financial_health_score": 78.0,
        "payment_terms_days": 45,
        "materials_supplied": 2,
        "sole_source_materials": 0,
        "avg_lead_time_days": 13.5,
        "annual_spend_inr_lakh": 5291.39,
        "share_of_rm_spend": 0.3275,
        "domestic_import": "Domestic",
        "geo_risk": 0.15,
        "is_sole_source": False,
        "disrupted_next_30d": 0,
        "watch_list_reasons": "High share of RM spend"
    },
    {
        "supplier_id": "S06",
        "supplier_name": "Coimbatore Magnet Wires Pvt Ltd",
        "short_name": "Coimbatore Magnet",
        "city_state": "Coimbatore, Tamil Nadu",
        "region": "Tamil Nadu",
        "country": "India",
        "supplier_type": "Winding wire maker",
        "certifications": "ISO 9001",
        "on_time_delivery": 0.885,
        "avg_delay_when_late_days": 4.0,
        "rejection_rate": 0.007,
        "lead_time_std_dev": 3.5,
        "financial_health_score": 66.0,
        "payment_terms_days": 45,
        "materials_supplied": 1,
        "sole_source_materials": 0,
        "avg_lead_time_days": 14.0,
        "annual_spend_inr_lakh": 1689.55,
        "share_of_rm_spend": 0.1046,
        "domestic_import": "Domestic",
        "geo_risk": 0.16,
        "is_sole_source": False,
        "disrupted_next_30d": 1,
        "watch_list_reasons": "Low on-time delivery"
    },
    {
        "supplier_id": "S07",
        "supplier_name": "Mumbai Polymer Distribution Co.",
        "short_name": "Mumbai Polymer",
        "city_state": "Navi Mumbai, Maharashtra",
        "region": "Maharashtra-West",
        "country": "India",
        "supplier_type": "Polymer distributor",
        "certifications": "ISO 9001",
        "on_time_delivery": 0.945,
        "avg_delay_when_late_days": 2.0,
        "rejection_rate": 0.004,
        "lead_time_std_dev": 2.0,
        "financial_health_score": 85.0,
        "payment_terms_days": 30,
        "materials_supplied": 2,
        "sole_source_materials": 0,
        "avg_lead_time_days": 6.0,
        "annual_spend_inr_lakh": 1067.00,
        "share_of_rm_spend": 0.0660,
        "domestic_import": "Domestic",
        "geo_risk": 0.12,
        "is_sole_source": False,
        "disrupted_next_30d": 0,
        "watch_list_reasons": "None"
    },
    {
        "supplier_id": "S08",
        "supplier_name": "Pacific Engineering Plastics Co. Ltd",
        "short_name": "Pacific Plastics (TW)",
        "city_state": "Kaohsiung, Taiwan",
        "region": "Taiwan (Import)",
        "country": "Taiwan",
        "supplier_type": "Resin producer (import)",
        "certifications": "ISO 9001, ISO 14001",
        "on_time_delivery": 0.860,
        "avg_delay_when_late_days": 6.5,
        "rejection_rate": 0.005,
        "lead_time_std_dev": 7.0,
        "financial_health_score": 88.0,
        "payment_terms_days": 60,
        "materials_supplied": 2,
        "sole_source_materials": 0,
        "avg_lead_time_days": 38.0,
        "annual_spend_inr_lakh": 775.44,
        "share_of_rm_spend": 0.0480,
        "domestic_import": "Import",
        "geo_risk": 0.50,
        "is_sole_source": False,
        "disrupted_next_30d": 1,
        "watch_list_reasons": "Low on-time delivery; Import / long lead time"
    },
    {
        "supplier_id": "S09",
        "supplier_name": "Ahmedabad Coatings & Powders Pvt Ltd",
        "short_name": "Ahmedabad Coatings",
        "city_state": "Ahmedabad, Gujarat",
        "region": "Gujarat",
        "country": "India",
        "supplier_type": "Powder-coating manufacturer",
        "certifications": "ISO 9001",
        "on_time_delivery": 0.925,
        "avg_delay_when_late_days": 3.0,
        "rejection_rate": 0.006,
        "lead_time_std_dev": 2.5,
        "financial_health_score": 58.0,
        "payment_terms_days": 45,
        "materials_supplied": 1,
        "sole_source_materials": 1,
        "avg_lead_time_days": 9.0,
        "annual_spend_inr_lakh": 314.25,
        "share_of_rm_spend": 0.0194,
        "domestic_import": "Domestic",
        "geo_risk": 0.15,
        "is_sole_source": True,
        "disrupted_next_30d": 1,
        "watch_list_reasons": "Sole source for 1 material(s); Weak financial score"
    },
    {
        "supplier_id": "S10",
        "supplier_name": "Bhiwandi Packaging Industries",
        "short_name": "Bhiwandi Packaging",
        "city_state": "Bhiwandi, Maharashtra",
        "region": "Maharashtra-West",
        "country": "India",
        "supplier_type": "Corrugated carton converter",
        "certifications": "ISO 9001, FSC chain of custody",
        "on_time_delivery": 0.970,
        "avg_delay_when_late_days": 1.0,
        "rejection_rate": 0.009,
        "lead_time_std_dev": 1.0,
        "financial_health_score": 72.0,
        "payment_terms_days": 60,
        "materials_supplied": 1,
        "sole_source_materials": 1,
        "avg_lead_time_days": 6.0,
        "annual_spend_inr_lakh": 795.33,
        "share_of_rm_spend": 0.0492,
        "domestic_import": "Domestic",
        "geo_risk": 0.12,
        "is_sole_source": True,
        "disrupted_next_30d": 0,
        "watch_list_reasons": "Sole source for 1 material(s)"
    }
]
sup_df = pd.DataFrame(suppliers_data)
sup_df.to_csv(os.path.join(DATA, "suppliers.csv"), index=False)

# ==============================================================================
# 2. RAW MATERIALS / INVENTORY TABLE (RW01 - RW10)
# ==============================================================================
inventory_data = [
    {
        "material_id": "RW01",
        "material_name": "CRNGO Electrical Steel Coil",
        "short_name": "CRNGO steel coil",
        "category": "Ferrous metal",
        "primary_supplier_id": "S01",
        "supplier_id": "S01",
        "std_price_inr_per_kg": 93.4,
        "on_hand_units": 80500.0,
        "on_order_units": 20000.0,
        "avg_daily_usage": 2595.6,
        "days_cover": 31.0,
        "days_cover_total": 38.7,
        "quoted_lead_time_days": 16.8,
        "safety_stock_units": 18169.4,
        "reorder_point_units": 61776.0,
        "status": "OK",
        "suggested_order_kg": 0,
        "suggested_order_lakh": 0.0,
        "inventory_value_lakh": 75.19,
        "annual_spend_inr_lakh": 1255.15,
        "abc_class": "A",
        "is_sole_source": False
    },
    {
        "material_id": "RW02",
        "material_name": "CRCA Steel Sheet / Coil",
        "short_name": "CRCA steel sheet",
        "category": "Ferrous metal",
        "primary_supplier_id": "S02",
        "supplier_id": "S02",
        "std_price_inr_per_kg": 66.65,
        "on_hand_units": 71400.0,
        "on_order_units": 0.0,
        "avg_daily_usage": 4465.4,
        "days_cover": 16.0,
        "days_cover_total": 16.0,
        "quoted_lead_time_days": 10.85,
        "safety_stock_units": 31257.9,
        "reorder_point_units": 79707.6,
        "status": "REORDER NOW",
        "suggested_order_kg": 144000,
        "suggested_order_lakh": 95.98,
        "inventory_value_lakh": 47.59,
        "annual_spend_inr_lakh": 1560.28,
        "abc_class": "A",
        "is_sole_source": False
    },
    {
        "material_id": "RW03",
        "material_name": "Aluminium Alloy Ingot (ADC12)",
        "short_name": "Aluminium ADC12",
        "category": "Non-ferrous metal",
        "primary_supplier_id": "S03",
        "supplier_id": "S03",
        "std_price_inr_per_kg": 261.5,
        "on_hand_units": 29200.0,
        "on_order_units": 0.0,
        "avg_daily_usage": 1946.3,
        "days_cover": 15.0,
        "days_cover_total": 15.0,
        "quoted_lead_time_days": 7.9,
        "safety_stock_units": 11678.0,
        "reorder_point_units": 27054.0,
        "status": "WATCH",
        "suggested_order_kg": 0,
        "suggested_order_lakh": 0.0,
        "inventory_value_lakh": 76.36,
        "annual_spend_inr_lakh": 2266.49,
        "abc_class": "A",
        "is_sole_source": False
    },
    {
        "material_id": "RW04",
        "material_name": "Enamelled Copper Winding Wire",
        "short_name": "Copper winding wire",
        "category": "Non-ferrous metal",
        "primary_supplier_id": "S05",
        "supplier_id": "S05",
        "std_price_inr_per_kg": 1336.25,
        "on_hand_units": 13600.0,
        "on_order_units": 9000.0,
        "avg_daily_usage": 971.6,
        "days_cover": 14.0,
        "days_cover_total": 23.3,
        "quoted_lead_time_days": 12.5,
        "safety_stock_units": 6800.9,
        "reorder_point_units": 18945.5,
        "status": "OK",
        "suggested_order_kg": 0,
        "suggested_order_lakh": 0.0,
        "inventory_value_lakh": 181.73,
        "annual_spend_inr_lakh": 6664.66,
        "abc_class": "A",
        "is_sole_source": False
    },
    {
        "material_id": "RW05",
        "material_name": "Polypropylene (PP) Granules",
        "short_name": "PP granules",
        "category": "Polymer",
        "primary_supplier_id": "S07",
        "supplier_id": "S07",
        "std_price_inr_per_kg": 107.0,
        "on_hand_units": 46700.0,
        "on_order_units": 0.0,
        "avg_daily_usage": 1138.9,
        "days_cover": 41.0,
        "days_cover_total": 41.0,
        "quoted_lead_time_days": 12.4,
        "safety_stock_units": 13666.3,
        "reorder_point_units": 27788.2,
        "status": "OK",
        "suggested_order_kg": 0,
        "suggested_order_lakh": 0.0,
        "inventory_value_lakh": 49.97,
        "annual_spend_inr_lakh": 769.40,
        "abc_class": "C",
        "is_sole_source": False
    },
    {
        "material_id": "RW06",
        "material_name": "ABS Granules",
        "short_name": "ABS granules",
        "category": "Polymer",
        "primary_supplier_id": "S08",
        "supplier_id": "S08",
        "std_price_inr_per_kg": 156.0,
        "on_hand_units": 65800.0,
        "on_order_units": 0.0,
        "avg_daily_usage": 1994.7,
        "days_cover": 33.0,
        "days_cover_total": 33.0,
        "quoted_lead_time_days": 25.2,
        "safety_stock_units": 27926.3,
        "reorder_point_units": 78193.5,
        "status": "REORDER NOW",
        "suggested_order_kg": 80000,
        "suggested_order_lakh": 124.80,
        "inventory_value_lakh": 102.65,
        "annual_spend_inr_lakh": 1073.04,
        "abc_class": "A",
        "is_sole_source": False
    },
    {
        "material_id": "RW07",
        "material_name": "Stainless Steel 304 Sheet",
        "short_name": "SS304 sheet",
        "category": "Ferrous metal (stainless)",
        "primary_supplier_id": "S02",
        "supplier_id": "S02",
        "std_price_inr_per_kg": 206.5,
        "on_hand_units": 30600.0,
        "on_order_units": 0.0,
        "avg_daily_usage": 1610.9,
        "days_cover": 19.0,
        "days_cover_total": 19.0,
        "quoted_lead_time_days": 5.2,
        "safety_stock_units": 11276.4,
        "reorder_point_units": 19653.1,
        "status": "OK",
        "suggested_order_kg": 0,
        "suggested_order_lakh": 0.0,
        "inventory_value_lakh": 63.19,
        "annual_spend_inr_lakh": 1000.95,
        "abc_class": "B",
        "is_sole_source": False
    },
    {
        "material_id": "RW08",
        "material_name": "Nichrome Resistance Wire (Ni80/Cr20)",
        "short_name": "Nichrome wire",
        "category": "Alloy",
        "primary_supplier_id": "S05",
        "supplier_id": "S05",
        "std_price_inr_per_kg": 2080.0,
        "on_hand_units": 3750.0,
        "on_order_units": 0.0,
        "avg_daily_usage": 104.0,
        "days_cover": 36.0,
        "days_cover_total": 36.0,
        "quoted_lead_time_days": 12.3,
        "safety_stock_units": 1560.7,
        "reorder_point_units": 2840.5,
        "status": "OK",
        "suggested_order_kg": 0,
        "suggested_order_lakh": 0.0,
        "inventory_value_lakh": 78.00,
        "annual_spend_inr_lakh": 458.43,
        "abc_class": "C",
        "is_sole_source": False
    },
    {
        "material_id": "RW09",
        "material_name": "Powder Coating (Epoxy-Polyester)",
        "short_name": "Powder coating",
        "category": "Coating",
        "primary_supplier_id": "S09",
        "supplier_id": "S09",
        "std_price_inr_per_kg": 345.0,
        "on_hand_units": 4050.0,
        "on_order_units": 0.0,
        "avg_daily_usage": 168.6,
        "days_cover": 24.0,
        "days_cover_total": 24.0,
        "quoted_lead_time_days": 9.0,
        "safety_stock_units": 1686.3,
        "reorder_point_units": 3204.1,
        "status": "OK",
        "suggested_order_kg": 0,
        "suggested_order_lakh": 0.0,
        "inventory_value_lakh": 13.97,
        "annual_spend_inr_lakh": 314.25,
        "abc_class": "C",
        "is_sole_source": True
    },
    {
        "material_id": "RW10",
        "material_name": "Corrugated Board / Cartons",
        "short_name": "Corrugated cartons",
        "category": "Packaging",
        "primary_supplier_id": "S10",
        "supplier_id": "S10",
        "std_price_inr_per_kg": 52.0,
        "on_hand_units": 58200.0,
        "on_order_units": 16000.0,
        "avg_daily_usage": 3421.4,
        "days_cover": 17.0,
        "days_cover_total": 21.7,
        "quoted_lead_time_days": 6.0,
        "safety_stock_units": 23949.7,
        "reorder_point_units": 44478.1,
        "status": "OK",
        "suggested_order_kg": 0,
        "suggested_order_lakh": 0.0,
        "inventory_value_lakh": 30.26,
        "annual_spend_inr_lakh": 795.33,
        "abc_class": "B",
        "is_sole_source": True
    }
]
inv_df = pd.DataFrame(inventory_data)
inv_df.to_csv(os.path.join(DATA, "inventory.csv"), index=False)

# ==============================================================================
# 3. SOURCING LINKS (18 Links)
# ==============================================================================
sourcing_links = [
    ("L01", "RW01", "S01", 0.70, 91.0, 21, 10000, "Rail + road", "Primary"),
    ("L02", "RW01", "S02", 0.30, 99.0, 7, 2000, "Road", "Secondary"),
    ("L03", "RW02", "S02", 0.55, 68.0, 5, 3000, "Road", "Primary"),
    ("L04", "RW02", "S01", 0.45, 65.0, 18, 15000, "Rail + road", "Secondary"),
    ("L05", "RW03", "S03", 0.65, 258.0, 10, 5000, "Road", "Primary"),
    ("L06", "RW03", "S04", 0.35, 268.0, 4, 1000, "Road", "Secondary"),
    ("L07", "RW04", "S05", 0.75, 1330.0, 12, 1000, "Road", "Primary"),
    ("L08", "RW04", "S06", 0.25, 1355.0, 14, 500, "Road", "Secondary"),
    ("L09", "RW05", "S07", 0.80, 108.0, 6, 5000, "Road", "Primary"),
    ("L10", "RW05", "S08", 0.20, 103.0, 38, 20000, "Sea + road", "Secondary"),
    ("L11", "RW06", "S08", 0.60, 152.0, 38, 20000, "Sea + road", "Primary"),
    ("L12", "RW06", "S07", 0.40, 162.0, 6, 2500, "Road", "Secondary"),
    ("L13", "RW07", "S02", 0.55, 202.0, 7, 1000, "Road", "Primary"),
    ("L14", "RW07", "S04", 0.45, 212.0, 3, 500, "Road", "Secondary"),
    ("L15", "RW08", "S05", 0.70, 2050.0, 15, 100, "Road", "Primary"),
    ("L16", "RW08", "S04", 0.30, 2150.0, 6, 50, "Road", "Secondary"),
    ("L17", "RW09", "S09", 1.00, 345.0, 9, 500, "Road", "Sole source"),
    ("L18", "RW10", "S10", 1.00, 52.0, 6, 2000, "Road", "Sole source"),
]
src_df = pd.DataFrame(sourcing_links, columns=[
    "link_id", "material_id", "supplier_id", "share", "price", "lead_time", "moq", "transport", "role"
])
src_df.to_csv(os.path.join(DATA, "sourcing_links.csv"), index=False)

# ==============================================================================
# 4. INBOUND SHIPMENTS / DELIVERIES TABLE (~3,200 Deliveries)
# ==============================================================================
N_DELIVERIES = 3200
dlv_rows = []
sup_lookup = sup_df.set_index("supplier_id")

for i in range(N_DELIVERIES):
    link = src_df.sample(1, weights=src_df["share"]).iloc[0]
    sid = link["supplier_id"]
    mid = link["material_id"]
    s = sup_lookup.loc[sid]
    
    order_days = int(rng.integers(0, (AS_OF - START).days - 35))
    order_date = START + pd.Timedelta(days=order_days)
    promised_lead = int(link["lead_time"])
    promised_date = order_date + pd.Timedelta(days=promised_lead)
    
    is_disrupted = bool(s["disrupted_next_30d"] == 1)
    progress = (order_date - START).days / (AS_OF - START).days
    
    # Base delay distribution anchored to Meridian's supplier performance metrics
    base_mean = s["avg_delay_when_late_days"] * (1 - s["on_time_delivery"])
    delay_std = s["lead_time_std_dev"]
    
    if is_disrupted:
        # For troubled suppliers, delivery delay worsens over time
        if sid == "S08":  # Pacific Plastics Taiwan (Port congestion + transit)
            delay_mean = base_mean + 2.5 + 9.0 * (progress ** 1.8)
        elif sid == "S09":  # Ahmedabad Coatings (Financial liquidity crisis)
            delay_mean = base_mean + 1.5 + 7.5 * progress
        elif sid == "S06":  # Coimbatore Magnet (Enamel oven breakdowns)
            delay_mean = base_mean + 2.0 + 6.0 * progress
        elif sid == "S04":  # Bharat Metal Traders (Credit/trader hold)
            delay_mean = base_mean + 1.0 + 5.5 * progress
        else:
            delay_mean = base_mean + 3.0 * progress
    else:
        delay_mean = max(0.2, base_mean + rng.normal(0, 0.4))
    
    delay_days = max(0, int(round(rng.normal(delay_mean, max(1.0, delay_std * 0.7)))))
    actual_date = promised_date + pd.Timedelta(days=delay_days)
    
    # Quantity ordered
    qty = int(round(link["moq"] * rng.uniform(1.0, 3.5), -2))
    
    # Defect rate
    base_def = s["rejection_rate"]
    defect_rate = max(0.001, rng.normal(base_def * (1.8 if is_disrupted else 1.0), 0.003))
    
    dlv_rows.append((
        f"D{i+1:05d}", sid, mid, link["link_id"], order_date, promised_date, actual_date,
        qty, round(defect_rate, 4), link["transport"], delay_days
    ))

dlv_df = pd.DataFrame(dlv_rows, columns=[
    "delivery_id", "supplier_id", "material_id", "link_id", "order_date", "promised_date",
    "actual_date", "quantity", "defect_rate", "transport_mode", "delay_days"
])
dlv_df.to_csv(os.path.join(DATA, "deliveries.csv"), index=False)

# ==============================================================================
# 5. PRODUCTS & PRODUCTION ORDERS (MES)
# ==============================================================================
products_data = [
    ("P01", "Ceiling Fan 1200 mm - Induction", "Fans & Cooling", "WC06", "FA-1 Fans & coolers", 2010.0, 458500, 9215.85),
    ("P02", "Ceiling Fan 1200 mm - BLDC", "Fans & Cooling", "WC06", "FA-1 Fans & coolers", 2590.0, 145000, 3755.50),
    ("P03", "Pedestal Fan 400 mm", "Fans & Cooling", "WC06", "FA-1 Fans & coolers", 1760.0, 109500, 1927.20),
    ("P04", "Table Fan 400 mm", "Fans & Cooling", "WC06", "FA-1 Fans & coolers", 1215.0, 171000, 2077.65),
    ("P05", "Exhaust Fan 230 mm", "Fans & Cooling", "WC06", "FA-1 Fans & coolers", 710.0, 195000, 1384.50),
    ("P06", "Personal Air Cooler 30 L", "Fans & Cooling", "WC06", "FA-1 Fans & coolers", 2215.0, 78300, 1734.35),
    ("P07", "Mixer Grinder 500 W", "Kitchen Appliances", "WC07", "FA-2 Kitchen", 1555.0, 218500, 3397.68),
    ("P08", "Mixer Grinder 750 W", "Kitchen Appliances", "WC07", "FA-2 Kitchen", 2005.0, 169250, 3393.46),
    ("P09", "Electric Kettle 1.5 L", "Kitchen Appliances", "WC07", "FA-2 Kitchen", 560.0, 266500, 1492.40),
    ("P10", "Induction Cooktop 2000 W", "Kitchen Appliances", "WC07", "FA-2 Kitchen", 1795.0, 133500, 2396.33),
    ("P11", "Sandwich Maker 750 W", "Kitchen Appliances", "WC07", "FA-2 Kitchen", 710.0, 115500, 820.05),
    ("P12", "Fan Room Heater 2000 W", "Heating & Water", "WC08", "FA-3 Heating & pumps", 1100.0, 85250, 937.75),
    ("P13", "Immersion Water Heater Rod 1500 W", "Heating & Water", "WC08", "FA-3 Heating & pumps", 310.0, 180500, 559.55),
    ("P14", "Dry Iron 1000 W", "Heating & Water", "WC08", "FA-3 Heating & pumps", 565.0, 240000, 1356.00),
    ("P15", "Water Pump 0.5 HP Monoblock", "Heating & Water", "WC08", "FA-3 Heating & pumps", 3565.0, 54400, 1939.36),
]
prod_df = pd.DataFrame(products_data, columns=[
    "product_id", "product_name", "family", "wc_id", "final_assembly_line", "selling_price_inr", "annual_units", "annual_revenue_lakh"
])
prod_df.to_csv(os.path.join(DATA, "products.csv"), index=False)

# MES Work Orders (600 Production orders)
N_PO = 600
po_rows = []
for i in range(N_PO):
    p = prod_df.sample(1).iloc[0]
    pid = p["product_id"]
    start_date = START + pd.Timedelta(days=int(rng.integers(0, (AS_OF - START).days)))
    planned_units = int(rng.integers(400, 2500))
    
    # Check if this product depends on high-risk materials (RW06 from S08, RW09 from S09, RW02 from S02)
    # P06, P04, P05, P07, P08 use ABS (RW06, S08)
    # P01, P02, P10 use Powder coating (RW09, S09)
    is_vulnerable = pid in ["P06", "P01", "P02", "P07", "P08", "P10", "P12"]
    
    p_delay = 0.48 if is_vulnerable else 0.12
    delayed = rng.random() < p_delay
    delay_days = int(rng.integers(2, 10)) if delayed else 0
    produced_units = int(planned_units * (rng.uniform(0.72, 0.90) if delayed else rng.uniform(0.97, 1.02)))
    
    # Primary linked supplier for attribution
    if pid in ["P06", "P04", "P08"]:
        linked_sid = "S08"
    elif pid in ["P01", "P02", "P10"]:
        linked_sid = "S09"
    elif pid in ["P07", "P15"]:
        linked_sid = "S05"
    elif pid in ["P12", "P14"]:
        linked_sid = "S04"
    else:
        linked_sid = "S02"
        
    po_rows.append((
        f"PO{i+1:04d}", pid, p["product_name"], p["family"], linked_sid, p["wc_id"],
        start_date, planned_units, produced_units, int(delayed), delay_days
    ))

po_df = pd.DataFrame(po_rows, columns=[
    "po_id", "product_id", "product_name", "family", "supplier_id", "wc_id",
    "start_date", "planned_units", "produced_units", "delayed_flag", "delay_days_production"
])
po_df.to_csv(os.path.join(DATA, "production_orders.csv"), index=False)

print(f"Data Generation for Meridian Home Appliances successfully complete!")
print(f"Suppliers: {sup_df.shape}, Inventory: {inv_df.shape}, Deliveries: {dlv_df.shape}, Production Orders: {po_df.shape}")
print(f"Troubled suppliers planted: {sup_df[sup_df['disrupted_next_30d']==1]['supplier_id'].tolist()}")
