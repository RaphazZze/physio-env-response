import os
import pandas as pd
from connectors.fitbit_connector import FitbitConnector

DATA_DIR = 'data'
FITBIT_BASE_PATH = os.path.join(DATA_DIR, 'Fitbit')
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
    print("[INFO] Loading Fitbit data...")

    fitbit = FitbitConnector(FITBIT_BASE_PATH)
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

    merged = merge_dataframes([rhr_df, hrv_df])

    if merged is not None and not merged.empty:
        merged.to_csv(OUTPUT_CSV, index=False)
        print(f"[INFO] Merged file written to: {OUTPUT_CSV}")
    else:
        print("[WARN] No data to write! Check your input files.")


if __name__ == "__main__":
    main()