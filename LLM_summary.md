### 1. Project Title
Analyzing Personal Physiological Response to Montreal Forest Fire Smoke Events

### 2. Current Goal
Align and merge daily Resting Heart Rate (RHR), Heart Rate Variability (HRV, RMSSD), and PM2.5 & O3 air quality data into a single dataset, using modular connectors. Ensure consistent date handling and extensible architecture for adding new metrics.

### 3. Background & Vision
The project investigates links between air pollution from Montreal forest fire smoke events and personal physiological markers recorded by Fitbit and local air quality sensors. Long-term, it aims to visualize and understand personal health impacts from environmental stressors to support informed lifestyle and health decisions.

### 4. Tech/Method Stack
- VS Code on Mac as IDE
- Python (with venv)
- pandas (data processing)
- Modular connector architecture:
  - `fitbit_csv.py` for Fitbit data
  - `openaq_csv.py` for OpenAQ CSV air quality data
- Logging for process feedback

### 5. Key Requirements
- Modular, connector-based ingestion
- Automatic ingestion of multiple OpenAQ CSVs (handles multiple months, merges overlaps)
- Aggregates daily mean values for PM2.5 (1 decimal) and O3 (3 decimals)
- One row per day, including all dates present in any source
- Allow missing values (leave blank if metric is missing)
- Consistent `datetime.date` type for date columns
- Easy to extend with new metrics or data sources
- User drops standardized export folders under `/data`
- All input and output files in `/data` folder
- Output file: `merged_data.csv`

### 6. Decisions Made
- DRY aggregation for OpenAQ metrics using a bulk daily means function
- Unified date handling across connectors (`datetime.date`)
- Merge logic enforces date normalization
- Outer join ensures all dates from all sources are preserved
- Logging module replaces print statements for better control
- Deduplicate per day (first value for physiological data; mean for air quality)

### 7. Open Questions / Risks
- Integration of additional environmental data is planned but not yet implemented
- No automated data validation (outliers, corrupted rows, etc.) yet
- Extensibility for additional physiological or environmental metrics is planned

### 8. Next Actions
- Integrate GI flareups data (e.g., 2025-08-08)
- Prepare visualization layer for merged dataset
- Add unit tests for connectors

### 9. Artifacts Generated
- Python scripts: `main.py`, `connectors/fitbit_csv.py`, `connectors/openaq_csv.py`
- Output data: `data/merged_data.csv`