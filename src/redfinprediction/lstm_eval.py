import os
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import MinMaxScaler

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
TEST_DATA_PATH = os.path.join(BASE_PATH, "data/raw")
MODEL_PATH = os.path.join(BASE_PATH, "src/redfinprediction")
RESULT_PATH = os.path.join(BASE_PATH, "data/machinelearningresults")

# Evaluation components
def load_test_data(file_path):
    """
    Load and preprocess test data from a CSV file.

    Args:
        file_path (str): Path to the CSV file containing the test data.

    Returns:
        pd.DataFrame: A DataFrame with preprocessed test data.
    """
    df = pd.read_csv(file_path)
    df['period_begin'] = pd.to_datetime(df['period_begin'])
    df['period_end'] = pd.to_datetime(df['period_end'])
    return df

def load_lstm_model(model_path):
    """
    Load a trained LSTM model from a file.

    Args:
        model_path (str): Path to the saved LSTM model file.

    Returns:
        keras.Model: The loaded LSTM model.
    """
    try:
        model = load_model(model_path)
        print(f"Model successfully loaded from {model_path}.")
        return model
    except Exception as e:
        print(f"An error occurred while loading the model: {e}")
        return None

def calculate_metrics(y_true, y_pred):
    """
    Calculate evaluation metrics for predictions.

    Args:
        y_true (np.ndarray): True values of the target variable.
        y_pred (np.ndarray): Predicted values of the target variable.

    Returns:
        dict: A dictionary containing evaluation metrics (MAE, MSE, RMSE, MAPE).
    """
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100

    return {
        "MAE": mae,
        "MSE": mse,
        "RMSE": rmse,
        "MAPE": mape
    }

def evaluate_lstm(test_df, model, output_path=None):
    """
    Evaluate an LSTM model on test data.

    Args:
        test_df (pd.DataFrame): The test data containing features and the target variable.
        model (keras.Model): The trained LSTM model.
        output_path (str, optional): Path to save the predictions CSV file. Defaults to None.

    Returns:
        dict: A dictionary of evaluation metrics.
    """
    if output_path is None:
        output_path = os.path.join(RESULT_PATH, "lstm_predictions.csv")

    # Define features and target
    features = [
        "median_list_price", "median_ppsf", "median_sale_price_mom",
        "city_freq", "property_type_Condo/Co-op", "median_list_price_mom",
        "median_ppsf_mom", "avg_sale_to_list", "inventory",
        "price_change_vs_inventory", "market_heat_index", "pending_to_sold_ratio"
    ]
    target = "median_sale_price"

    # Extract features and target from test data
    X_test = test_df[features].values
    y_test = test_df[target].values

    # Scale the features and target as in training
    scaler_X = MinMaxScaler()
    scaler_y = MinMaxScaler()

    # Fit scalers on the test data (to mimic training scaling logic)
    X_test_scaled = scaler_X.fit_transform(X_test)
    y_test_scaled = scaler_y.fit_transform(y_test.reshape(-1, 1))

    # Reshape features for LSTM input
    X_test_scaled = np.reshape(X_test_scaled, (X_test_scaled.shape[0], 1, X_test_scaled.shape[1]))

    # Make predictions
    predictions_scaled = model.predict(X_test_scaled)
    predictions = scaler_y.inverse_transform(predictions_scaled)

    # Save predictions to CSV
    predictions_df = pd.DataFrame({
        "Predicted Median Sale Price": predictions.flatten(),
        "Actual Median Sale Price": y_test
    })
    predictions_df.to_csv(output_path, index=False)
    print(f"Predictions saved to {output_path}.")

    # Calculate metrics
    metrics = calculate_metrics(y_test, predictions.flatten())

    print("LSTM Evaluation Metrics:")
    for key, value in metrics.items():
        print(f"{key}: {value:.2f}")

    return metrics


def main(test_file_path, model_filename):
    # Load test data
    test_df = load_test_data(test_file_path)

    # Load the trained LSTM model
    model_path = os.path.join(MODEL_PATH, model_filename)
    model = load_lstm_model(model_path)

    # Evaluate the model
    if model:
        metrics = evaluate_lstm(test_df, model)
        return metrics

# Parameters for evaluation
test_file_path = os.path.join(TEST_DATA_PATH, "test_data.csv")
model_filename = "lstm_model.keras"

if __name__ == "__main__":
    main(test_file_path, model_filename)