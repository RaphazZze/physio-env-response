## 1. Project Title
Analyzing Personal Physiological Response to Montreal Forest Fire Smoke Events

## 2. Current Goal
I am consolidating and aligning my daily Resting Heart Rate (RHR) and Heart Rate Variability (HRV, RMSSD) data from Fitbit CSV exports into a single CSV file, in preparation for future correlation with environmental data.

## 3. Background & Vision
This project aims to explore possible relationships between air pollution from forest fire smoke events in Montreal and changes in my physiological markers, as recorded by Fitbit. Longer term, I want to visualize and understand the health impact of environmental stressors to inform lifestyle or health decisions.

## 4. Tech/Method Stack
- Python (main scripting language)
- pandas (data processing)
- Virtual environment for dependency isolation
- Fitbit data exports: `sleep_score.csv` for RHR, daily HRV summary CSVs for HRV
- VS Code on Mac as IDE

## 5. Key Requirements
- Correct extraction of daily RHR from `/Sleep Score/sleep_score.csv`
- Correct extraction of daily HRV (RMSSD) from `/Heart Rate Variability/Daily Heart Rate Variability Summary*.csv` files (one per day)
- Merge into a single CSV (`merged_data.csv`) with columns: `date`, `resting_heart_rate`, `HRV_rmssd`
- One row per day, including all dates present in either source
- Missing values allowed (leave blank if metric is missing)
- Code should be easy to extend with new metrics later
- Paths are configurable via a variable

## 6. Decisions Made
- Only process HRV files whose names start with `Daily Heart Rate Variability Summary`
- Use the `timestamp` column as the date for both RHR and HRV
- Deduplicate per day (take first value if there are duplicates)
- Output file named `merged_data.csv`
- HRV column is named `HRV_rmssd`
- Virtual environment is used for project dependencies

## 7. Open Questions / Risks
- Air quality/environmental data integration is not yet included
- No data validation on outliers or corrupted rows
- Future extensibility for other physiological or environmental metrics still to be implemented

## 8. Next Actions
- Begin integrating environmental (air quality) data for Montreal smoke events
- Plan for expansion to include other metrics as needed

## 9. Artifacts Generated
- Python script: `main.py` (merges RHR and HRV)
- Output data: `merged_data.csv`
- Virtual environment setup (`venv`), dependencies managed via `pip`
- Sample code snippets for modular data loading and merging

Respond with 'Got it.'