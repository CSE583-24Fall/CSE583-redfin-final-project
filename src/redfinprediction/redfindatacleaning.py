import os
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Utility functions

def load_data_from_file(file_path, separator='\t'):
    """Load the data from a local file into a DataFrame."""
    try:
        return pd.read_csv(file_path, sep=separator, on_bad_lines='skip')
    except Exception as e:
        logging.error(f"Error loading file {file_path}: {e}")
        raise

def filter_dataframe_by_date(df, date_column, start_date):
    """Filter the DataFrame by date, keeping only rows after the start date."""
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
    filtered_df = df[df[date_column] >= start_date]
    filtered_df.dropna(inplace=True)
    return filtered_df

def save_dataframe_to_file(dataframe, output_path):
    """Save the cleaned DataFrame to a local file."""
    try:
        dataframe.to_csv(output_path, index=False)
    except Exception as e:
        logging.error(f"Error saving file {output_path}: {e}")
        raise
    return output_path

def save_metadata_to_file(metadata_filename, data_filename, max_period_end_str, output_folder):
    """Save metadata (filename and max date) to a text file."""
    metadata_content = f"{data_filename}\n{max_period_end_str}"
    metadata_path = os.path.join(output_folder, metadata_filename)
    try:
        with open(metadata_path, 'w') as file:
            file.write(metadata_content)
    except Exception as e:
        logging.error(f"Error saving metadata file {metadata_path}: {e}")
        raise
    return metadata_path


# Main function for the initial run
def process_initial_run(raw_data_folder, start_date, output_folder):
    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Load the data from the raw folder
    raw_file_path = os.path.join(raw_data_folder, "city_market_tracker.tsv")
    df = load_data_from_file(raw_file_path)

    # Filter the data by date
    start_date = pd.to_datetime(start_date)
    filtered_df = filter_dataframe_by_date(df, 'period_end', start_date)

    # Get the maximum period_end date
    max_period_end = filtered_df['period_end'].max()
    max_period_end_str = max_period_end.strftime('%Y-%m-%d')

    # Define output file names
    output_filename = f"city_market_tracker_after_{start_date.strftime('%Y-%m-%d')}_{max_period_end_str}.csv"
    metadata_filename = "initial_run_filename.txt"

    # Save the filtered data and metadata
    output_file_path = os.path.join(output_folder, output_filename)
    metadata_file_path = save_metadata_to_file(metadata_filename, output_filename, max_period_end_str, output_folder)
    save_dataframe_to_file(filtered_df, output_file_path)

    logging.info(f"Initial run completed. Data saved to: {output_file_path}")
    logging.info(f"Metadata saved to: {metadata_file_path}")

# Example usage
if __name__ == "__main__":
    # Define directories and parameters
    raw_data_folder = "../../data/raw"  # Folder where raw data is stored
    start_date = "2019-01-01"  # Date to filter data
    output_folder = "../../data/processed"  # Folder to save cleaned data

    process_initial_run(raw_data_folder, start_date, output_folder)
