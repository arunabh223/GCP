from google.cloud import bigquery
from google.oauth2 import service_account
import pandas_gbq
import pandas as pd
import config as cfg
import os 
import configparser

# Set up the environment variable for authentication
# Read the configuration file
config = configparser.ConfigParser()
config.read('config.cfg')

# Get the path to the service account key from the configuration file
creds_path = config.get('google', 'creds')

# Set up the environment variable for authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path

# First SQL query: To see the total sales by the Product Line type
query_string_1 = """ 
SELECT `Product line`, SUM(Total) AS Total_sales
FROM `project-2-434009.Datasets.SupermarketSales`
GROUP BY `Product line`
ORDER BY SUM(Total) DESC
LIMIT 1000
"""

# Second SQL query: See the Total sales based on Customer type
query_string_2 = """ 
SELECT `Customer type`, SUM(Total) AS Total
FROM `project-2-434009.Datasets.SupermarketSales` 
GROUP BY `Customer type`
ORDER BY Total DESC
LIMIT 1000
"""

# Second SQL query: See the Total sales based on Customer type
query_string_3 = """ 
SELECT Gender, `Product line`, SUM(Total) AS Total
FROM `project-2-434009.Datasets.SupermarketSales` 
GROUP BY `Product line`, Gender
ORDER BY Gender
LIMIT 1000
"""

# Initialize BigQuery client
bq_client = bigquery.Client()

# Execute the first query and save the result in the first DataFrame
df_productline = bq_client.query(query_string_1).to_dataframe()

# Execute the second query and save the result in the second DataFrame
df_member_sales = bq_client.query(query_string_2).to_dataframe()

# Execute the third query and save the result in the third DataFrame
df_gender_sales = bq_client.query(query_string_3).to_dataframe()

# Exporting the DataFrames to CSV files
df_productline.to_csv('data/productline_sales.csv', index=False)
df_member_sales.to_csv('data/member_sales.csv', index=False)
df_gender_sales.to_csv('data/gender_sales.csv', index=False)