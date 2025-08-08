import os
import glob
import pandas as pd

class OpenAQCSVConnector:
    """
    Connector for OpenAQ air quality measurement CSVs.
    Expects:
      {base_path}/OpenAQ/*.csv
    Supports PM2.5 ("pm25", 1 decimal) and Ozone ("o3", 3 decimals).
    """

    def __init__(self, base_path):
        self.base_path = base_path
        self.data_folder = base_path  # Already points to data/OpenAQ
        self.csv_paths = glob.glob(os.path.join(self.data_folder, '*.csv'))

    def load_all_data(self):
        # Read and concatenate all CSVs
        dfs = []
        for path in self.csv_paths:
            try:
                df = pd.read_csv(path)
                dfs.append(df)
            except Exception as e:
                print(f"Warning: Failed to read {path}: {e}")
        if not dfs:
            return pd.DataFrame()  # Empty if no data
        df_all = pd.concat(dfs, ignore_index=True)
        return df_all

    def get_daily_means(self, df, parameter, decimals):
        sub = df[df['parameter'].str.lower() == parameter].copy()
        if sub.empty:
            return pd.DataFrame(columns=['date', parameter])
        sub['date'] = pd.to_datetime(sub['datetimeLocal']).dt.date.astype(str)
        daily = sub.groupby('date', as_index=False)['value'].mean()
        daily[parameter] = daily['value'].round(decimals)
        return daily[['date', parameter]]

    def load_pm25_o3(self):
        df_all = self.load_all_data()
        if df_all.empty:
            # Return empty DataFrame with expected columns
            return pd.DataFrame(columns=['date', 'pm25', 'o3'])

        pm25_daily = self.get_daily_means(df_all, 'pm25', 1)
        o3_daily = self.get_daily_means(df_all, 'o3', 3)

        # Outer join on date so all days appear
        merged = pd.merge(pm25_daily, o3_daily, on='date', how='outer', sort=True)
        merged = merged.sort_values('date')
        return merged

    def get_daily_metrics(self):
        """Returns a dict of dataframes keyed by metric group."""
        merged = self.load_pm25_o3()
        return {
            'air_quality': merged
        }