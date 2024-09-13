import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define EDA Functions

def descriptive_statistics(df, numerical_columns):
    descriptive_stats = df[numerical_columns].describe()
    return descriptive_stats

def plot_histogram(df, column, title, output_folder):
    plt.figure(figsize=(8, 5))
    sns.histplot(df[column], kde=True, bins=30)
    plt.title(f'Distribution of {title}')
    plt.savefig(f'{output_folder}/{title}_histogram.png')
    plt.close()

def plot_bar(df, column, title, output_folder):
    plt.figure(figsize=(8, 5))
    sns.countplot(x=column, data=df)
    plt.title(f'{title} Distribution')
    plt.savefig(f'{output_folder}/{title}_bar.png')
    plt.close()

# More functions for scatter, box plots, etc.
