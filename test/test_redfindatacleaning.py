import os
import pandas as pd
import pytest
import sys

# Add the 'src' directory to sys.path so Python can find the redfinprediction package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from unittest.mock import patch
from redfinprediction.redfindatacleaning import (
    load_data_from_file,
    filter_dataframe_by_date,
    save_dataframe_to_file,
    save_metadata_to_file
)

# Sample data fixture for use in tests
@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'period_end': ['2019-01-01', '2020-01-01', '2021-01-01'],
        'value': [100, 200, 300]
    })

# Test load_data_from_file function
@patch("pandas.read_csv")  # Mock pandas.read_csv instead of open to simulate file reading
def test_load_data_from_file(mock_read_csv):
    """
    Test the load_data_from_file function. This ensures that the function correctly 
    loads a DataFrame from a file, and the expected structure is preserved.
    """
    # Mock data to be returned by read_csv
    mock_df = pd.DataFrame({
        'period_end': ['2019-01-01', '2020-01-01'],
        'value': [100, 200]
    })
    
    # Set the mock to return this DataFrame
    mock_read_csv.return_value = mock_df

    # Simulate calling the function
    df = load_data_from_file("dummy_path.tsv", separator="\t")
    
    # Test the returned DataFrame
    assert not df.empty
    assert len(df) == 2
    assert list(df.columns) == ["period_end", "value"]

# Test filter_dataframe_by_date function
def test_filter_dataframe_by_date(sample_data):
    """
    Test the filter_dataframe_by_date function. This ensures that the function filters 
    the DataFrame correctly based on the provided start date.
    """
    start_date = pd.to_datetime("2020-01-01")
    filtered_df = filter_dataframe_by_date(sample_data, 'period_end', start_date)
    
    # Check if the correct number of rows are returned
    assert len(filtered_df) == 2
    # Ensure the first row's period_end is the expected value
    assert filtered_df['period_end'].iloc[0] == pd.Timestamp("2020-01-01")

# Test save_dataframe_to_file function
def test_save_dataframe_to_file(tmp_path, sample_data):
    """
    Test the save_dataframe_to_file function. This ensures that the DataFrame is 
    saved to the correct path and that the file is created.
    """
    # Use tmp_path to create a temporary file for testing
    output_file = tmp_path / "output.csv"
    
    # Call the function to save the DataFrame
    save_dataframe_to_file(sample_data, output_file)
    
    # Check if the file exists
    assert output_file.exists()

# Test save_metadata_to_file function
def test_save_metadata_to_file(tmp_path):
    """
    Test the save_metadata_to_file function. This ensures that metadata is written 
    to the correct file with the expected content.
    """
    metadata_file = tmp_path / "metadata.txt"
    output_folder = tmp_path
    result_path = save_metadata_to_file(
        "metadata.txt", 
        "datafile.csv", 
        "2021-12-31", 
        output_folder
    )
    
    # Check if the metadata file was created
    assert metadata_file.exists()
    assert result_path == str(metadata_file)
    
    # Check if the content of the file is as expected
    with open(metadata_file, 'r') as file:
        content = file.read()
    assert content == "datafile.csv\n2021-12-31"

