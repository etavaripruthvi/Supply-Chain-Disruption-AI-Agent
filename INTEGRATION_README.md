# IA-3 workbook-integrated supply-chain risk project

## What changed
- `risk_engine.py` now reads supplier master fields from `Manufacturing_Plant_Model.xlsx` → `Suppliers`.
- It reads inventory/reorder/valuation fields from `Manufacturing_Plant_Model.xlsx` → `Inventory`.
- It maps each material to its primary/sole supplier using the workbook's `Sourcing` sheet and material categories from `RawMaterials`.
- `data/deliveries.csv` (3,200 records) and `data/production_orders.csv` (600 records) remain synthetic case-study histories.
- `data/suppliers.csv` is retained only for synthetic future-disruption labels and the illustrative numeric `geo_risk` assumption, because those fields are not directly supplied by the workbook.
- `output/data_provenance.json` records these sources and limitations.
- `app.py` uses the revised violet-theme dashboard code and the Model Audit disclaimer.

## Run
1. Keep `Manufacturing_Plant_Model.xlsx` in the same folder as `risk_engine.py`.
2. Install dependencies in your project environment: `pip install pandas numpy openpyxl streamlit plotly`
3. From this folder run: `python risk_engine.py`
4. Then run: `streamlit run app.py`

## Important interpretation note
The disruption labels and delivery/production histories are synthetic. Precision, recall, F1 and accuracy measure agreement with supplied synthetic labels only. They are not independently validated real-world predictive performance. Cost-avoidance numbers in the report must be presented as estimates unless independently evidenced.

## Validation status
- `risk_engine.py` syntax check: passed.
- `app.py` syntax check: passed.
- Risk engine executed successfully against the included workbook and data; outputs include 10 suppliers, 10 materials, 3,200 synthetic deliveries, 600 synthetic production orders and 6 action-queue entries.
- Streamlit UI runtime was not verified in this environment because Streamlit is not installed here. Run the app in your own environment and inspect each page before submission.
