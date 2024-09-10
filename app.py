import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database connection
def get_engine():
    return create_engine(f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}')

# Load data from PostgreSQL
@st.cache_data
def load_data():
    engine = get_engine()
    query = """
    SELECT 
        * 
    FROM xdr_data;
    """
    return pd.read_sql(query, engine)

# Ensure columns are properly converted to datetime
def preprocess_data(df):
    if 'Start' in df.columns:
        df['Start'] = pd.to_datetime(df['Start'], errors='coerce')
    if 'End' in df.columns:
        df['End'] = pd.to_datetime(df['End'], errors='coerce')
    return df

# Dashboard layout
def main():
    st.title('Telecom Data Analysis Dashboard')

    # Load and preprocess data
    data = load_data()
    data = preprocess_data(data)

    # Sidebar for filters
    st.sidebar.title("Filters")
    
    # Handle manufacturer filter
    st.sidebar.markdown("### Filter by Handset Manufacturer")
    manufacturer = st.sidebar.selectbox('Select Handset Manufacturer', 
                                        ['All'] + list(data['Handset Manufacturer'].dropna().unique()))

    # Handle date range filter
    st.sidebar.markdown("### Filter by Date Range")
    if 'Start' in data.columns and 'End' in data.columns:
        start_date = st.sidebar.date_input('Start Date', value=data['Start'].min().to_pydatetime())
        end_date = st.sidebar.date_input('End Date', value=data['End'].max().to_pydatetime())
    else:
        st.sidebar.write("Date columns are not available in the data.")

    # Filter data
    if 'Start' in data.columns and 'End' in data.columns:
        filtered_data = data[(data['Start'] >= pd.Timestamp(start_date)) & (data['End'] <= pd.Timestamp(end_date))]
    else:
        filtered_data = data

    if manufacturer != 'All':
        filtered_data = filtered_data[filtered_data['Handset Manufacturer'] == manufacturer]

    # Display key insights
    st.markdown("### Key Performance Indicators (KPIs)")
    st.write("Total Records:", filtered_data.shape[0])
    st.write("Average Total DL (Bytes):", round(filtered_data['Total DL (Bytes)'].mean(), 2) if 'Total DL (Bytes)' in filtered_data.columns else "N/A")
    st.write("Average Total UL (Bytes):", round(filtered_data['Total UL (Bytes)'].mean(), 2) if 'Total UL (Bytes)' in filtered_data.columns else "N/A")

    # Data distribution by handset manufacturer
    st.markdown("### Data Distribution by Handset Manufacturer")
    if 'Handset Manufacturer' in filtered_data.columns:
        distribution_by_manufacturer = filtered_data.groupby('Handset Manufacturer')['Total DL (Bytes)'].sum().sort_values(ascending=False)
        st.bar_chart(distribution_by_manufacturer)
    else:
        st.write("Handset Manufacturer data is not available.")

    # Time series analysis
    st.markdown("### Data Traffic Over Time")
    if 'Start' in filtered_data.columns:
        time_series_data = filtered_data.groupby('Start')['Total DL (Bytes)'].sum()
        st.line_chart(time_series_data)
    else:
        st.write("Start date data is not available.")

    # Data distribution
    st.markdown("### Distribution of Total DL (Bytes)")
    if 'Total DL (Bytes)' in filtered_data.columns:
        fig, ax = plt.subplots()
        sns.histplot(filtered_data['Total DL (Bytes)'], kde=True, ax=ax)
        st.pyplot(fig)
    else:
        st.write("Total DL (Bytes) data is not available.")

    # Download option
    st.markdown("### Download Filtered Data")
    csv = filtered_data.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='filtered_data.csv',
        mime='text/csv'
    )

if __name__ == "__main__":
    main()
