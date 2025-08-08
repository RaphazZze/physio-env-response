### 1. Project Title
Analyzing Personal Physiological Response to Montreal Forest Fire Smoke Events

### 2. Current Goal
Consolidate, align, and merge daily Resting Heart Rate (RHR), Heart Rate Variability (HRV, RMSSD), and PM2.5 & O3 air quality data (from OpenAQ) using a modular connector architecture, in preparation for future correlation with environmental data.

### 3. Background & Vision
This project explores relationships between air pollution from Montreal forest fire smoke events and personal physiological markers, as recorded by Fitbit and local air quality sensors. The long-term aim is to visualize and understand personal health impacts from environmental stressors, supporting informed lifestyle or health decisions.

### 4. Tech/Method Stack
- VS Code on Mac as IDE
- Python (with venv)
- pandas (data processing)
- Modular connectors for scalable data ingestion:
  - `fitbit_csv.py` for Fitbit data
  - `openaq_csv.py` for OpenAQ CSV air quality data

### 5. Key Requirements
- Modular, connector-based data ingestion (`FitbitCSVConnector`, `OpenAQCSVConnector`)
- Automatic ingestion of multiple OpenAQ CSVs (handles multiple months, merges overlaps)
- Aggregates daily mean values for PM2.5 (rounded to 1 decimal) and O3 (rounded to 3 decimals)
- One row per day, including all dates present in any source
- Allow missing values (leave blank if metric is missing)
- Code is easy to extend with new metrics or data sources
- User simply drops standardized export folders under `/data`
- All data input and output files are in the `/data` folder

### 6. Decisions Made
- Connector filenames are short and explicit: `fitbit_csv.py`, `openaq_csv.py`
- Class names reflect data source and type: `FitbitCSVConnector`, `OpenAQCSVConnector`
- Main pipeline (`main.py`) is modular, referencing only the connector’s base path
- Deduplicate per day (take first value if there are duplicates for physiological data; mean for air quality)
- Output file named `merged_data.csv`
- OpenAQ connector processes all `.csv` files in its folder and merges them
- PM2.5 column is named `pm25` (1 decimal), O3 is named `o3` (3 decimals)

### 7. Open Questions / Risks
- Integration of additional environmental data is planned but not yet implemented
- No automated data validation (outliers, corrupted rows, etc.) yet
- Extensibility for additional physiological or environmental metrics is planned

### 8. Next Actions
- Begin integrating other environmental (air quality) data sources or metrics
- Continue extending the connector architecture for additional data sources/metrics

### 9. Artifacts Generated
- Python scripts: `main.py`, `connectors/fitbit_csv.py`, `connectors/openaq_csv.py`
- Output data: `data/merged_data.csv`
