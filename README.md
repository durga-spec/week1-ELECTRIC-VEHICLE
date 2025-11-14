🚗 EV Range Prediction – Machine Learning Model (Week-2 Submission)


📌 Week-2 Objective

The goal of Week-2 is to improve the Week-1 work by:

Cleaning and preparing the merged EV dataset

Performing feature engineering

Building an ML model

Evaluating its performance

Documenting insights and results professionally



---

📂 Dataset Used

The dataset contains the following key features:

Brand

Model

Country

Battery Capacity (kWh)

Charging Time (hours)

Efficiency (km/kWh)

Fast Charging Support

Price (USD)

Actual Range (km) → Target variable


This dataset was cleaned and processed for model building.


---

⚙️ Machine Learning Model

A Linear Regression model was trained to predict the driving range (km) of an Electric Vehicle based on key numeric and encoded categorical features.

✔️ Steps Performed

1. Imported dataset into Jupyter Notebook


2. Performed data cleaning


3. Removed missing values


4. Applied One-Hot Encoding to Brand, Model, and Country


5. Split data into training and testing sets


6. Trained Linear Regression model


7. Evaluated performance using MAE, RMSE, and R² Score




---

📊 Model Performance

Metric	Result

MAE	445 km
RMSE	570 km
R² Score	0.75


📌 Interpretation

The model explains 75% of the variance in EV range.

MAE and RMSE indicate moderate accuracy, suitable for baseline modeling.

This establishes a strong foundation for Week-3 improvement.



---

🧠 Insights Gained

Battery capacity has the highest correlation with EV range.

Efficiency (km/kWh) and fast-charging capability also impact range.

Categorical variables (Brand, Country) add useful patterns after encoding.

