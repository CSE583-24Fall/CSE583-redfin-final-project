import os
import pandas as pd
import pytest
from unittest.mock import patch, mock_open
from redfinprediction.redfindatacleaning import (
    load_data_from_file,
    filter_dataframe_by_date,
    save_dataframe_to_file,
    save_metadata_to_file
)

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'period_end': ['2019-01-01', '2020-01-01', '2021-01-01'],
        'value': [100, 200, 300]
    })

def test_load_data_from_file():
    mock_data = "period_end\tvalue\n2019-01-01\t100\n2020-01-01\t200\n"
    with patch("builtins.open", mock_open(read_data=mock_data)):  #
        df = load_data_from_file("dummy_path.tsv", separator="\t")
        assert not df.empty
        assert len(df) == 2
        assert list(df.columns) == ["period_end", "value"]

def test_filter_dataframe_by_date(sample_data):
    start_date = pd.to_datetime("2020-01-01")
    filtered_df = filter_dataframe_by_date(sample_data, 'period_end', start_date)
    assert len(filtered_df) == 2
    assert filtered_df['period_end'].iloc[0] == pd.Timestamp("2020-01-01")

def test_save_dataframe_to_file(tmp_path, sample_data):
    output_file = tmp_path / "output.csv"  # tmp_path is a built-in pytest fixture that creates a temporary directory for testing file output.
    save_dataframe_to_file(sample_data, output_file)
    assert output_file.exists()

def test_save_metadata_to_file(tmp_path):
    metadata_file = tmp_path / "metadata.txt"
    output_folder = tmp_path
    result_path = save_metadata_to_file(
        "metadata.txt", 
        "datafile.csv", 
        "2021-12-31", 
        output_folder
    )
    assert metadata_file.exists()
    assert result_path == str(metadata_file)
    with open(metadata_file, 'r') as file:
        content = file.read()
    assert content == "datafile.csv\n2021-12-31"


\