import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential, save_model
from tensorflow.keras.layers import Dense, Dropout, Input, LSTM
import os

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DATA_PATH = os.path.join(BASE_PATH, "data/raw")

# Data Preparation
def load_and_preprocess_data(file_path):
    """
    Load and preprocess data for LSTM training.

    Args:
        file_path (str): Path to the CSV file containing the data.

    Returns:
        tuple: Scaled training datasets (X_train, y_train) and scalers for inverse transformations.
    """
    df = pd.read_csv(file_path)

    # Feature selection
    features = ["median_sale_price_mom", "median_list_price", "median_list_price_mom", 
                "median_ppsf", "median_ppsf_mom", "homes_sold", "inventory", 
                "months_of_supply", "median_dom", "avg_sale_to_list", "price_drops", 
                "off_market_in_two_weeks"]
    target = "median_sale_price"

    X = df[features].values
    y = df[target].values

    # Scale the data
    scaler_X = MinMaxScaler()
    scaler_y = MinMaxScaler()

    X_scaled = scaler_X.fit_transform(X)
    y_scaled = scaler_y.fit_transform(y.reshape(-1, 1))

    # Reshape for LSTM input
    X_scaled = np.reshape(X_scaled, (X_scaled.shape[0], 1, X_scaled.shape[1]))

    return X_scaled, y_scaled, scaler_X, scaler_y

# Build LSTM Model
def build_lstm_model(input_shape):
    """
    Build and compile the LSTM model.

    Args:
        input_shape (tuple): Shape of the input data.

    Returns:
        Sequential: Compiled LSTM model.
    """
    model = Sequential([
        Input(shape=input_shape),
        LSTM(64, return_sequences=True),
        Dropout(0.2),
        LSTM(32, return_sequences=False),
        Dropout(0.2),
        Dense(16, activation='relu'),
        Dense(1)  # Single output for regression
    ])

    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
    return model

# Train LSTM Model
def train_lstm_model(file_path):
    """
    Train the LSTM model.

    Args:
        file_path (str): Path to the CSV file containing the data.

    Returns:
        tuple: Trained model, scalers for inverse transformations.
    """
    X, y, scaler_X, scaler_y = load_and_preprocess_data(file_path)
    
    # Build model
    model = build_lstm_model((X.shape[1], X.shape[2]))

    # Train the model
    model.fit(X, y, epochs=50, batch_size=32, verbose=1)

    return model, scaler_X, scaler_y

# Save Model
def save_model_to_file(model, filename):
    """
    Save the LSTM model to a file in the HDF5 format.

    Args:
        model (Sequential): Trained LSTM model.
        filename (str): The name of the file to save the model.

    Returns:
        None
    """
    output_path = os.path.join(BASE_PATH, "src/redfinprediction", filename)
    try:
        model.save(output_path)
        print(f"Model successfully saved to {output_path}.")
    except Exception as e:
        print(f"An error occurred while saving the model: {e}")

# Main function
def main(file_path, model_filename):
    """
    Main function to run the LSTM training and save the model.

    Args:
        file_path (str): Path to the input data.
        model_filename (str): Name of the file to save the trained model.

    Returns:
        None
    """
    model, _, _ = train_lstm_model(file_path)
    save_model_to_file(model, model_filename)

# Run the script
if __name__ == "__main__":
    input_file_path = os.path.join(DATA_PATH, "train_data.csv")
    model_file_name = "LSTM_model.keras"
    main(input_file_path, model_file_name) 
