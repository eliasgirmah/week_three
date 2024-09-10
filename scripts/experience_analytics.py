# scripts/experience_analytics.py

import pandas as pd
from scripts.load_data import load_data_from_postgres
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

def aggregate_experience_data():
    query = '''
    SELECT user_id, AVG("TCP DL Retrans. Vol (Bytes)") as avg_tcp_dl_retrans,
           AVG("Avg RTT DL (ms)") as avg_rtt_dl,
           AVG("Avg Bearer TP DL (kbps)") as avg_throughput_dl,
           AVG("Avg RTT UL (ms)") as avg_rtt_ul,
           AVG("Avg Bearer TP UL (kbps)") as avg_throughput_ul,
           "Handset Type"
    FROM xdr_data
    GROUP BY user_id, "Handset Type";
    '''
    return load_data_from_postgres(query)

def perform_experience_clustering(df, n_clusters=3):
    kmeans = KMeans(n_clusters=n_clusters)
    df['cluster'] = kmeans.fit_predict(df[['avg_tcp_dl_retrans', 'avg_rtt_dl', 'avg_throughput_dl', 'avg_rtt_ul', 'avg_throughput_ul']])
    return df, kmeans

def plot_throughput_distribution(df):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Handset Type', y='avg_throughput_dl', data=df)
    plt.title('Throughput Distribution per Handset Type')
    plt.xlabel('Handset Type')
    plt.ylabel('Average Throughput (kbps)')
    plt.xticks(rotation=45)
    plt.show()

# Example usage
if __name__ == "__main__":
    df_experience = aggregate_experience_data()
    df_experience, kmeans_model = perform_experience_clustering(df_experience)
    plot_throughput_distribution(df_experience)
