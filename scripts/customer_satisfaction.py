import sys
import os

# Add the 'scripts' directory to sys.path
sys.path.append(os.path.abspath('./scripts'))

from load_data import load_data_from_postgres


import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
#from scripts.load_data import load_data_from_postgres

# Load data
query = '''
    SELECT user_id, session_frequency, session_duration, total_traffic
    FROM user_engagement
'''
df = load_data_from_postgres(query)

# Check if 'satisfaction_score' exists, if not, calculate it
if 'satisfaction_score' not in df.columns:
    df['satisfaction_score'] = (df['session_frequency'] * 0.3) + (df['session_duration'] * 0.4) + (df['total_traffic'] * 0.3)

# Prepare features and target
X = df[['session_frequency', 'session_duration', 'total_traffic']]
y_reg = df['satisfaction_score']

# Standardize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train a linear regression model
regressor = LinearRegression()
regressor.fit(X_scaled, y_reg)

# Output the regression coefficients
print("Regression Coefficients:", regressor.coef_)
