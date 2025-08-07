import os
import pandas as pd

class OpenAQCSVConnector:
    """
    Connector for OpenAQ PM2.5 measurement CSVs.
    Expects:
      {base_path}/OpenAQ Location 8477 Measurements.csv
    Only PM2.5 ("pm25") data is supported for now.
    """
    def __init__(self, base_path):
        self.base_path = base_path
        # For now, hardcoded filename structure
        self.pm25_path = os.path.join(base_path, 'OpenAQ Location 8477 Measurements.csv')

    def load_pm25(self):
        df = pd.read_csv(self.pm25_path)
        # Only keep PM2.5 rows (should be all, but future-proof)
        df = df[df['parameter'].str.lower() == 'pm25']
        # Use 'datetimeLocal' for local date, parse to datetime
        df['date'] = pd.to_datetime(df['datetimeLocal']).dt.date.astype(str)
        # Group by day, aggregate as mean PM2.5 per day, then round to 1 decimal
        pm25_df = df.groupby('date', as_index=False)['value'].mean()
        pm25_df = pm25_df.rename(columns={'value': 'pm25'})
        pm25_df['pm25'] = pm25_df['pm25'].round(1)
        # Deduplicate: mean ensures one row per day
        return pm25_df

    def get_daily_metrics(self):
        """Returns a dict of dataframes keyed by metric name."""
        return {
            'pm25': self.load_pm25()
        }