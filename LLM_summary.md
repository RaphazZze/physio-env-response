### 1. Project Title
Analyzing Personal Physiological Response to Montreal Forest Fire Smoke Events

### 2. Current Goal
Consolidate, align, and merge daily Resting Heart Rate (RHR) and Heart Rate Variability (HRV, RMSSD) data from Fitbit CSV exports using a modular connector architecture, in preparation for future correlation with environmental data.

### 3. Background & Vision
This project explores relationships between air pollution from Montreal forest fire smoke events and personal physiological markers, as recorded by Fitbit. Long-term, the aim is to visualize and understand personal health impacts from environmental stressors, supporting informed lifestyle or health decisions.

### 4. Tech/Method Stack
- VS Code on Mac as IDE
- Python (with venv)
- pandas (data processing)
- Modular connectors (starting with Fitbit) for scalable data ingestion
- Fitbit data exports: `sleep_score.csv` for RHR, daily HRV summary CSVs for HRV

### 5. Key Requirements
- Modular, connector-based data ingestion (FitbitConnector)
- Merge into single CSV (`merged_data.csv`) with columns: `date`, `resting_heart_rate`, `HRV_rmssd`
- One row per day, including all dates present in either source
- Allow missing values (leave blank if metric is missing)
- Code is easy to extend with new metrics or data sources
- User simply drops the standardized Fitbit export folder under `/data`
- All data input and output files are in the `/data` folder

### 6. Decisions Made
- Introduced a `connectors/fitbit_connector.py` module encapsulating all Fitbit-specific subpaths and logic
- Main pipeline (`main.py`) is modular, referencing only the connector’s base path
- Deduplicate per day (take first value if there are duplicates)
- Output file named `merged_data.csv`
- HRV column is named `HRV_rmssd`

### 7. Open Questions / Risks
- Integration of air quality/environmental data is planned but not yet implemented
- No automated data validation (outliers, corrupted rows, etc.) yet
- Extensibility for additional physiological or environmental metrics is planned

### 8. Next Actions
- Begin integrating environmental (air quality) data for Montreal smoke events
- Continue extending the connector architecture for additional data sources/metrics

### 9. Artifacts Generated
- Python scripts: `main.py`, `connectors/fitbit_connector.py`
- Output data: `data/merged_data.csv`