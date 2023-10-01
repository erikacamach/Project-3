import sqlite3
import pandas as pd
from pathlib import Path

# Read the CSV file
csv_file_path = 'cities.csv'
df = pd.read_csv(csv_file_path)

# Clean column names by stripping whitespaces
df.columns = df.columns.str.strip()

# Specify the SQLite database file path
database_path = 'cities.db'

# Connect to SQLite database
conn = sqlite3.connect(database_path)

# Convert the DataFrame to an SQLite table (replace if exists)
df.to_sql('cities', conn, if_exists='replace', index=False)

# Close the connection
conn.close()

