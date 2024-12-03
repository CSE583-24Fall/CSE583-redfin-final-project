import pandas as pd
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Update BASE_PATH to point to repository root
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_PATH = os.path.join(BASE_PATH, "data/machinelearningresults")

# ### Import Data
results = os.path.join(DATA_PATH, "models_predictions.csv")
df = pd.read_csv(results)
df.head()

# Example DataFrame
data = {
    "date": df['period_end'],
    "actual": df['Actual Values'],  # Actual housing prices
    "arima": df['ARIMA Predictions'],  # ARIMA predictions
    "ensemble": df['Random Forest Regressor'],  # Ensemble predictions
    "lstm": df['LSTM Predictions'],  # LSTM predictions
    "sarimax": df['SARIMAX'],  # SARIMAX predictions
}
df = pd.DataFrame(data)

# Streamlit app
st.title("Redfin Housing Price Prediction Visualization")

# Sidebar for model selection
st.sidebar.header("Choose a Model")
model = st.sidebar.selectbox(
    "Select a model to visualize:",
    ["ARIMA", "Ensemble", "LSTM", "SARIMAX"]
)

# Map model names to DataFrame columns
model_column = {
    "ARIMA": "arima",
    "Ensemble": "ensemble",
    "LSTM": "lstm",
    "SARIMAX":"sarimax"
}[model]

# Plot actual vs predicted
st.subheader(f"{model} Predictions vs Actual")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(df["date"], df["actual"], label="Actual", linewidth=2.5)
ax.plot(df["date"], df[model_column], label=f"{model} Predicted", linestyle="--", linewidth=2)
ax.set_xlabel("Date")
ax.set_ylabel("Housing Prices")
ax.legend()
ax.grid(True)

# Rotate x-axis labels
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

# Optional: Show data table
if st.checkbox("Show Data Table"):
    st.write(df[["date", "actual", model_column]])

mae = mean_absolute_error(df["actual"], df[model_column])
st.sidebar.write(f"MAE: {mae:.2f}")

# Compute metrics for the selected model
mae = mean_absolute_error(df["actual"], df[model_column])
rmse = mean_squared_error(df["actual"], df[model_column], squared=False)
r2 = r2_score(df["actual"], df[model_column])

# Display metrics
st.sidebar.subheader("Model Performance Metrics")
st.sidebar.write(f"Mean Absolute Error (MAE): {mae:.2f}")
st.sidebar.write(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
st.sidebar.write(f"R² Score: {r2:.2f}")

# Sidebar to select multiple models
selected_models = st.sidebar.multiselect(
    "Select Models to Compare", ["ARIMA", "Ensemble", "LSTM", "SARIMAX"], default=["ARIMA", "Ensemble"]
)

# Plot predictions for selected models
st.subheader("Model Comparison")
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(df["date"], df["actual"], label="Actual", linewidth=2.5)
for model in selected_models:
    ax.plot(df["date"], df[model.lower()], label=f"{model} Predicted", linestyle="--")
ax.legend()
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)


# Highlight significant errors
df["error"] = abs(df["actual"] - df[model_column])
significant_error_threshold = st.sidebar.slider("Error Threshold", 0, 1000, 500)

significant_errors = df[df["error"] > significant_error_threshold]
ax.scatter(
    significant_errors["date"], significant_errors["actual"],
    color="red", label="Significant Errors", zorder=1
)
st.pyplot(fig)





