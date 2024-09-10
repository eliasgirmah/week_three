import sys
import os

# Add the parent directory of the project to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)

# src/eda.py

def basic_summary_stats(df):
    return df.describe()

def column_data_types(df):
    return df.dtypes

def univariate_analysis(df, column):
    return df[column].value_counts()

def correlation_matrix(df):
    return df.corr()
