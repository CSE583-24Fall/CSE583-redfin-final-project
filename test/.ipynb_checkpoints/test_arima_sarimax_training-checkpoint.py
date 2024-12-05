import os
import pytest
import pandas as pd
from src.redfinprediction.arima_sarimax_training import (
    load_and_preprocess_data,
    find_best_order,
    train_arima,
    train_sarimax,
    save_model_to_pickle
)

# Update BASE_PATH to point to repository root
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_PATH, "data/raw")

def test_load_and_preprocess_data():
    """
    Test the `load_and_preprocess_data` function.

    This test ensures that the function correctly loads data from a CSV file and processes it
    into a non-empty pandas DataFrame with the required structure.

    Assertions:
        - The output DataFrame is not empty.
        - The output is an instance of `pandas.DataFrame`.
        - The required column `median_sale_price` is present.
    """
    train_file = os.path.join(DATA_PATH, "train_data.csv")
    df = load_and_preprocess_data(train_file)
    assert not df.empty, "DataFrame is empty"
    assert isinstance(df, pd.DataFrame), "Output should be a pandas DataFrame"
    assert "median_sale_price" in df.columns, "Required column missing"

def test_find_best_order():
    """
    Test the `find_best_order` function.

    This test validates that the function correctly determines the optimal ARIMA order
    and seasonal order (if applicable) for a given time series column.

    Assertions:
        - The ARIMA order is a tuple of length 3.
        - If a seasonal order is returned, it is a tuple of length 4.
        - Handles both seasonal and non-seasonal cases without errors.
    """
    train_file = os.path.join(DATA_PATH, "train_data.csv")
    df = load_and_preprocess_data(train_file)
    result = find_best_order(df, 'median_sale_price')
    if isinstance(result, tuple) and len(result) == 2:
        arima_order, seasonal_order = result
    else:
        arima_order = result
        seasonal_order = None
        
    # Validate ARIMA order
    assert len(arima_order) == 3, "ARIMA order should be a tuple of length 3"
    # Validate seasonal order if it exists
    if seasonal_order is not None:
        assert len(seasonal_order) == 4, "Seasonal order should be a tuple of length 4"
    else:
        print("No seasonal order returned, test passed for non-seasonal case.")

def test_train_arima():
    """
    Test the `train_arima` function.

    This test verifies that the ARIMA model can be trained successfully using the provided data
    and ARIMA order.

    Assertions:
        - The trained ARIMA model is not `None`.
    """
    train_file = os.path.join(DATA_PATH, "train_data.csv")
    df = load_and_preprocess_data(train_file)
    arima_order, _ = find_best_order(df, 'median_sale_price', seasonal=False)
    model = train_arima(df, 'median_sale_price', arima_order)
    assert model is not None, "ARIMA training failed"

def test_train_sarimax():
    """
    Test the `train_sarimax` function.

    This test ensures that the SARIMAX model can be trained successfully using the provided data,
    ARIMA order, and seasonal order.

    Assertions:
        - The trained SARIMAX model is not `None`.
    """
    train_file = os.path.join(DATA_PATH, "train_data.csv")
    df = load_and_preprocess_data(train_file)
    _, seasonal_order = find_best_order(df, 'median_sale_price', seasonal=True, seasonal_period=12)
    model = train_sarimax(df, 'median_sale_price', (1, 1, 1), seasonal_order)
    assert model is not None, "SARIMAX training failed"

def test_save_model_to_pickle(tmp_path):
    """
    Test the `save_model_to_pickle` function.

    This test validates that a model can be successfully serialized and saved to a pickle file.

    Args:
        tmp_path (pathlib.Path): A temporary directory provided by pytest for saving files during tests.

    Assertions:
        - The file is saved to the specified path.
    """
    model = {"test": "value"}
    file_path = tmp_path / "test_model.pkl"
    save_model_to_pickle(model, str(file_path))
    assert file_path.exists(), "Model file was not saved"
