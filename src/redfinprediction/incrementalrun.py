import os
import pandas as pd
from datetime import datetime
from redfinprediction.redfindatacleaning import (
    load_data_from_file,
    filter_dataframe_by_date,
    save_dataframe_to_file,
    save_metadata_to_file
)
def load_metadata(metadata_filename, output_folder):
    """
    Load metadata from the file, returning the last processed file and date.

    Args:
        metadata_filename (str): Name of the metadata file.
        output_folder (str): Path to the folder where the metadata file is located.

    Returns:
        tuple: A tuple containing:
            - last_processed_file (str): The name of the last processed file.
            - last_processed_date (str): The last processed date as a string in 'YYYY-MM-DD' format.
    """
    metadata_path = os.path.join(output_folder, metadata_filename)
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as file:
            lines = file.readlines()
            last_processed_file = lines[0].strip()
            last_processed_date = lines[1].strip()
            return last_processed_file, last_processed_date
    else:
        return None, None

def process_incremental_run(raw_data_folder, metadata_filename, output_folder):
    """
    Process incremental data from a raw data file by filtering based on the last processed date.

    Args:
        raw_data_folder (str): Path to the folder containing the raw data.
        metadata_filename (str): Name of the metadata file.
        output_folder (str): Path to the folder where the processed data and metadata should be saved.
    
    Returns:
        None
    """
    # Load metadata (last processed file and date)
    last_processed_file, last_processed_date = load_metadata(metadata_filename, output_folder)
    
    if last_processed_date is None:
        print("Metadata file not found or empty. No previous data found.")
        return

    last_processed_date = pd.to_datetime(last_processed_date)
    raw_file_path = os.path.join(raw_data_folder, "city_market_tracker.tsv")
    
    # Load raw data
    df = load_data_from_file(raw_file_path)

    # Filter data by the last processed date
    filtered_df = filter_dataframe_by_date(df, 'period_end', last_processed_date)
    
    if filtered_df.empty:
        print(f"No new data after {last_processed_date.strftime('%Y-%m-%d')}.")
        return

    max_period_end = filtered_df['period_end'].max()
    max_period_end_str = max_period_end.strftime('%Y-%m-%d')

    # Generate output filename
    output_filename = f"city_market_tracker_incremental_after_{last_processed_date.strftime('%Y-%m-%d')}_{max_period_end_str}.csv"
    output_file_path = os.path.join(output_folder, output_filename)

    # Save filtered data
    save_dataframe_to_file(filtered_df, output_file_path)

    # Update metadata
    save_metadata_to_file(metadata_filename, output_filename, max_period_end_str, output_folder)
    
    print(f"Incremental run completed. Data saved to: {output_file_path}")
    print(f"Metadata updated to: {os.path.join(output_folder, metadata_filename)}")

if __name__ == "__main__":
    # Adjust paths based on your directory structure
    raw_data_folder = "../../data/raw"  
    metadata_filename = "initial_run_filename.txt"  
    output_folder = "../../data/processed"  

    process_incremental_run(raw_data_folder, metadata_filename, output_folder)
