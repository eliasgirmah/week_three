# scripts/user_engagement.py

import pandas as pd
from scripts.load_data import load_data_from_postgres
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

def aggregate_engagement_data():
    query = '''
    SELECT user_id, COUNT(session_id) as num_sessions, 
           SUM(session_duration) as total_duration,
           SUM(download_data) as total_download, 
           SUM(upload_data) as total_upload
    FROM xdr_data
    GROUP BY user_id;
    '''
    return load_data_from_postgres(query)

def perform_kmeans_clustering(df, n_clusters=3):
    kmeans = KMeans(n_clusters=n_clusters)
    df['cluster'] = kmeans.fit_predict(df[['num_sessions', 'total_duration', 'total_download', 'total_upload']])
    return df, kmeans

def plot_application_usage(df):
    df_app_usage = df[['social_media_data', 'google_data', 'email_data', 'youtube_data', 'netflix_data', 'gaming_data', 'other_data']].sum()
    df_app_usage.plot(kind='bar', figsize=(10, 6))
    plt.title('Top 3 Most Used Applications')
    plt.xlabel('Application')
    plt.ylabel('Total Data Usage (Bytes)')
    plt.show()

# Example usage
if __name__ == "__main__":
    df_engagement = aggregate_engagement_data()
    df_engagement, kmeans_model = perform_kmeans_clustering(df_engagement)
    plot_application_usage(df_engagement)
