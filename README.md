# Meridian Home Appliances — Supply Chain Disruption AI Agent
## Autonomous AI Operations System for Proactive Risk Identification & Mitigation
**Course:** AI Agents & Autonomous Business Operations (MBA IA-3)  
**Problem Statement:** Problem 8 — Supply Chain Disruption Prediction  
**Enterprise Deployment:** Meridian Home Appliances Pvt Ltd · Plant 1, Chakan (Pune), Maharashtra  
**Scale:** 15 Products · 10 Raw Materials · 10 Suppliers · 9 Work Centres · ₹363.9 Cr Revenue  

---

## Quick Execution Guide

1. **Generate Enterprise Operational Data:**
   ```bash
   python generate_data.py
   ```
   *Builds connected relational tables in `data/`: `suppliers.csv`, `inventory.csv`, `deliveries.csv`, `production_orders.csv`, `products.csv`, `sourcing_links.csv`.*

2. **Execute Multi-Vector Risk Engine & Routing:**
   ```bash
   python risk_engine.py
   ```
   *Scores all 10 suppliers, extracts temporal delay trends (60d vs 120d), applies sole-source critical overrides, and outputs to `output/`: `supplier_risk_scores.csv`, `action_queue.csv`, `material_risk.csv`, `metrics.json`, `weekly_delay_trend.csv`.*

3. **Generate Publication-Quality Visualizations:**
   ```bash
   python generate_visuals.py
   python generate_control_tower_diagram.py
   ```
   *Renders Figures 1–8 into `output/figures/`.*

4. **Launch Streamlit Operations Cockpit:**
   ```bash
   streamlit run app.py
   ```
   *Runs the interactive web cockpit on `http://localhost:8501`.*

5. **Capture Verified UI Screenshots:**
   ```bash
   python capture_app_screenshots.py
   ```
   *Uses headless Microsoft Edge to capture full application screenshots into `output/figures/`.*

6. **Compile Master Submission Word Documents (.docx):**
   ```bash
   python build_docx_report.py
   python build_simple_explainer_docx.py
   ```
   *Generates `Supply_Chain_Disruption_AI_Operations_Report.docx` and `Supply_Chain_AI_Simple_Explainer.docx`.*

---

## Key Metrics at a Glance
- **Disruption Recall:** 100.0% (4 out of 4 troubled suppliers caught early)
- **Precision:** 100.0% (Zero false alarms across portfolio)
- **F1-Score:** 1.000 | **Accuracy:** 100.0%
- **Annual RM Spend:** ₹16,158.0 Lakhs (₹161.58 Crore, 44.4% of revenue)
- **Spend at Risk:** ₹4,196.81 Lakhs (₹41.97 Crore, 26.0% of RM spend)
- **Factory Downtime Cost Avoidance:** ₹3.08 Crore ($370,000)
