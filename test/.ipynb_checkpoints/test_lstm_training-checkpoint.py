import pytest
import os
import numpy as np
from tensorflow.keras.models import Sequential, load_model
from src.redfinprediction.lstm_training import (
    load_and_preprocess_data,
    build_lstm_model,
    train_lstm_model,
    save_model_to_file,
)

# Paths for testing
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(BASE_PATH, "data/raw")
MODEL_PATH = os.path.join(BASE_PATH, "src/redfinprediction/test_model.keras")


def test_load_and_preprocess_data():
    """
    Test the `load_and_preprocess_data` function.

    This test ensures that the function correctly loads data from a CSV file and processes it
    into scaled feature matrices and scalers.
    """
    train_file = os.path.join(DATA_PATH, "train_data.csv")
    X_scaled, y_scaled, scaler_X, scaler_y = load_and_preprocess_data(train_file)

    # Assert shapes
    assert X_scaled.shape[1:] == (1, 12), "Unexpected feature matrix shape"  # 12 features
    assert y_scaled.ndim == 2, "Unexpected target vector shape"


def test_build_lstm_model():
    """
    Test the `build_lstm_model` function.

    This test validates that the LSTM model is correctly constructed and compiled.
    """
    model = build_lstm_model((1, 12))  # 1 timestep, 12 features
    assert isinstance(model, Sequential), "Model is not a Sequential model"
    assert len(model.layers) > 0, "Model has no layers"


def test_train_lstm_model():
    """
    Test the `train_lstm_model` function.

    This test ensures that the model is trained successfully using the real train data.
    """
    train_file = os.path.join(DATA_PATH, "train_data.csv")
    model, scaler_X, scaler_y = train_lstm_model(train_file)

    # Assert the model is trained
    assert isinstance(model, Sequential), "Model training failed"
    assert scaler_X is not None, "Feature scaler is None"
    assert scaler_y is not None, "Target scaler is None"


def test_save_model_to_file(tmp_path):
    """
    Test the `save_model_to_file` function.

    This test validates that a trained model is saved correctly in the `.keras` format.

    Args:
        tmp_path (pathlib.Path): A temporary directory provided by pytest for saving files during tests.
    """
    train_file = os.path.join(DATA_PATH, "train_data.csv")
    model, _, _ = train_lstm_model(train_file)

    # Save the model
    file_path = tmp_path / "test_model.keras"
    save_model_to_file(model, str(file_path))

    # Assert the model file exists
    assert file_path.exists(), "Model file was not saved"


def test_full_pipeline():
    """
    End-to-end test: Load data, train the model, and save it.

    This test uses the real train data and validates that the full pipeline runs without errors.
    """
    train_file = os.path.join(DATA_PATH, "train_data.csv")

    # Train the model
    model, _, _ = train_lstm_model(train_file)

    # Save the model
    save_model_to_file(model, MODEL_PATH)

    # Load the saved model to verify it works
    loaded_model = load_model(MODEL_PATH)
    assert isinstance(loaded_model, Sequential), "Loaded model is not a Sequential model"