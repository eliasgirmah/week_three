# src/ab_testing.py

import pandas as pd
from scipy import stats

def test_risk_by_province(data):
    """Test for differences in risk by province."""
    provinces = data['Province'].unique()
    province_risks = data.groupby('Province')['TotalClaims'].mean()
    f_stat, p_value = stats.f_oneway(*[data[data['Province'] == prov]['TotalClaims'].dropna() for prov in provinces])
    return f_stat, p_value

def test_risk_by_zipcode(data):
    """Test for differences in risk by postal code."""
    postal_codes = data['PostalCode'].unique()
    postal_code_risks = data.groupby('PostalCode')['TotalClaims'].mean()
    f_stat, p_value = stats.f_oneway(*[data[data['PostalCode'] == code]['TotalClaims'].dropna() for code in postal_codes])
    return f_stat, p_value

def test_margin_by_zipcode(data):
    """Test for differences in profit margin by postal code."""
    postal_codes = data['PostalCode'].unique()
    postal_code_margins = data.groupby('PostalCode')['CalculatedPremiumPerTerm'].mean()
    f_stat, p_value = stats.f_oneway(*[data[data['PostalCode'] == code]['CalculatedPremiumPerTerm'].dropna() for code in postal_codes])
    return f_stat, p_value

def test_risk_by_gender(data):
    """Test for differences in risk by gender."""
    gender_groups = data['Gender'].unique()
    gender_risks = data.groupby('Gender')['TotalClaims'].mean()
    t_stat, p_value = stats.ttest_ind(
        data[data['Gender'] == gender_groups[0]]['TotalClaims'].dropna(),
        data[data['Gender'] == gender_groups[1]]['TotalClaims'].dropna()
    )
    return t_stat, p_value
