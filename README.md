# RedfinPredict: Real Estate Sales Pricing Forecast

RedfinPredict is a tool that provides real-time predictions of median sale 
prices for homes in popular U.S. cities, based on data from Redfin’s 
housing market. It visualizes price trends from 2019 to the present and 
offers dynamic insights to track and forecast housing market movements. 
The tool supports two machine learning methods, allowing users to compare 
and select the best approach for accurate predictions.

## Mission

Our mission is to empower homebuyers, investors, and real estate agents 
with real-time, data-driven insights into housing market trends. By 
leveraging Redfin’s comprehensive market data and advanced machine 
learning models, users can visualize price trends and compare two 
predictive approaches, enabling them to navigate price fluctuations and 
make informed decisions.

## Project Objective

Understanding the trend of median sale prices is crucial for homebuyers, 
investors, and real estate agents. Real estate prices are influenced by 
various factors, including economic conditions and housing features. This 
tool helps users:

- Easily visualize and track price trends.
- Make informed decisions with accurate sales price predictions.
- Navigate the complexities of a rapidly changing housing market.

RedfinPredict addresses the challenge of manually tracking and 
interpreting market trends by providing a real-time dashboard that tracks 
median sale price trends in popular U.S. cities. It uses machine learning 
models to offer accurate forecasts, allowing users to predict future price 
movements and choose the most reliable prediction model.

## Repository Structure

The final project directory consists of the following main subdirectories:

- **`data/`**: Contains raw data, cleaned data, and predictions.
- **`docs/`**: Holds the technology review files.
- **`src/`**: Includes code for the ETL pipeline, real-time data 
processing, and machine learning model comparisons (Streamlit app).
- **`tests/`**: Contains unit tests for the ETL pipeline and machine 
learning code.

## Architecture Diagram

Below is the architecture diagram of the RedfinPredict project.

![Architecture Diagram](images/583archv1.png)

The project follows an automated ETL pipeline architecture:

1. **Data Extraction**: Data is collected from Redfin’s data center.
2. **Data Cleaning**: Missing values, duplicates, and inconsistencies are 
handled automatically.
3. **Storage**: Cleaned data is uploaded to **Azure Blob Storage**.
4. **Machine Learning Models**: Four models (Ensemble, LSTM, ARIMA, 
SARIMAX) analyze the data and generate predictions.
5. **Visualization**: The results are visualized in **Tableau**, where 
interactive dashboards allow stakeholders to explore trends, compare model 
predictions, and track performance.

## Machine Learning Methods

The tool employs four machine learning methods to predict median sale 
prices:

- **Ensemble (Random Forest)**: Handles non-linear relationships, reduces 
overfitting, and identifies important features.
- **LSTM (Long Short-Term Memory)**: Models temporal dependencies and 
long-term trends in time-series data.
- **ARIMA (AutoRegressive Integrated Moving Average)**: Effective for 
short-term predictions based on univariate data.
- **SARIMAX (Seasonal ARIMAX)**: Advanced model that incorporates 
seasonality and external factors for more comprehensive forecasts.

### Model Performance

| ML Methods | Ensemble  | LSTM      | ARIMA     | SARIMAX   |
|------------|-----------|-----------|-----------|-----------|
| **MAE**    | 57,603.67 | 62,258.11 | 191,723.41| 194,247.94|
| **R-Squared** | 0.82    | 0.85      | -0.04     | -0.02     |

- **Best models**: Ensemble and LSTM, with the lowest MAE and highest 
R-squared score.

## Usage

### For Tech Users

1. Clone the repository and set up the environment.
2. The ETL pipeline is automated for data collection and processing.
3. Run the models (Ensemble, LSTM, ARIMA, SARIMAX) locally or on a cloud 
platform.
4. Evaluate model performance using metrics like **MAE** and 
**R-squared**.
5. Visualize the results in **Tableau** and compare model predictions.

### For Non-Tech Users

- Visit the interactive dashboard.
- Select your preferred time frame and view predicted median sale prices 
for homes.
- Compare predictive 

