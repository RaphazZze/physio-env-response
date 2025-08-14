import os
import glob
import pandas as pd
from functools import reduce


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
        """Read and concatenate all CSVs found in the folder."""
        dfs = []
        for path in self.csv_paths:
            try:
                df = pd.read_csv(path)
                dfs.append(df)
            except Exception as e:
                print(f"Warning: Failed to read {path}: {e}")
        if not dfs:
            return pd.DataFrame()
        return pd.concat(dfs, ignore_index=True)

    def get_daily_means_bulk(self, df, parameters):
        """
        Compute daily mean values for multiple parameters in one go.

        parameters: list of tuples (param_name, decimals)
        """
        daily_dfs = []
        for param, decimals in parameters:
            sub = df[df['parameter'].str.lower() == param].copy()
            if sub.empty:
                daily_dfs.append(pd.DataFrame(columns=['date', param]))
                continue
            sub['date'] = pd.to_datetime(sub['datetimeLocal']).dt.date
            daily = sub.groupby('date', as_index=False)['value'].mean()
            daily[param] = daily['value'].round(decimals)
            daily_dfs.append(daily[['date', param]])

        # Merge all metrics on date
        merged = reduce(lambda left, right: pd.merge(left, right, on='date', how='outer'), daily_dfs)
        return merged.sort_values('date')

    def load_pm25_o3(self):
        """Load and merge PM2.5 and O3 daily means."""
        df_all = self.load_all_data()
        if df_all.empty:
            return pd.DataFrame(columns=['date', 'pm25', 'o3'])
        return self.get_daily_means_bulk(df_all, [('pm25', 1), ('o3', 3)])

    def get_daily_metrics(self):
        """Returns a dict of dataframes keyed by metric group."""
        merged = self.load_pm25_o3()
        return {
            'air_quality': merged
        }