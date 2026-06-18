\# Mushroom Yield Forecast — Technical Report



\## Executive Summary

This report presents a predictive modeling solution to forecast daily oyster mushroom (\*Pleurotus ostreatus\*) yield in a controlled-environment polyhouse. Using historical daily sensor readings—specifically temperature (°C), relative humidity (%), and carbon dioxide (CO₂, measured in ppm)—we evaluated linear and non-linear machine learning models. 



Our initial objective was to evaluate a tuned Random Forest regressor, which achieved a \*\*Test MAE of 0.445 kg\*\* (CV MAE of 0.466 kg) under optimized hyperparameters. However, a simpler baseline \*\*Linear Regression model outperformed the Random Forest, achieving a Test MAE of 0.419 kg\*\* (CV MAE of 0.441 kg) and explaining \*\*42.7%\*\* of the test variance ($R^2 = 0.427$). 



Following our project's tie-breaking protocol (which favors the simpler model if the Test MAE difference is within a 0.05 kg threshold), the \*\*Linear Regression model was selected as the final champion\*\*. This choice guarantees high interpretability for stakeholders and lower operational maintenance costs. The model has been successfully deployed as an interactive Streamlit dashboard for growers.



> \[!IMPORTANT]

> \*\*Champion Model Selected: Linear Regression\*\*

> \* \*\*Performance:\*\* Test MAE = 0.419 kg, CV MAE = 0.441 kg, $R^2 = 0.427$

> \* \*\*Rationale:\*\* Outperformed the tuned Random Forest model while remaining simpler and fully interpretable. The performance difference of 0.026 kg falls well within the project's 0.05 kg selection threshold.



\---



\## 1. Problem \& Agritech Context

Oyster mushrooms are highly sensitive to their microclimate. Cultivating them in controlled polyhouse environments requires maintaining strict atmospheric parameters to maximize fruiting efficiency and total crop yield. Key environmental factors include:



\* \*\*Temperature (°C):\*\* Regulates metabolic activity, growth rate, and trigger points for fruiting body initiation.

\* \*\*Relative Humidity (%):\*\* Crucial for preventing drying of the mycelium and supporting cell expansion in the growing fruiting bodies.

\* \*\*Carbon Dioxide (CO₂, ppm):\*\* High $\\text{CO}\_2$ levels promote mycelial growth but severely inhibit the development of caps during the fruiting phase, leading to long stems and low-quality yields.



Historically, harvest planning has been reactive, leading to supply-chain inefficiencies, market stockouts, or product waste. Developing a reliable machine learning model to estimate daily yield based on environmental telemetry allows growers to:

1\. \*\*Optimize Harvest Logistics:\*\* Plan labor, packaging, and transport schedules in advance.

2\. \*\*Actively Control Polyhouse Conditions:\*\* Adjust heating, ventilation, and misting systems based on predictive feedback.



\---



\## 2. Data Sources \& Cleaning

The raw dataset, \[polyhouse\_sensors.csv](file:///C:/Users/mahic/mushroom-yield-project%20-%20data/raw/polyhouse\_sensors.csv), contains \*\*365 observations\*\* representing a full year of daily readings from January 1, 2024, to December 30, 2024.



\### Data Cleaning Strategy

The data pipeline was implemented in \[clean.py](file:///C:/Users/mahic/mushroom-yield-project%20-%20src/clean.py) using the following steps:

1\. \*\*Missing Value Assessment:\*\* An initial check reported zero null values across all sensor parameters and target yields.

2\. \*\*Range Validation \& Filtering:\*\* Clean boundaries were established based on polyhouse operating limits:

&#x20;  \* \*\*Temperature:\*\* 10 to 35 °C

&#x20;  \* \*\*Humidity:\*\* 50% to 100%

&#x20;  \* \*\*$\\text{CO}\_2$:\*\* 400 to 2000 ppm

&#x20;  \* \*\*Yield:\*\* Non-null target values (`yield\_kg`)

3\. \*\*Sensor Imputation:\*\* Short sensor gaps were addressed using forward-fill imputation with a limit of 2 consecutive days.

4\. \*\*Deduplication:\*\* Duplicate timestamps were resolved by retaining the latest record.



\### Ingestion \& Cleaning Results

\* \*\*Initial Records:\*\* 365 rows

\* \*\*Invalid Records Filtered:\*\* 0 rows (all readings fell within expected operational envelopes)

\* \*\*Duplicates Removed:\*\* 0 rows

\* \*\*Final Preprocessed Dataset:\*\* 365 rows



The cleaned data is saved in Parquet format at \[02\_cleaned.parquet](file:///C:/Users/mahic/mushroom-yield-project%20-%20data/interim/02\_cleaned.parquet) for downstream modeling.



\---



\## 3. Exploratory Analysis

Descriptive statistics and correlations were computed to understand feature distributions and their relationships with yield.



\### Summary Statistics

| Metric | Temperature (°C) | Relative Humidity (%) | $\\text{CO}\_2$ (ppm) | Mushroom Yield (kg) |

| :--- | :---: | :---: | :---: | :---: |

| \*\*Count\*\* | 365 | 365 | 365 | 365 |

| \*\*Mean\*\* | 21.99 | 86.74 | 901.16 | 17.14 |

| \*\*Median\*\* | 21.97 | 86.70 | 904.00 | 17.13 |

| \*\*Std Dev\*\* | 1.41 | 3.07 | 78.27 | 0.68 |

| \*\*Min\*\* | 18.15 | 78.10 | 608.00 | 15.31 |

| \*\*Max\*\* | 26.37 | 94.80 | 1154.00 | 18.85 |

| \*\*CV\*\* | 0.064 | 0.035 | 0.087 | 0.040 |



\### Key Insights \& Distributions

\* \*\*Skewness:\*\* Mean and median are closely aligned for all variables, showing approximately symmetric, near-normal distributions (slight right skew in temperature, humidity, and yield; slight left skew in $\\text{CO}\_2$).

\* \*\*Coefficient of Variation (CV):\*\* Relative variability is low across all measurements (all CV values are under 10%), indicating a tightly controlled climate in the polyhouse.



\### Correlation Analysis

Pearson correlation coefficients ($r$) indicate the strength and direction of linear relationships between environmental inputs and yield:

\* \*\*Temperature \& Yield ($r = 0.524$):\*\* Moderate positive relationship. Within the observed range, higher temperatures are associated with higher yields, indicating enhanced growth kinetics.

\* \*\*Humidity \& Yield ($r = 0.242$):\*\* Weak positive relationship. Higher humidity supports development, but its effect is less pronounced linearly due to the already-high baseline humidity (median 86.70%).

\* \*\*$\\text{CO}\_2$ \& Yield ($r = -0.260$):\*\* Weak negative relationship. Elevated $\\text{CO}\_2$ concentrations correlate with reduced yield, highlighting the biological need for adequate ventilation.

\* \*\*Inter-sensor Collinearity:\*\* Correlations between sensor variables are extremely close to zero (e.g., Temperature vs Humidity $r = -0.022$; Temperature vs $\\text{CO}\_2$ $r = 0.007$). This indicates no multicollinearity, meaning the regression coefficients can be interpreted reliably.



\#### Correlation Heatmap

!\[Correlation Heatmap](file:///C:/Users/mahic/mushroom-yield-project%20-%20reports/figures/corr\_heatmap.png)



\#### Scatter Plots vs Yield

!\[Sensor Scatter Plots](file:///C:/Users/mahic/mushroom-yield-project%20-%20reports/figures/scatter\_yield.png)



\---



\## 4. Feature Engineering \& Validation Strategy



\### Feature Preprocessing

1\. \*\*Min-Max Scaling:\*\* Environmental variables occupy different scales ($\\text{CO}\_2$ is in hundreds of ppm, temperature in tens of °C). To prevent variables with larger absolute scales from dominating the loss function, features were normalized to a common \[0, 1] range:

&#x20;  $$\\text{Scaled Value} = \\frac{\\text{Value} - \\text{Min Value}}{\\text{Max Value} - \\text{Min Value}}$$

2\. \*\*Interaction Feature:\*\* A Temperature–Humidity interaction feature was tested:

&#x20;  $$\\text{temp\\\_humid\\\_interaction} = \\frac{\\text{temperature\\\_c} \\times \\text{humidity\\\_pct}}{100}$$

&#x20;  This was designed to capture biological synergistic effects. However, feature selection logs confirmed that utilizing the direct raw inputs yielded more stable cross-validation scores without overfitting.



\### Validation Strategy: Why a Temporal Split Matters

A standard random K-fold cross-validation or a random train/test split is inappropriate for temporal sensor data. Random splitting leads to \*\*data leakage\*\* because sensor readings from adjacent days are highly correlated. Under a random split, the model might train on day $N-1$ and day $N+1$ and test on day $N$, resulting in an artificially inflated test score that fails to generalize when deployed.



To simulate real-world forecasting (where the model must predict future yield using past environmental data), we implemented a strict \*\*chronological 80/20 train/test split\*\* in \[split\_scale.py](file:///C:/Users/mahic/mushroom-yield-project%20-%20src/split\_scale.py):

\* \*\*Training Period (First 80%):\*\* 2024-01-01 to 2024-10-18 (292 daily records)

\* \*\*Test Period (Last 20%):\*\* 2024-10-19 to 2024-12-30 (73 daily records)

\* \*\*Leakage Prevention Assertion:\*\* We enforce `assert test\_start\_date > train\_end\_date` to ensure no future observations ever leak into the training set.

\* \*\*Fitted Scaler Isolation:\*\* The `MinMaxScaler` is fitted \*only\* on the training dataset and subsequently applied to transform the test set, preventing target leakages during feature scaling.



\---



\## 5. Models Evaluated

Three modeling configurations were evaluated:

1\. \*\*Linear Regression (Baseline):\*\* A simple linear model trained using Ordinary Least Squares. Highly interpretable, offering direct visibility into how changes in each environmental variable affect yield.

2\. \*\*Random Forest (Default):\*\* An ensemble of 100 decision trees trained using scikit-learn defaults. Highly prone to overfitting on small datasets.

3\. \*\*Random Forest (Tuned):\*\* Hyperparameters were optimized using Grid Search with time-series cross-validation.

&#x20;  \* \*\*Cross-Validation:\*\* `TimeSeriesSplit(n\_splits=3)` on the training data.

&#x20;  \* \*\*Hyperparameter Search Grid:\*\*

&#x20;    \* `n\_estimators`: `\[50, 100, 200]`

&#x20;    \* `max\_depth`: `\[None, 8, 16]`

&#x20;    \* `min\_samples\_leaf`: `\[1, 3, 5]`

&#x20;  \* \*\*Optimal Hyperparameters Selected:\*\*

&#x20;    ```json

&#x20;    {

&#x20;      "max\_depth": 8,

&#x20;      "min\_samples\_leaf": 5,

&#x20;      "n\_estimators": 100

&#x20;    }

&#x20;    ```

&#x20;  \* \*\*Grid Boundary Analysis:\*\* The search selected `min\_samples\_leaf = 5`, which is at the upper edge of the grid. This indicates that additional regularization (larger leaf sizes) helps prevent overfitting in the decision trees.



\---



\## 6. Results \& Champion Selection



\### Model Performance Comparison

We evaluated the models on the held-out chronological test set.



> \[!NOTE]

> \*\*Metric Explanations for Non-Technical Stakeholders:\*\*

> \* \*\*Mean Absolute Error (MAE):\*\* The average prediction error in kilograms. An MAE of 0.419 kg means the predictions differ from actual yields by 0.419 kg on average.

> \* \*\*Root Mean Squared Error (RMSE):\*\* Similar to MAE but penalizes larger errors more heavily.

> \* \*\*$R^2$ (Coefficient of Determination):\*\* The proportion of variance explained by environmental features. A score of 0.427 means the model explains 42.7% of yield fluctuations.



| Model | CV Mean MAE (kg) | Test MAE (kg) | Test RMSE (kg) | Test $R^2$ | Interpretability |

| :--- | :---: | :---: | :---: | :---: | :---: |

| \*\*Linear Regression (Champion)\*\* | \*\*0.441\*\* | \*\*0.419\*\* | \*\*0.535\*\* | \*\*0.427\*\* | \*\*High\*\* |

| \*\*Random Forest (Tuned)\*\* | 0.466 | 0.445 | 0.562 | 0.369 | Medium-Low |

| \*\*Random Forest (Default)\*\* | 0.475 | 0.450 | 0.580 | 0.327 | Medium |



\### Rationale for Champion Selection

1\. \*\*Highest Performance:\*\* Linear Regression achieved the lowest Test MAE (0.419 kg), the lowest Test RMSE (0.535 kg), and the highest $R^2$ score (0.427) on the unseen test dataset.

2\. \*\*Tie-Breaking Rule:\*\* Our project rule states that if the difference in Test MAE between the complex model (Random Forest Tuned) and the simple model (Linear Regression) is less than 0.05 kg, the simpler model is selected. The difference is:

&#x20;  $$\\text{Difference} = 0.445\\text{ kg} - 0.419\\text{ kg} = 0.026\\text{ kg}$$

&#x20;  Since 0.026 kg is well under the 0.05 kg threshold, Linear Regression is the clear champion.

3\. \*\*Leakage/Overfitting Signs:\*\* The default Random Forest showed severe overfitting (Train MAE of 0.167 kg vs Test MAE of 0.450 kg). While hyperparameter tuning mitigated this, the Random Forest model could not outperform the linear baseline.

4\. \*\*Stakeholder Trust \& Coefficients:\*\* The linear model yields clear, actionable equations. Since features are scaled, coefficient weights are directly comparable:

&#x20;  \* \*\*Temperature Coefficient ($+1.894$):\*\* A 1-unit increase in scaled temperature increases yield by 1.894 kg.

&#x20;  \* \*\*Humidity Coefficient ($+0.959$):\*\* A 1-unit increase in scaled humidity increases yield by 0.959 kg.

&#x20;  \* \*\*$\\text{CO}\_2$ Coefficient ($-1.213$):\*\* A 1-unit increase in scaled $\\text{CO}\_2$ decreases yield by 1.213 kg.



\#### Predicted vs Actual Yield Plot (Champion Model)

!\[Predicted vs Actual Yield](file:///C:/Users/mahic/mushroom-yield-project%20-%20reports/figures/pred\_vs\_actual.png)



\---



\## 7. Streamlit App \& Deployment



\### Dashboard Implementation

An interactive dashboard was developed in \[app.py](file:///C:/Users/mahic/mushroom-yield-project%20-%20app.py) for operational use by growers:

\* \*\*Sensor Inputs:\*\* User-friendly sliders for Temperature (10 to 35 °C), Humidity (50 to 100%), and $\\text{CO}\_2$ (400 to 2000 ppm).

\* \*\*Advisory Boundary Warnings:\*\* Displays warnings if user inputs fall outside the training ranges (Temperature: 15–30 °C, Humidity: 60–95%, $\\text{CO}\_2$: 500–1500 ppm), notifying the grower that predictions may be less reliable.

\* \*\*Sensitivity (What-if) Chart:\*\* Generates a real-time line chart showing how predicted yield shifts as humidity varies from 60% to 98% while holding the input temperature and $\\text{CO}\_2$ constant.

\* \*\*API \& Logging:\*\* Requests are processed using the prediction module in \[predict.py](file:///C:/Users/mahic/mushroom-yield-project%20-%20Copy/src/predict.py) and appended to \[predictions.csv](file:///C:/Users/mahic/mushroom-yield-project%20-%20logs/predictions.csv).



\### Live Cloud Deployment

\* \*\*Platform:\*\* Streamlit Community Cloud

\* \*\*URL:\*\* \[mushroom-yield-project-kxxscjfktzdrjvfcegriut.streamlit.app/](https://mushroom-yield-project-kxxscjfktzdrjvfcegriut.streamlit.app/)

\* \*\*Verification:\*\* Verified that the deployed cloud instance produces predictions matching the local environment within standard floating-point tolerance.



\---



\## 8. Monitoring \& Next Iterations



\### Inference Logging

All production prediction requests are logged to \[predictions.csv](file:///C:/Users/mahic/mushroom-yield-project%20-%20logs/predictions.csv). The recorded fields are:

1\. `timestamp\_utc`: Time of the request.

2\. `temperature\_c`: Input temperature.

3\. `humidity\_pct`: Input humidity.

4\. `co2\_ppm`: Input $\\text{CO}\_2$ concentration.

5\. `predicted\_kg`: Output yield prediction in kg.



\### Data Drift Scenarios

1\. \*\*Sensor Calibration Drift:\*\* Over time, physical sensors degrade. For example, if a humidity sensor drifts +5% higher than the actual room state, the model will over-predict yield. Continuous calibration schedules are required.

2\. \*\*Seasonal Drift:\*\* Extreme conditions (e.g., peak summer or monsoon seasons) not represented in the training period will lead to out-of-range inputs.

3\. \*\*Operational Drift:\*\* Changes in substrate mixture, ventilation setups, or growing different varieties of oyster mushrooms will alter the underlying biology and invalidate the coefficients.



\### Retraining Triggers

The model should be retrained:

\* Every \*\*3 to 6 months\*\* as new harvest and telemetry logs are collected.

\* Whenever \*\*sensor hardware is replaced or re-calibrated\*\*.

\* Following major \*\*operational changes\*\* (such as a new polyhouse ventilation structure).



\---



\## 9. Limitations

1\. \*\*Dataset Size:\*\* A sample size of 365 daily records is small. It prevents the use of deep sequence models (like LSTM or transformer architectures) that could learn complex temporal lags.

2\. \*\*Linearity Assumption:\*\* The champion model assumes linear, additive relationships. In reality, biological systems have sharp thresholds—e.g., if temperature rises above 32 °C, mushroom growth doesn't increase linearly; the crop dies.

3\. \*\*Sensor Gaps:\*\* Important growth factors are missing, such as:

&#x20;  \* \*Light intensity (lux)\*

&#x20;  \* \*Airflow velocity/ventilation rate (m/s)\*

&#x20;  \* \*Substrate moisture content (%)\*

4\. \*\*Synthetic Data:\*\* The data is synthetically generated for development purposes and may lack real-world sensor noise and micro-fluctuations.



\---



\## Appendix: Reproduction Commands

To replicate the entire machine learning pipeline from raw data to the final model artifacts and figures, run the following commands sequentially from the project root:



```bash

\# 1. Activate virtual environment

venv\\Scripts\\activate



\# 2. Re-ingest raw sensor data

python src/ingest.py



\# 3. Clean and validate dataset

python src/clean.py



\# 4. Perform chronological split and feature scaling

python src/split\_scale.py



\# 5. Train baseline Linear Regression model

python src/lr\_model.py



\# 6. Run baseline model residual diagnostic analysis

python src/diagnostics.py



\# 7. Train default Random Forest model \& plot feature importances

python src/random\_forest.py



\# 8. Run 5-fold TimeSeries cross-validation evaluation

python src/cv.py



\# 9. Perform hyperparameter tuning via GridSearchCV

python src/gridsearch-cv.py



\# 10. Run champion selection \& generate final evaluation outputs

python src/champion.py



\# 11. Run prediction validation tests

python -m pytest tests/

```



