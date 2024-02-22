import sqlite3
import json

# Path to your database
database_path = 'C:\\Users\\luizm\\webscraper\\web_analysis.db'

# Connect to the SQLite database
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

# Execute query to fetch data
query = "SELECT * FROM websites"  # Adjusted to your table name
cursor.execute(query)

# Fetch all rows
rows = cursor.fetchall()

# Transform data into desired JSON structure
data = []
for row in rows:
    try:
        # Convert JSON strings in specific columns
        seo_status = json.loads(row[2]) if row[2] else {}
        load_time = json.loads(row[3]) if row[3] else {}
        design_status = json.loads(row[4]) if row[4] else {}
        pwa_features_status = json.loads(row[5]) if row[5] else {}
    except json.JSONDecodeError:
        # Handle invalid JSON strings
        seo_status = {}
        load_time = {}
        design_status = {}
        pwa_features_status = {}

    entry = {
        "url": row[0],
        "segment": row[1],
        "seo_status": seo_status, 
        "load_time": load_time,
        "design_status": design_status,
        "pwa_features_status": pwa_features_status
    }
    data.append(entry)

# Close the database connection
conn.close()


# Write data to JSON file
with open('C:\\Users\\luizm\\webscraper\\extracted_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, indent=4)

print("Data extraction complete and saved to extracted_data.json")
