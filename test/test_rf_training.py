import os
import pytest
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from src.redfinprediction.rf_training import (
    load_and_preprocess_data,
    train_random_forest_model,
    save_model_to_file,
)

# Paths for testing
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_PATH, "data/raw")
MODEL_PATH = os.path.join(BASE_PATH, "src/redfinprediction/test_RF_model.pkl")

def test_load_and_preprocess_data():
    """
    Test the `load_and_preprocess_data` function.

    This test ensures that the function correctly loads data from a CSV file and processes it
    into feature and target arrays.
    """
    train_file = os.path.join(DATA_PATH, "train_data.csv")
    X, y = load_and_preprocess_data(train_file)

    # Assert the shapes of features and target
    assert X.ndim == 2, "Feature matrix X should be 2-dimensional"
    assert y.ndim == 1, "Target vector y should be 1-dimensional"

    # Assert that the feature matrix and target vector are not empty
    assert X.shape[0] > 0, "Feature matrix X is empty"
    assert y.shape[0] > 0, "Target vector y is empty"

def test_train_random_forest_model():
    """
    Test the `train_random_forest_model` function.

    This test ensures that the Random Forest model is trained successfully with the real data.
    """
    train_file = os.path.join(DATA_PATH, "train_data.csv")
    X, y = load_and_preprocess_data(train_file)

    # Train the model
    best_model, best_params = train_random_forest_model(X, y)

    # Assert the model is a RandomForestRegressor
    assert isinstance(best_model, RandomForestRegressor), "Model is not a RandomForestRegressor"

    # Assert best_params is a dictionary with at least one parameter
    assert isinstance(best_params, dict), "Best parameters should be a dictionary"
    assert len(best_params) > 0, "Best parameters dictionary is empty"

def test_save_model_to_file(tmp_path):
    """
    Test the `save_model_to_file` function.

    This test validates that the model is saved correctly using joblib.

    Args:
        tmp_path (pathlib.Path): A temporary directory provided by pytest for saving files during tests.
    """
    train_file = os.path.join(DATA_PATH, "train_data.csv")
    X, y = load_and_preprocess_data(train_file)
    best_model, _ = train_random_forest_model(X, y)

    # Save the model
    file_path = tmp_path / "test_RF_model.pkl"
    save_model_to_file(best_model, str(file_path))

    # Assert the model file exists
    assert file_path.exists(), "Model file was not saved"

def test_full_pipeline():
    """
    End-to-end test: Load data, train the model, and save it.

    This test uses the real train data and validates that the full pipeline runs without errors.
    """
    train_file = os.path.join(DATA_PATH, "train_data.csv")
    X, y = load_and_preprocess_data(train_file)

    # Train the model
    best_model, _ = train_random_forest_model(X, y)

    # Save the model
    save_model_to_file(best_model, MODEL_PATH)

    # Load the saved model to verify it exists
    assert os.path.exists(MODEL_PATH), "Saved model file does not exist"

    # Assert the saved file can be loaded
    from joblib import load
    loaded_model = load(MODEL_PATH)
    assert isinstance(loaded_model, RandomForestRegressor), "Loaded model is not a RandomForestRegressor"
