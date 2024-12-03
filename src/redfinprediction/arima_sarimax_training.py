import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pmdarima import auto_arima
import pickle
from sklearn.metrics import mean_absolute_error, mean_squared_error

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
DATA_PATH = os.path.join(BASE_PATH, "data/raw")

# Training component
def load_and_preprocess_data(file_path):
    """
    Load and preprocess time series data from a CSV file.

    This function reads data from a CSV file, converts date columns to datetime format,
    and sets the `period_end` column as the index.

    Args:
        file_path (str): Path to the CSV file containing the data.

    Returns:
        pd.DataFrame: A DataFrame with preprocessed data where `period_end` is the index.
    """
    df = pd.read_csv(file_path)
    df['period_begin'] = pd.to_datetime(df['period_begin'])
    df['period_end'] = pd.to_datetime(df['period_end'])
    df.set_index('period_end', inplace=True)
    return df

def find_best_order(data, column, seasonal=False, seasonal_period=1, return_params=True):
    """
    Find the best ARIMA or SARIMA model order for the given data.

    This function uses the `auto_arima` method to determine the optimal
    (p, d, q) and seasonal (P, D, Q, m) parameters for the specified column.

    Args:
        data (pd.DataFrame): The input DataFrame containing the time series data.
        column (str): Name of the column to model.
        seasonal (bool, optional): Whether to include seasonal components. Defaults to False.
        seasonal_period (int, optional): Seasonal period for the time series. Defaults to 1.
        return_params (bool, optional): Whether to return the model parameters. Defaults to True.

    Returns:
        tuple: A tuple containing the (p, d, q) order and the seasonal (P, D, Q, m) order.
    """
    auto_model = auto_arima(
        data[column],
        seasonal=seasonal,
        m=seasonal_period,
        trace=True,
        error_action='ignore',
        suppress_warnings=True,
        stepwise=True
    )
    return auto_model.order, auto_model.seasonal_order

def train_arima(df, column, order):
    """
    Train an ARIMA model on the given data.

    This function fits an ARIMA model to the specified column of the input DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame containing the time series data.
        column (str): Name of the column to model.
        order (tuple): The (p, d, q) order of the ARIMA model.

    Returns:
        ARIMA Results: The fitted ARIMA model results.
    """
    model = ARIMA(df[column], order=order)
    result = model.fit()
    return result

def train_sarimax(df, column, order, seasonal_order):
    """
    Train a SARIMAX model on the given data with exogenous variables.

    This function fits a SARIMAX model to the specified column of the input DataFrame
    using exogenous variables.

    Args:
        df (pd.DataFrame): The input DataFrame containing the time series data.
        column (str): Name of the column to model.
        order (tuple): The (p, d, q) order of the ARIMA component.
        seasonal_order (tuple): The (P, D, Q, m) order of the seasonal component.

    Returns:
        SARIMAX Results: The fitted SARIMAX model results.
    """
    X_train = df[['demand_supply_ratio', 'price_drop_ratio', 'pending_to_sold_ratio', 'market_heat_index', 'price_change_vs_inventory', 'sales_change_vs_supply']]
    y_train = df['median_sale_price']
    sarimax_model = SARIMAX(y_train, exog=X_train, order=order, seasonal_order=seasonal_order)
    sarimax_result = sarimax_model.fit(disp=False)
    return sarimax_result

def save_model_to_pickle(model, filename):
    """
    Save a model to a file using pickle.

    This function serializes and saves a trained model to a file for later use.

    Args:
        model (object): The trained model to be saved.
        filename (str): The name of the file to save the model.

    Returns:
        None
    """
    output_path = os.path.join(BASE_PATH, "src/data/redfinprediction", filename)
    try:
        with open(filename, 'wb') as file:
            pickle.dump(model, file)
        print(f"Model successfully saved to {output_path}.")
    except Exception as e:
        print(f"An error occurred while saving the model: {e}")

def main(file_path, arima_filename, sarimax_filename):
    # Load and preprocess data
    df = load_and_preprocess_data(file_path)

    # Find best orders
    arima_order, _ = find_best_order(df, 'median_sale_price', seasonal=False)
    sarimax_order, seasonal_order = find_best_order(df, 'median_sale_price', seasonal=True, seasonal_period=12)

    # Train and save ARIMA model
    arima_result = train_arima(df, 'median_sale_price', arima_order)
    save_model_to_pickle(arima_result, arima_filename)

    # Train and save SARIMAX model
    sarimax_result = train_sarimax(df, 'median_sale_price', sarimax_order, seasonal_order)
    save_model_to_pickle(sarimax_result, sarimax_filename)

# Parameters for training
file_path = os.path.join(DATA_PATH, "train_data.csv")
arima_filename = "arima_final.pkl"
sarimax_filename = "sarimax_final.pkl"

if __name__ == "__main__":
    main(file_path, arima_filename, sarimax_filename)
