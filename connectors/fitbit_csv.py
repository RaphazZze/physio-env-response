import os
import glob
import pandas as pd

class FitbitCSVConnector:
    """
    Connector for standardized Fitbit export folders.
    Expects:
      {base_path}/Sleep Score/sleep_score.csv
      {base_path}/Heart Rate Variability/Daily Heart Rate Variability Summary*.csv
    """
    def __init__(self, base_path):
        self.base_path = base_path
        self.sleep_score_path = os.path.join(base_path, 'Sleep Score', 'sleep_score.csv')
        self.hrv_dir = os.path.join(base_path, 'Heart Rate Variability')

    def load_rhr(self):
        """Load daily Resting Heart Rate (RHR) as datetime.date."""
        df = pd.read_csv(self.sleep_score_path)
        df['date'] = pd.to_datetime(df['timestamp']).dt.date  # datetime.date, not str
        rhr_df = df[['date', 'resting_heart_rate']].copy()
        # Deduplicate: keep first per day
        rhr_df = rhr_df.groupby('date', as_index=False).first()
        return rhr_df

    def load_hrv(self):
        """Load daily Heart Rate Variability (RMSSD) as datetime.date."""
        pattern = os.path.join(self.hrv_dir, 'Daily Heart Rate Variability Summary*.csv')
        hrv_files = glob.glob(pattern)
        hrv_rows = []
        for file in hrv_files:
            try:
                df = pd.read_csv(file)
                if df.empty:
                    continue
                row = df.iloc[0]
                date_val = pd.to_datetime(row['timestamp']).date()
                rmssd = row.get('rmssd', None)
                hrv_rows.append({'date': date_val, 'HRV_rmssd': rmssd})
            except Exception as e:
                print(f"Warning: Could not read {file}: {e}")
        hrv_df = pd.DataFrame(hrv_rows)
        # Deduplicate: keep first per day
        hrv_df = hrv_df.groupby('date', as_index=False).first()
        return hrv_df

    def get_daily_metrics(self):
        """Returns a dict of dataframes keyed by metric name."""
        return {
            'rhr': self.load_rhr(),
            'hrv': self.load_hrv()
        }