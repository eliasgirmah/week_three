import sys
import os

# Add the scripts folder to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))

from load_data import load_data_from_postgres

# src/user_analysis.py
#from scripts.load_data import load_data_from_postgres

def get_top_10_handsets():
    """
    Get the top 10 handsets used by customers.
    :return: DataFrame of top 10 handsets.
    """
    query = '''
    SELECT "Handset Type", COUNT(*) as usage_count
    FROM xdr_data
    GROUP BY "Handset Type"
    ORDER BY usage_count DESC
    LIMIT 10;
    '''
    return load_data_from_postgres(query)

def get_top_3_manufacturers():
    """
    Get the top 3 handset manufacturers.
    :return: DataFrame of top 3 manufacturers.
    """
    query = '''
    SELECT "Handset Manufacturer", COUNT(*) as usage_count
    FROM xdr_data
    GROUP BY "Handset Manufacturer"
    ORDER BY usage_count DESC
    LIMIT 3;
    '''
    return load_data_from_postgres(query)

def get_top_5_handsets_per_manufacturer():
    """
    Get the top 5 handsets for each of the top 3 manufacturers.
    :return: DataFrame of top 5 handsets per manufacturer.
    """
    query = '''
    SELECT "Handset Manufacturer", "Handset Type", COUNT(*) as usage_count
    FROM xdr_data
    WHERE "Handset Manufacturer" IN (
        SELECT "Handset Manufacturer"
        FROM xdr_data
        GROUP BY "Handset Manufacturer"
        ORDER BY COUNT(*) DESC
        LIMIT 3
    )
    GROUP BY "Handset Manufacturer", "Handset Type"
    ORDER BY "Handset Manufacturer", usage_count DESC
    LIMIT 5;
    '''
    return load_data_from_postgres(query)

def aggregate_user_data():
    """
    Aggregate user data including session metrics and application usage.
    :return: DataFrame of aggregated user data.
    """
    query = '''
    SELECT "MSISDN/Number" as user_id, COUNT("Bearer Id") as num_sessions, 
           SUM("Dur. (ms)") as total_duration,
           SUM("Total DL (Bytes)") as total_download, SUM("Total UL (Bytes)") as total_upload,
           SUM("Social Media DL (Bytes)") as social_media_data, 
           SUM("Google DL (Bytes)") as google_data,
           SUM("Email DL (Bytes)") as email_data, 
           SUM("Youtube DL (Bytes)") as youtube_data,
           SUM("Netflix DL (Bytes)") as netflix_data, 
           SUM("Gaming DL (Bytes)") as gaming_data,
           SUM("Other DL (Bytes)") as other_data
    FROM xdr_data
    GROUP BY user_id;
    '''
    return load_data_from_postgres(query)
