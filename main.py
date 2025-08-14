import os
import logging
from functools import reduce
import pandas as pd
from connectors.fitbit_csv import FitbitCSVConnector
from connectors.openaq_csv import OpenAQCSVConnector

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

DATA_DIR = 'data'
FITBIT_BASE_PATH = os.path.join(DATA_DIR, 'Fitbit')
OPENAQ_BASE_PATH = os.path.join(DATA_DIR, 'OpenAQ')
OUTPUT_CSV = os.path.join(DATA_DIR, 'merged_data.csv')


def merge_dataframes(dataframes):
    """Merge multiple dataframes on 'date' using an outer join."""
    valid_dfs = []
    for df in dataframes:
        if df is not None and not df.empty:
            # Ensure date is datetime.date
            df['date'] = pd.to_datetime(df['date']).dt.date
            valid_dfs.append(df)

    if not valid_dfs:
        return None

    merged = reduce(lambda left, right: pd.merge(left, right, on='date', how='outer'), valid_dfs)
    return merged.sort_values('date')


def main():
    # Load Fitbit data
    logger.info("Loading Fitbit data...")
    fitbit = FitbitCSVConnector(FITBIT_BASE_PATH)
    metric_dfs = fitbit.get_daily_metrics()
    rhr_df = metric_dfs.get('rhr')
    hrv_df = metric_dfs.get('hrv')

    if rhr_df is not None:
        logger.info(f"Loaded {len(rhr_df)} days RHR.")
    else:
        logger.warning("No RHR data loaded.")

    if hrv_df is not None:
        logger.info(f"Loaded {len(hrv_df)} days HRV.")
    else:
        logger.warning("No HRV data loaded.")

    # Load OpenAQ data
    logger.info("Loading OpenAQ data...")
    openaq = OpenAQCSVConnector(OPENAQ_BASE_PATH)
    logger.debug(f"Looking for CSVs in: {openaq.data_folder}")
    logger.debug(f"Found CSV paths: {openaq.csv_paths}")
    aq_metrics = openaq.get_daily_metrics()
    aq_df = aq_metrics.get('air_quality')

    if aq_df is not None and not aq_df.empty:
        logger.info(f"Loaded {len(aq_df)} days OpenAQ air quality (pm25, o3).")
    else:
        logger.warning("No OpenAQ air quality data loaded.")

    # Merge all dataframes
    merged = merge_dataframes([rhr_df, hrv_df, aq_df])

    if merged is not None and not merged.empty:
        # Convert date to string for CSV
        merged['date'] = merged['date'].astype(str)
        if os.path.exists(OUTPUT_CSV):
            logger.warning(f"{OUTPUT_CSV} already exists and will be overwritten.")
        merged.to_csv(OUTPUT_CSV, index=False)
        logger.info(f"Merged file written to: {OUTPUT_CSV}")
    else:
        logger.warning("No data to write! Check your input files.")


if __name__ == "__main__":
    main()