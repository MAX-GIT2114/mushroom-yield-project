import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os

# Ensure the figures directory exists
os.makedirs('reports/figures', exist_ok=True)

# 1. Load Data and Model
# Loading the test.csv to access the unscaled humidity values for interpretable plots
test_df = pd.read_csv('data/processed/test.csv')
X_test = np.load('data/processed/X_test.npy')
y_test = np.load('data/processed/y_test.npy')

model = joblib.load('models/linear_regression.joblib')

# 2. Generate Predictions & Calculate Residuals
y_pred = model.predict(X_test)

# Checklist item: Residuals calculated correctly (sign: actual - predicted)
residuals = y_test - y_pred

# 3. Diagnostic Plots
sns.set_theme(style="darkgrid")

# Plot A: Residuals vs Predicted Values
plt.figure(figsize=(8, 6))
plt.scatter(y_pred, residuals, alpha=0.6, edgecolors='w', color='royalblue')
plt.axhline(y=0, color='crimson', linestyle='--', linewidth=2)
plt.title('Residuals vs. Predicted Mushroom Yield')
plt.xlabel('Predicted Yield (kg)')
plt.ylabel('Residuals (Actual - Predicted)')
plt.tight_layout()
plt.savefig('reports/figures/residual_vs_predicted.png', dpi=150)
plt.close()

# Plot B: Residuals vs Humidity
plt.figure(figsize=(8, 6))
plt.scatter(test_df['humidity_pct'], residuals, alpha=0.6, edgecolors='w', color='seagreen')
plt.axhline(y=0, color='crimson', linestyle='--', linewidth=2)
plt.title('Residuals vs. Relative Humidity (%)')
plt.xlabel('Humidity (%)')
plt.ylabel('Residuals (Actual - Predicted)')
plt.tight_layout()
plt.savefig('reports/figures/residual_vs_humidity.png', dpi=150)
plt.close()

print("Diagnostics complete. Plots saved to reports/figures/.")