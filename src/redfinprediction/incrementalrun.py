import os
import pandas as pd
from datetime import datetime
from redfindatacleaning import load_data_from_file, filter_dataframe_by_date, save_dataframe_to_file, save_metadata_to_file

def load_metadata(metadata_filename, output_folder):
    """Load metadata from the file, returning the last processed file and date."""
    metadata_path = os.path.join(output_folder, metadata_filename)
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as file:
            lines = file.readlines()
            last_processed_file = lines[0].strip()  # Extract the last processed file name
            last_processed_date = lines[1].strip()  # Extract the last processed date
            return last_processed_file, last_processed_date
    else:
        # If metadata file doesn't exist, return None for both values
        return None, None

# Incremental loading function
def process_incremental_run(raw_data_folder, metadata_filename, output_folder):
    # Load metadata (last processed file and date)
    last_processed_file, last_processed_date = load_metadata(metadata_filename, output_folder)
    
    # If there's no metadata or the file is empty, start from the beginning
    if last_processed_date is None:
        print("Metadata file not found or empty. No previous data found.")
        return

    # Convert the last processed date to a datetime object
    last_processed_date = pd.to_datetime(last_processed_date)

    # Find the raw data file that contains data after the last processed date
    raw_file_path = os.path.join(raw_data_folder, "city_market_tracker.tsv")
    df = load_data_from_file(raw_file_path)
    
    # Filter the data by the last processed date
    filtered_df = filter_dataframe_by_date(df, 'period_end', last_processed_date)
    
    # If there's no new data to process, notify and exit
    if filtered_df.empty:
        print(f"No new data after {last_processed_date.strftime('%Y-%m-%d')}.")
        return

    # Get the maximum period_end date for the new data
    max_period_end = filtered_df['period_end'].max()
    max_period_end_str = max_period_end.strftime('%Y-%m-%d')

    # Define the output file name for incremental data
    output_filename = f"city_market_tracker_incremental_after_{last_processed_date.strftime('%Y-%m-%d')}_{max_period_end_str}.csv"
    
    # Save the filtered data
    output_file_path = os.path.join(output_folder, output_filename)
    save_dataframe_to_file(filtered_df, output_file_path)
    
    # Update the metadata with the new filename and the latest period_end date
    save_metadata_to_file(metadata_filename, output_filename, max_period_end_str, output_folder)
    
    print(f"Incremental run completed. Data saved to: {output_file_path}")
    print(f"Metadata updated to: {os.path.join(output_folder, metadata_filename)}")

# Example usage
if __name__ == "__main__":
    # Define directories and parameters
    raw_data_folder = "../../data/raw"  # Folder where raw data is stored
    metadata_filename = "../../data/processed/initial_run_filename.txt"  # Metadata file from the initial run
    output_folder = "../../data/processed"  # Folder to save cleaned data

    process_incremental_run(raw_data_folder, metadata_filename, output_folder)
