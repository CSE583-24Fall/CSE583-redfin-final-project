import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import os

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DATA_PATH = os.path.join(BASE_PATH, "data/raw")

# Data Preparation
def load_and_preprocess_data(file_path):
    """
    Load and preprocess data for Random Forest training.

    Args:
        file_path (str): Path to the CSV file containing the data.

    Returns:
        tuple: Training datasets (X, y).
    """
    df = pd.read_csv(file_path)

    # Feature selection
    features = [
        "median_sale_price_mom", "median_list_price", "median_list_price_mom", 
        "median_ppsf", "median_ppsf_mom", "homes_sold", "inventory", 
        "months_of_supply", "median_dom", "avg_sale_to_list", "price_drops", 
        "off_market_in_two_weeks"
    ]
    target = "median_sale_price"

    X = df[features].values
    y = df[target].values

    return X, y

# Train Random Forest Model
def train_random_forest_model(X, y):
    """
    Train the Random Forest model with grid search.

    Args:
        X (np.ndarray): Feature matrix.
        y (np.ndarray): Target vector.

    Returns:
        tuple: Best model and the best hyperparameters.
    """
    rf_model = RandomForestRegressor(random_state=42)

    # Define hyperparameter grid
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 20, 30, None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'max_features': ['sqrt', 'log2', None]
    }

    grid_search = GridSearchCV(estimator=rf_model, param_grid=param_grid, cv=3, scoring='r2', verbose=2, n_jobs=-1)
    grid_search.fit(X, y)

    print(f"Best Parameters: {grid_search.best_params_}")
    print(f"Best Score: {grid_search.best_score_}")

    return grid_search.best_estimator_, grid_search.best_params_

# Save Model
def save_model_to_file(model, filename):
    """
    Save the Random Forest model to a file using joblib.

    Args:
        model (RandomForestRegressor): Trained Random Forest model.
        filename (str): The name of the file to save the model.

    Returns:
        None
    """
    output_path = os.path.join(BASE_PATH, "src/redfinprediction", filename)
    try:
        import joblib
        joblib.dump(model, output_path)
        print(f"Model successfully saved to {output_path}.")
    except Exception as e:
        print(f"An error occurred while saving the model: {e}")

# Main function
def main(file_path, model_filename):
    """
    Main function to run the Random Forest training and save the model.

    Args:
        file_path (str): Path to the input data.
        model_filename (str): Name of the file to save the trained model.

    Returns:
        None
    """
    X, y = load_and_preprocess_data(file_path)
    best_model, best_params = train_random_forest_model(X, y)
    save_model_to_file(best_model, model_filename)

# Run the script
if __name__ == "__main__":
    input_file_path = os.path.join(DATA_PATH, "train_data.csv")
    model_file_name = "RF_model.pkl"
    main(input_file_path, model_file_name)
