import sys
import os
import pytest
import pandas as pd
from unittest.mock import patch

# Dynamically add the 'src' directory to sys.path to import from the redfinprediction package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Import functions to be tested
from redfinprediction.incrementalrun import process_incremental_run, load_metadata
from redfinprediction.redfindatacleaning import (
    load_data_from_file,
    filter_dataframe_by_date,
    save_dataframe_to_file,
    save_metadata_to_file
)

@pytest.fixture
def mock_metadata():
    """
    Fixture for creating mock metadata.

    Returns:
        tuple: A tuple containing:
            - str: The name of the last processed file.
            - str: The last processed date in 'YYYY-MM-DD' format.
    """
    return "test_file.tsv", "2024-12-01"

@pytest.fixture
def mock_dataframe():
    """
    Fixture for creating a mock DataFrame for testing.

    Returns:
        pd.DataFrame: A DataFrame containing sample 'period_end' dates and corresponding 'value'.
    """
    data = {
        'period_end': pd.to_datetime(['2024-12-02', '2024-12-03']),
        'value': [100, 200]
    }
    return pd.DataFrame(data)

@patch("redfinprediction.incrementalrun.load_data_from_file")
@patch("redfinprediction.incrementalrun.filter_dataframe_by_date")
@patch("redfinprediction.incrementalrun.save_dataframe_to_file")
@patch("redfinprediction.incrementalrun.save_metadata_to_file")
def test_process_incremental_run(mock_save_metadata, mock_save_dataframe, mock_filter_df, mock_load_data, mock_metadata, mock_dataframe, tmp_path):
    """
    Test the process_incremental_run function with mock dependencies.

    Args:
        mock_save_metadata (Mock): Mock object for the save_metadata_to_file function.
        mock_save_dataframe (Mock): Mock object for the save_dataframe_to_file function.
        mock_filter_df (Mock): Mock object for the filter_dataframe_by_date function.
        mock_load_data (Mock): Mock object for the load_data_from_file function.
        mock_metadata (tuple): Fixture containing mock metadata (file name and date).
        mock_dataframe (pd.DataFrame): Fixture containing a mock DataFrame.
        tmp_path (pathlib.Path): Temporary path provided by pytest for file operations.

    Asserts:
        - Verifies the incremental processing logic and ensures filtered data is saved.
        - Ensures that metadata is updated correctly.
    """
    raw_data_folder = tmp_path / "raw"
    output_folder = tmp_path / "processed"
    metadata_filename = "test_metadata.txt"

    # Create mock file structure
    raw_data_folder.mkdir(parents=True)
    output_folder.mkdir(parents=True)

    # Mock metadata file content
    metadata_path = output_folder / metadata_filename
    with open(metadata_path, 'w') as f:
        f.write(f"{mock_metadata[0]}\n{mock_metadata[1]}\n")

    # Mock behavior for data loading and filtering
    mock_load_data.return_value = mock_dataframe
    mock_filter_df.return_value = mock_dataframe
    
    # This is the file name that will be generated
    expected_output_filename = f"city_market_tracker_incremental_after_2024-12-01_2024-12-03.csv"
    expected_output_file_path = output_folder / expected_output_filename

    # Mock the save function to simulate the file creation without actually writing
    mock_save_dataframe.return_value = None  # Simulate a successful save without actual file IO
    mock_save_metadata.return_value = None  # Simulate a successful metadata save

    # Run the function
    process_incremental_run(str(raw_data_folder), metadata_filename, str(output_folder))

    # Check function calls and output
    mock_load_data.assert_called_once()
    mock_filter_df.assert_called_once_with(mock_dataframe, 'period_end', pd.Timestamp(mock_metadata[1]))
    mock_save_dataframe.assert_called_once()  # Verify that saving the dataframe was called
    mock_save_metadata.assert_called_once()  # Verify that saving metadata was called

    # Check that the mock save function was called to create the expected file
    mock_save_dataframe.assert_called_with(mock_dataframe, str(expected_output_file_path))
    
    # Since we are mocking, we won't find the file, but we ensure the function is called with the right path.
    # Just ensure the mock was called correctly.
    mock_save_dataframe.assert_called_once_with(mock_dataframe, str(expected_output_file_path))

    # Optionally, check if the content of the saved file is as expected:
    # This part can be skipped, as we are mocking the save operation, not the actual file content
    # saved_file_path = expected_output_file_path
    # if os.path.exists(saved_file_path):
    #     with open(saved_file_path, 'r') as f:
    #         print(f"Saved file content:\n{f.read()}")


def test_load_metadata(tmp_path):
    """
    Test the load_metadata function to ensure it correctly reads metadata from a file.

    Args:
        tmp_path (pathlib.Path): Temporary path provided by pytest for file operations.

    Asserts:
        - Checks that the metadata file is correctly read and parsed.
        - Ensures the returned values match the expected metadata.
    """
    metadata_filename = "test_metadata.txt"
    output_folder = tmp_path / "processed"
    output_folder.mkdir(parents=True)

    metadata_path = output_folder / metadata_filename
    metadata_content = "test_file.tsv\n2024-12-01\n"
    
    with open(metadata_path, 'w') as file:
        file.write(metadata_content)

    last_processed_file, last_processed_date = load_metadata(metadata_filename, str(output_folder))

    assert last_processed_file == "test_file.tsv"
    assert last_processed_date == "2024-12-01"
