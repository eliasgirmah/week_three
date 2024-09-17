import os
import pandas as pd
#S  from src.eda import descriptive_statistics, plot_histogram, plot_bar
import sys
import os

# Add the project root directory to Python's path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import from the 'src' folder
from src.eda import descriptive_statistics, plot_histogram, plot_bar

# Define paths
data_path = 'data/dataset.csv'
output_folder = 'output/eda_figures'

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Load the dataset
df = pd.read_csv(data_path)

# Numerical columns for descriptive stats
numerical_columns = ['TotalPremium', 'TotalClaims']

# Perform EDA
descriptive_stats = descriptive_statistics(df, numerical_columns)
print(descriptive_stats)

# Save visualizations
plot_histogram(df, 'TotalPremium', 'Total Premium', output_folder)
plot_bar(df, 'Gender', 'Gender', output_folder)

# Add more plots as needed
