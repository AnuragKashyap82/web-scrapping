import pandas as pd
import sqlite3

# Load CSV file into DataFrame
csv_file = 'new_car_details.csv'
df = pd.read_csv(csv_file)

# Create SQLite database
conn = sqlite3.connect('mergedFileTaxiDataBase.db')
df.to_sql('car_table', conn, if_exists='replace', index=False)

# Close the connection
conn.close()
