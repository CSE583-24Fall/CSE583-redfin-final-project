import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from pmdarima import auto_arima
import pickle
from sklearn.metrics import mean_absolute_error, mean_squared_error
import os

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
TEST_DATA_PATH = os.path.join(BASE_PATH, "data/raw")
MODEL_PATH = os.path.join(BASE_PATH, "src/data/redfinprediction")

# Evaluation components
def load_test_data(file_path):
    """
    Load and preprocess test data from a CSV file.

    This function reads test data from a CSV file, converts date columns to datetime format,
    and sets the `period_end` column as the index.

    Args:
        file_path (str): Path to the CSV file containing the test data.

    Returns:
        pd.DataFrame: A DataFrame with preprocessed test data where `period_end` is the index.
    """
    df = pd.read_csv(file_path)
    df['period_begin'] = pd.to_datetime(df['period_begin'])
    df['period_end'] = pd.to_datetime(df['period_end'])
    df.set_index('period_end', inplace=True)
    return df

def load_model_from_pickle(filename):
    """
    Load a model from a pickle file.

    This function deserializes and loads a trained model from a file.

    Args:
        filename (str): The name of the file containing the serialized model.

    Returns:
        object: The loaded model if successful; otherwise, `None` if an error occurs.
    """
    try:
        with open(filename, 'rb') as file:
            model = pickle.load(file)
        print(f"Model successfully loaded from {filename}.")
        return model
    except Exception as e:
        print(f"An error occurred while loading the model: {e}")
        return None

def calculate_metrics(y_true, y_pred):
    """
    Calculate evaluation metrics for predictions.

    This function computes common regression metrics such as Mean Absolute Error (MAE),
    Mean Squared Error (MSE), Root Mean Squared Error (RMSE), and Mean Absolute Percentage Error (MAPE).

    Args:
        y_true (pd.Series or np.ndarray): True values of the target variable.
        y_pred (pd.Series or np.ndarray): Predicted values of the target variable.

    Returns:
        dict: A dictionary containing the following metrics:
            - "MAE": Mean Absolute Error
            - "MSE": Mean Squared Error
            - "RMSE": Root Mean Squared Error
            - "MAPE": Mean Absolute Percentage Error
    """
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = mse ** 0.5
    mape = (np.abs((y_true - y_pred) / y_true).mean()) * 100

    return {
        "MAE": mae,
        "MSE": mse,
        "RMSE": rmse,
        "MAPE": mape
    }

def evaluate_arima(test_df, model, output_path=None):
    """
    Evaluate an ARIMA model on test data.

    This function uses the provided ARIMA model to generate forecasts and evaluates its performance
    using metrics such as MAE, MSE, RMSE, and MAPE.

    Args:
        test_df (pd.DataFrame): The test data containing the target variable.
            Must include the `median_sale_price` column.
        model (ARIMAResults): A fitted ARIMA model to be evaluated.
        output_path (str, optional): Path to save the predictions as a CSV file.
            Defaults to 'data/machinelearningresults/arima_predictions.csv'.

    Returns:
        dict: A dictionary of evaluation metrics for the ARIMA model.
    """
    if output_path is None:
        output_path = os.path.join(BASE_PATH, "data/machinelearningresults/arima_predictions.csv")

    y_test = test_df['median_sale_price']
    predictions = model.forecast(steps=len(test_df))
    predictions = pd.Series(predictions)
    predictions.index = test_df.index

    # Save predictions to CSV
    predictions_df = pd.DataFrame(predictions, columns=["ARIMA_Predicted_Value"])
    predictions_df.index.name = "Date"
    predictions_df.to_csv(output_path)
    print(f"ARIMA predictions saved to '{output_path}'.")

    # Calculate metrics
    metrics = calculate_metrics(y_test, predictions)

    print("ARIMA Evaluation Metrics:")
    for key, value in metrics.items():
        print(f"{key}: {value:.2f}")
    return metrics


    # Calculate metrics
    metrics = calculate_metrics(y_test, predictions)

    print("ARIMA Evaluation Metrics:")
    for key, value in metrics.items():
        print(f"{key}: {value:.2f}")
    return metrics

def evaluate_sarimax(test_df, model, output_path=None):
    """
    Evaluate a SARIMAX model on test data with exogenous variables.

    This function uses the provided SARIMAX model to generate predictions and evaluates
    its performance using metrics such as MAE, MSE, RMSE, and MAPE.

    Args:
        test_df (pd.DataFrame): The test data containing the target variable and exogenous variables.
            Must include the `median_sale_price` column and exogenous variable columns:
            ['demand_supply_ratio', 'price_drop_ratio', 'pending_to_sold_ratio',
             'market_heat_index', 'price_change_vs_inventory', 'sales_change_vs_supply'].
        model (SARIMAXResults): A fitted SARIMAX model to be evaluated.

    Returns:
        dict: A dictionary of evaluation metrics for the SARIMAX model.
        a dataframe containing sarimax prediction results.
    """
    if output_path is None:
        output_path = os.path.join(BASE_PATH, "data/machinelearningresults/sarimax_predictions.csv")

    X_test = test_df[['demand_supply_ratio', 'price_drop_ratio', 'pending_to_sold_ratio',
                      'market_heat_index', 'price_change_vs_inventory', 'sales_change_vs_supply']]
    y_test = test_df['median_sale_price']
    predictions = pd.Series(model.predict(start=0, end=len(y_test) - 1, exog=X_test))
    predictions.index = y_test.index

    # Save predictions to CSV
    predictions_df = pd.DataFrame(predictions, columns=["Sarimax_Predicted_Value"])
    predictions_df.index.name = "Date"
    predictions_df.to_csv(output_path)
    print("SARIMAX predictions saved to 'sarimax_predictions.csv'.")

    metrics = calculate_metrics(y_test, predictions)

    print("SARIMAX Evaluation Metrics:")
    for key, value in metrics.items():
        print(f"{key}: {value:.2f}")
    return metrics

def main(test_file_path, arima_filename, sarimax_filename):
    # Load test data
    test_df = load_test_data(test_file_path)

    # Load models
    arima_model = load_model_from_pickle(arima_filename)
    sarimax_model = load_model_from_pickle(sarimax_filename)

    # Evaluate ARIMA
    print("\nEvaluating ARIMA Model...")
    arima_metrics = evaluate_arima(test_df, arima_model)

    # Evaluate SARIMAX
    print("\nEvaluating SARIMAX Model...")
    sarimax_metrics = evaluate_sarimax(test_df, sarimax_model)

    return arima_metrics, sarimax_metrics


# Parameters for evaluation
test_file_path = os.path.join(TEST_DATA_PATH, "test_data.csv")
arima_filename = "arima_final.pkl"
sarimax_filename = "sarimax_final.pkl"

if __name__ == "__main__":
    main(test_file_path, arima_filename, sarimax_filename)
