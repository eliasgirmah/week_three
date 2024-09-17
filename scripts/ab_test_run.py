# scripts/run_ab_tests.py

import pandas as pd
from src.ab_testing import test_risk_by_province, test_risk_by_zipcode, test_margin_by_zipcode, test_risk_by_gender

# Load the dataset with specified data types
dtype_spec = {
    'PostalCode': 'object',  # Treat as object to avoid mixed type warnings
    'MaritalStatus': 'object',
    'CustomValueEstimate': 'float64',
    'WrittenOff': 'object',
    'Rebuilt': 'object',
    'Converted': 'object',
    'CrossBorder': 'object',
    'NumberOfVehiclesInFleet': 'float64'
}

data = pd.read_csv('data/dataset.csv', dtype=dtype_spec, low_memory=False)

# Handle missing values
data = data.dropna(subset=['TotalClaims', 'TotalPremium', 'Province', 'PostalCode', 'Gender'])

# Convert columns to appropriate types
data['TotalClaims'] = pd.to_numeric(data['TotalClaims'], errors='coerce')
data['TotalPremium'] = pd.to_numeric(data['TotalPremium'], errors='coerce')

# Drop rows with any remaining NaN values in essential columns
data = data.dropna(subset=['TotalClaims', 'TotalPremium'])

# Perform the tests
f_stat_province, p_value_province = test_risk_by_province(data)
f_stat_zipcode, p_value_zipcode = test_risk_by_zipcode(data)
f_stat_margin, p_value_margin = test_margin_by_zipcode(data)
t_stat_gender, p_value_gender = test_risk_by_gender(data)

# Print the results
print(f"Risk by Province - F-statistic: {f_stat_province}, p-value: {p_value_province}")
print(f"Risk by Zipcode - F-statistic: {f_stat_zipcode}, p-value: {p_value_zipcode}")
print(f"Margin by Zipcode - F-statistic: {f_stat_margin}, p-value: {p_value_margin}")
print(f"Risk by Gender - t-statistic: {t_stat_gender}, p-value: {p_value_gender}")

# Review the results
def review_results(p_value, significance_level=0.05):
    """Review results based on p-value."""
    if p_value < significance_level:
        return "Reject the null hypothesis: Significant difference detected."
    else:
        return "Fail to reject the null hypothesis: No significant difference detected."

print("\nReview of Hypotheses:")
print(f"Risk by Province: {review_results(p_value_province)}")
print(f"Risk by Zipcode: {review_results(p_value_zipcode)}")
print(f"Margin by Zipcode: {review_results(p_value_margin)}")
print(f"Risk by Gender: {review_results(p_value_gender)}")
