Many competing resources available for one task (e.g. machine learning)
Why do we need such task?
Why do we choose one resource over?

Hongfan update (for machine learning):
For DS and ML, our goal is to create the established algorithms to develop sale prices prediction
for the time seires data.
       
Section 1: traditional, statistical methods
        - Use statsmodel decompose to identify the trends, seasonality, and noise
        - Use ARIMA methods for autoregressive integrated moving average investigation

Section 2: Machine Learning Methods
        - XGBoost
        - RandomForest Regressor

Section 3:Deep learning methods
        - Use LSTM or RNN model that has capabilities to incorporate past information for future
        predictions

We will use statsmodel, xgboost, sklearn, and tensorflow keras, for the reasons that they are well  
established, well-maintained packages.


CP update (for visualization):
Our stakeholders are primarily non-technical individuals interested in 
tracking current real estate trends and forecasting future developments. 
They require a user-friendly and intuitive interface to easily visualize 
data, explore trends, and access predictive insights without needing 
technical expertise. Therefore we decided to include a dashboard in our 
project.


Tableau is user-friendly for both technical and non-technical users due to 
its drag-and-drop functionality. It also allows users with light coding 
skills to quickly create interactive dashboards.

Power BI works well with the Microsoft ecosystem, making Microsoft office 
Excel users easy to use learn. It provides strong features for visualizing 
data and business insights.

Python has several libraries for visualization like Matplotlib, Seaborn, 
and Plotly. They are open-source and highly customizable. However, they 
require coding knowledge, so they are especially for data science and tech 
professional handling advanced analytics and unique visualizations


Tableau:
-	Works with the iOS system. All team members use MacBooks for work, 
so we chose Tableau over Power BI. Since we are building an ETL process, 
Tableau can connect to various data sources, from databases to cloud 
sources, is also another thing we consider for adoption. On top of that, 
some of us already know the basics of Tableau, which is a bonus for 
teammates to add new project to portfolio on Tableau Public.
PowerBI:
-	It is a great and affordable tool overall, with comprehensive 
features. Many companies have also adopted this technology. However, since 
Power BI is heavily integrated into the Microsoft ecosystem, we have 
decided to go with Tableau. Additionally, connecting to non-Microsoft 
databases or cloud services in Power BI may require extra setup or 
third-party tools, which can complicate the ETL process and reduce its 
efficiency.
Python:
-	The major users of our dashboard are non-technical individuals who 
require a more user-friendly interface and ease of use. Python, however, 
is not ideal for this situation, as it is better suited for more technical 
users who are comfortable with coding and complex data processing.
 
