import os
import pandas as pd
from connectors.fitbit_csv import FitbitCSVConnector
from connectors.openaq_csv import OpenAQCSVConnector

DATA_DIR = 'data'
FITBIT_BASE_PATH = os.path.join(DATA_DIR, 'Fitbit')
OPENAQ_BASE_PATH = os.path.join(DATA_DIR, 'OpenAQ')
OUTPUT_CSV = os.path.join(DATA_DIR, 'merged_data.csv')


def merge_dataframes(dataframes):
    """
    Merge multiple dataframes on the 'date' column using an outer join.
    """
    merged = None
    for df in dataframes:
        if df is None or df.empty:
            continue
        if merged is None:
            merged = df
        else:
            merged = pd.merge(merged, df, on='date', how='outer')
    if merged is not None:
        merged = merged.sort_values('date')
    return merged


def main():
    # Load Fitbit data
    print("[INFO] Loading Fitbit data...")
    fitbit = FitbitCSVConnector(FITBIT_BASE_PATH)
    metric_dfs = fitbit.get_daily_metrics()
    rhr_df = metric_dfs.get('rhr')
    hrv_df = metric_dfs.get('hrv')

    if rhr_df is not None:
        print(f"[INFO] Loaded {len(rhr_df)} days RHR.")
    else:
        print("[WARN] No RHR data loaded.")

    if hrv_df is not None:
        print(f"[INFO] Loaded {len(hrv_df)} days HRV.")
    else:
        print("[WARN] No HRV data loaded.")

    # Load OpenAQ data
    print("[INFO] Loading OpenAQ data...")
    openaq = OpenAQCSVConnector(OPENAQ_BASE_PATH)
    print(f"[DEBUG] Looking for CSVs in: {openaq.data_folder}")
    print(f"[DEBUG] Found CSV paths: {openaq.csv_paths}")
    aq_metrics = openaq.get_daily_metrics()
    aq_df = aq_metrics.get('air_quality')

    if aq_df is not None and not aq_df.empty:
        print(f"[INFO] Loaded {len(aq_df)} days OpenAQ air quality (pm25, o3).")
    else:
        print("[WARN] No OpenAQ air quality data loaded.")

    # Merge all dataframes
    merged = merge_dataframes([rhr_df, hrv_df, aq_df])

    if merged is not None and not merged.empty:
        if os.path.exists(OUTPUT_CSV):
            print(f"[WARN] {OUTPUT_CSV} already exists and will be overwritten.")
        merged.to_csv(OUTPUT_CSV, index=False)
        print(f"[INFO] Merged file written to: {OUTPUT_CSV}")
    else:
        print("[WARN] No data to write! Check your input files.")


if __name__ == "__main__":
    main()