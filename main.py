import os
import glob
import pandas as pd

# ==== CONFIGURABLE BASE PATH ====
FITBIT_BASE_PATH = '/Users/raphael/Downloads/Takeout 2/Fitbit'

# ==== FILE LOCATIONS ====
SLEEP_SCORE_CSV = os.path.join(FITBIT_BASE_PATH, 'Sleep Score', 'sleep_score.csv')
HRV_DIR = os.path.join(FITBIT_BASE_PATH, 'Heart Rate Variability')

# ==== READ RHR DATA ====
def load_rhr(sleep_score_csv):
    df = pd.read_csv(sleep_score_csv)
    df['date'] = pd.to_datetime(df['timestamp']).dt.date.astype(str)
    rhr_df = df[['date', 'resting_heart_rate']].copy()
    return rhr_df

# ==== READ HRV DATA FROM MULTIPLE FILES ====
def load_hrv(hrv_dir):
    # Only pick files starting with the correct prefix
    pattern = os.path.join(hrv_dir, 'Daily Heart Rate Variability Summary*.csv')
    hrv_files = glob.glob(pattern)
    hrv_rows = []
    for file in hrv_files:
        try:
            df = pd.read_csv(file)
            if df.empty:
                continue
            row = df.iloc[0]
            date_str = pd.to_datetime(row['timestamp']).date().isoformat()
            rmssd = row.get('rmssd', None)
            hrv_rows.append({'date': date_str, 'rmssd': rmssd})
        except Exception as e:
            print(f"Warning: Could not read {file}: {e}")
    hrv_df = pd.DataFrame(hrv_rows)
    hrv_df = hrv_df.rename(columns={'rmssd': 'HRV_rmssd'})
    # Keep only the first row per date
    hrv_df = hrv_df.groupby('date', as_index=False).first()
    return hrv_df

# ==== MERGE & OUTPUT ====
def merge_and_save(rhr_df, hrv_df, output_csv='merged_data.csv'):
    merged = pd.merge(rhr_df, hrv_df, on='date', how='outer')
    merged = merged.sort_values('date')
    merged.to_csv(output_csv, index=False)
    print(f"[INFO] Merged file written to: {output_csv}")

def main():
    print("[INFO] Loading Resting Heart Rate data...")
    rhr_df = load_rhr(SLEEP_SCORE_CSV)
    print(f"[INFO] Loaded {len(rhr_df)} days from sleep_score.csv.")

    print("[INFO] Loading HRV (RMSSD) data from daily files...")
    hrv_df = load_hrv(HRV_DIR)
    print(f"[INFO] Loaded {len(hrv_df)} days from HRV summary files.")

    print("[INFO] Merging datasets...")
    merge_and_save(rhr_df, hrv_df)

if __name__ == "__main__":
    main()