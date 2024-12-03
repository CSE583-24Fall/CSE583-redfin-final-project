import os
import pytest
import pandas as pd
import pickle
from unittest.mock import MagicMock
from arima_sarimax.arima_sarimax_eval import (
    load_test_data,
    load_model_from_pickle,
    calculate_metrics,
    evaluate_arima,
    evaluate_sarimax
)

# Update BASE_PATH to point to repository root
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_PATH = os.path.join(BASE_PATH, "data/raw")

def test_load_test_data():
    """
    Test the `load_test_data` function.

    This test verifies that the function correctly loads data from a CSV file and processes it
    into a pandas DataFrame with the required structure.

    Assertions:
        - The output is an instance of `pandas.DataFrame`.
        - The required column `median_sale_price` is present.
    """
    test_file = os.path.join(DATA_PATH, "test_data.csv")
    df = load_test_data(test_file)
    assert isinstance(df, pd.DataFrame), "Output should be a pandas DataFrame"
    assert "median_sale_price" in df.columns, "Required column missing"

def test_load_model_from_pickle(tmp_path):
    """
    Test the `load_model_from_pickle` function.

    This test ensures that a serialized model can be correctly deserialized and matches
    the original model data.

    Args:
        tmp_path (pathlib.Path): A temporary directory provided by pytest for saving files during tests.

    Assertions:
        - The deserialized model matches the original model.
    """
    model = {"test": "value"}
    file_path = tmp_path / "test_model.pkl"
    with open(file_path, "wb") as f:
        pickle.dump(model, f)
    loaded_model = load_model_from_pickle(str(file_path))
    assert loaded_model == model, "Loaded model does not match the saved model"

def test_calculate_metrics():
    """
    Test the `calculate_metrics` function.

    This test validates the correctness of the calculated metrics for given true and predicted values.

    Assertions:
        - The metrics dictionary contains the keys "MAE" and "MSE".
        - The calculated MAE is correct and matches the expected value.
        - The calculated MSE is correct and matches the expected value.
    """
    y_true = pd.Series([100, 200, 300])
    y_pred = pd.Series([110, 190, 290])
    metrics = calculate_metrics(y_true, y_pred)
    assert "MAE" in metrics, "MAE is missing from metrics"
    assert "MSE" in metrics, "MSE is missing from metrics"
    assert metrics["MAE"] == 10, f"Expected MAE to be 10, got {metrics['MAE']}"
    assert metrics["MSE"] == 100, f"Expected MSE to be 100, got {metrics['MSE']}"

def test_evaluate_arima():
    """
    Test the `evaluate_arima` function.

    This test ensures that the ARIMA evaluation function correctly calculates metrics
    for mock predictions and handles data with the expected structure.

    Assertions:
        - The metrics dictionary contains the keys "MAE" and "MSE".
        - The metrics are non-negative.
    """
    # Mock test data
    test_df = pd.DataFrame({
        "median_sale_price": [100, 200, 300],
        "index": pd.date_range("2023-01-01", periods=3, freq="ME"),
    }).set_index("index")
    
    # Mock model
    mock_model = MagicMock()
    mock_model.forecast.return_value = [110, 210, 310]  # Simulate predictions
    
    # Call the function
    metrics = evaluate_arima(test_df, mock_model)
    
    # Assertions
    assert "MAE" in metrics, "MAE is missing from metrics"
    assert "MSE" in metrics, "MSE is missing from metrics"
    assert metrics["MAE"] >= 0, "MAE should be non-negative"
    assert metrics["MSE"] >= 0, "MSE should be non-negative"

def test_evaluate_sarimax():
    """
    Test the `evaluate_sarimax` function.

    This test verifies that the SARIMAX evaluation function correctly calculates metrics
    for mock predictions and handles data with the required structure, including exogenous variables.

    Assertions:
        - The metrics dictionary contains the keys "MAE" and "MSE".
        - The metrics are non-negative.
    """
    # Mock test data
    test_df = pd.DataFrame({
        "demand_supply_ratio": [0.5, 0.6, 0.7],
        "price_drop_ratio": [0.1, 0.2, 0.3],
        "pending_to_sold_ratio": [0.2, 0.3, 0.4],
        "market_heat_index": [0.8, 0.9, 1.0],
        "price_change_vs_inventory": [0.5, 0.6, 0.7],
        "sales_change_vs_supply": [0.3, 0.4, 0.5],
        "median_sale_price": [100, 200, 300],
        "index": pd.date_range("2023-01-01", periods=3, freq="ME"),
    }).set_index("index")
    
    # Mock model
    mock_model = MagicMock()
    mock_model.predict.return_value = [110, 210, 310]  # Simulate predictions
    
    # Call the function
    metrics = evaluate_sarimax(test_df, mock_model)
    
    # Assertions
    assert "MAE" in metrics, "MAE is missing from metrics"
    assert "MSE" in metrics, "MSE is missing from metrics"
    assert metrics["MAE"] >= 0, "MAE should be non-negative"
    assert metrics["MSE"] >= 0, "MSE should be non-negative"