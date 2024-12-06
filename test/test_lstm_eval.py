import os
import pytest
import pandas as pd
import numpy as np
from unittest.mock import MagicMock
from tensorflow.keras.models import Sequential
from src.redfinprediction.lstm_eval import (
    load_test_data,
    load_lstm_model,
    calculate_metrics,
    evaluate_lstm,
)

# Update paths for testing
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_PATH, "data/raw")
MODEL_PATH = os.path.join(BASE_PATH, "src/redfinprediction/test_model.keras")


def test_load_test_data():
    """
    Test the `load_test_data` function.

    This test verifies that the function correctly loads and processes the test data into
    a pandas DataFrame with the required structure.
    """
    test_file = os.path.join(DATA_PATH, "test_data.csv")
    df = load_test_data(test_file)
    assert isinstance(df, pd.DataFrame), "Output should be a pandas DataFrame"
    assert "median_sale_price" in df.columns, "Required column missing"


def test_load_lstm_model(tmp_path):
    """
    Test the `load_lstm_model` function.

    This test ensures that a saved LSTM model can be loaded successfully.

    Args:
        tmp_path (pathlib.Path): Temporary directory for saving a mock model during testing.

    Assertions:
        - The loaded model is a Sequential model.
    """
    # Mock model for testing
    mock_model_path = tmp_path / "test_lstm_model.keras"
    mock_model = Sequential()
    mock_model.save(mock_model_path)

    # Load the mock model
    loaded_model = load_lstm_model(mock_model_path)
    assert isinstance(loaded_model, Sequential), "Loaded model is not a Sequential model"


def test_calculate_metrics():
    """
    Test the `calculate_metrics` function.

    This test validates the correctness of the calculated metrics for given true and predicted values.

    Assertions:
        - Metrics dictionary contains keys "MAE", "MSE", "RMSE", and "MAPE".
        - Calculated metrics match expected values.
    """
    y_true = np.array([100, 200, 300])
    y_pred = np.array([110, 190, 290])
    metrics = calculate_metrics(y_true, y_pred)

    assert "MAE" in metrics, "MAE is missing from metrics"
    assert "MSE" in metrics, "MSE is missing from metrics"
    assert "RMSE" in metrics, "RMSE is missing from metrics"
    assert "MAPE" in metrics, "MAPE is missing from metrics"
    assert metrics["MAE"] == 10, f"Expected MAE to be 10, got {metrics['MAE']}"
    assert metrics["MSE"] == 100, f"Expected MSE to be 100, got {metrics['MSE']}"


def test_evaluate_lstm():
    """
    Test the `evaluate_lstm` function.

    This test ensures that the evaluation function calculates metrics and generates predictions
    correctly when given mock test data and a mock model.
    """
    # Mock test data
    test_df = pd.DataFrame({
        "median_list_price": [300000, 310000, 320000],
        "median_ppsf": [150, 155, 160],
        "median_sale_price_mom": [0.02, 0.03, 0.04],
        "city_freq": [1, 2, 3],
        "property_type_Condo/Co-op": [0, 1, 0],
        "median_list_price_mom": [0.01, 0.02, 0.01],
        "median_ppsf_mom": [0.01, 0.01, 0.01],
        "avg_sale_to_list": [0.98, 0.97, 0.99],
        "inventory": [100, 120, 150],
        "price_change_vs_inventory": [0.5, 0.6, 0.7],
        "market_heat_index": [0.8, 0.9, 1.0],
        "pending_to_sold_ratio": [0.5, 0.6, 0.7],
        "median_sale_price": [305000, 315000, 325000],
    })

    # Mock LSTM model
    mock_model = MagicMock()
    mock_model.predict.return_value = np.array([[310000], [320000], [330000]])

    # Evaluate the mock model
    metrics = evaluate_lstm(test_df, mock_model, output_path=None)

    # Assertions
    assert "MAE" in metrics, "MAE is missing from metrics"
    assert "MSE" in metrics, "MSE is missing from metrics"
    assert metrics["MAE"] >= 0, "MAE should be non-negative"
    assert metrics["MSE"] >= 0, "MSE should be non-negative"
    assert metrics["RMSE"] >= 0, "RMSE should be non-negative"
    assert metrics["MAPE"] >= 0, "MAPE should be non-negative"