import os
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Utility functions

def load_data_from_file(file_path, separator='\t'):
    """
    Load the data from a local file into a Pandas DataFrame.
    
    Args:
        file_path (str): The path to the input file.
        separator (str): The delimiter used in the file. Default is tab ('\t').
    
    Returns:
        pd.DataFrame: A Pandas DataFrame containing the loaded data.
    
    Raises:
        Exception: If there is an error while loading the file.
    """
    try:
        return pd.read_csv(file_path, sep=separator, on_bad_lines='skip')
    except Exception as e:
        logging.error(f"Error loading file {file_path}: {e}")
        raise

def filter_dataframe_by_date(df, date_column, start_date):
    """
    Filter the DataFrame to keep only rows with a date greater than or equal to the specified start date.
    
    Args:
        df (pd.DataFrame): The input DataFrame.
        date_column (str): The name of the column containing date values.
        start_date (str or datetime-like): The start date to filter rows. Can be a string or datetime object.
    
    Returns:
        pd.DataFrame: A filtered DataFrame containing rows with dates greater than or equal to `start_date`.
    """
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
    filtered_df = df[df[date_column] > start_date]
    filtered_df.dropna(inplace=True)
    return filtered_df

def save_dataframe_to_file(dataframe, output_path):
    """
    Save the cleaned DataFrame to a specified file path in CSV format.
    
    Args:
        dataframe (pd.DataFrame): The DataFrame to save.
        output_path (str): The path where the file should be saved.
    
    Returns:
        str: The path of the saved file.
    
    Raises:
        Exception: If there is an error while saving the DataFrame to the file.
    """
    try:
        dataframe.to_csv(output_path, index=False)
    except Exception as e:
        logging.error(f"Error saving file {output_path}: {e}")
        raise
    return output_path

def save_metadata_to_file(metadata_filename, data_filename, max_period_end_str, output_folder):
    """
    Save metadata (the data filename and the maximum period_end date) to a text file.
    
    Args:
        metadata_filename (str): The name of the metadata file to save.
        data_filename (str): The name of the data file to associate with the metadata.
        max_period_end_str (str): The maximum period_end date (formatted as 'YYYY-MM-DD').
        output_folder (str): The folder where the metadata file will be saved.
    
    Returns:
        str: The path to the saved metadata file.
    
    Raises:
        Exception: If there is an error while saving the metadata file.
    """
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
    """
    Main function to process the initial data run: load, filter, and save the cleaned data and metadata.
    
    Args:
        raw_data_folder (str): The folder containing the raw input data file.
        start_date (str): The date to filter data. Only rows with dates after or equal to this date are kept.
        output_folder (str): The folder to save the cleaned data and metadata files.
    
    Returns:
        None: This function does not return any value, but logs the status and paths of saved files.
    
    Raises:
        Exception: If there are errors in loading data, filtering data, or saving files.
    """
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
