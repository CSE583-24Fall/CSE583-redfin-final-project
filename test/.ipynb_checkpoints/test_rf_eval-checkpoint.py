import os
import pytest
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from src.redfinprediction.rf_eval import (
    load_test_data,
    load_rf_model,
    calculate_metrics,
    evaluate_rf,
    main
)

# Paths for testing
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_PATH, "data/raw")
MODEL_PATH = os.path.join(BASE_PATH, "src/redfinprediction/test_RF_model.pkl")
RESULT_PATH = os.path.join(BASE_PATH, "data/machinelearningresults")

def test_load_test_data():
    """
    Test the `load_test_data` function.

    Verifies that the test data is loaded as a DataFrame and contains required columns.
    """
    test_file = os.path.join(DATA_PATH, "test_data.csv")
    df = load_test_data(test_file)

    assert isinstance(df, pd.DataFrame), "Output should be a pandas DataFrame"
    assert "median_sale_price" in df.columns, "Required column `median_sale_price` missing"
    assert not df.empty, "DataFrame is empty"

def test_load_rf_model(tmp_path):
    """
    Test the `load_rf_model` function.

    Validates that a Random Forest model can be correctly loaded from a saved joblib file.
    """
    model = RandomForestRegressor()
    file_path = tmp_path / "test_RF_model.pkl"
    
    # Save the model to a temporary file
    import joblib
    joblib.dump(model, file_path)

    # Load the model
    loaded_model = load_rf_model(str(file_path))
    assert loaded_model is not None, "Model loading failed"
    assert isinstance(loaded_model, RandomForestRegressor), "Loaded model is not a Random Forest Regressor"

def test_calculate_metrics():
    """
    Test the `calculate_metrics` function.

    Validates the correctness of calculated metrics for given true and predicted values.
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

def test_evaluate_rf(tmp_path):
    """
    Test the `evaluate_rf` function.

    Validates that the evaluation process generates metrics and saves predictions to a CSV file.
    """
    # Mock test data
    test_df = pd.DataFrame({
        "median_list_price": [100, 200, 300],
        "median_ppsf": [110, 210, 310],
        "median_sale_price_mom": [1, 2, 3],
        "city_freq": [10, 20, 30],
        "property_type_Condo/Co-op": [0, 1, 0],
        "median_list_price_mom": [0.1, 0.2, 0.3],
        "median_ppsf_mom": [0.05, 0.15, 0.25],
        "avg_sale_to_list": [0.9, 1.0, 1.1],
        "inventory": [50, 60, 70],
        "price_change_vs_inventory": [0.5, 0.6, 0.7],
        "market_heat_index": [0.8, 0.9, 1.0],
        "pending_to_sold_ratio": [0.7, 0.8, 0.9],
        "median_sale_price": [150, 250, 350],
    })

    # Train a model for testing
    features = test_df.columns[:-1]
    target = "median_sale_price"
    X = test_df[features].values
    y = test_df[target].values
    model = RandomForestRegressor(random_state=42)
    model.fit(X, y)

    # Save the model
    model_file_path = tmp_path / "test_RF_model.pkl"
    import joblib
    joblib.dump(model, model_file_path)

    # Evaluate the model
    metrics = evaluate_rf(test_df, model, output_path=str(tmp_path / "predictions.csv"))

    # Assertions
    assert "MAE" in metrics, "MAE is missing from metrics"
    assert "MSE" in metrics, "MSE is missing from metrics"
    assert "RMSE" in metrics, "RMSE is missing from metrics"
    assert "MAPE" in metrics, "MAPE is missing from metrics"

    # Check predictions file
    predictions_file = tmp_path / "predictions.csv"
    assert predictions_file.exists(), "Predictions CSV file not created"

def test_main():
    """
    End-to-end test for the main function.

    Validates the entire evaluation pipeline runs without errors.
    """
    test_file = os.path.join(DATA_PATH, "test_data.csv")
    model_file = "RF_model.pkl"
    metrics = main(test_file, model_file)

    assert metrics is not None, "Metrics are None"
    assert "MAE" in metrics, "MAE is missing from metrics"
    assert "MSE" in metrics, "MSE is missing from metrics"
