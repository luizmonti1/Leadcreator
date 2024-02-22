import json
import csv
import logging

# Setup logging
logging.basicConfig(filename='data_processing_errors.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# File paths
input_file = "C:\\Users\\luizm\\webscraper\\extracted_data.json"
output_csv_file = "C:\\Users\\luizm\\webscraper\\phase2\\score_list.csv"

# Read JSON data
with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Prepare data for CSV
csv_rows = []

# Processing each website's data
for entry in data:
    try:
        url = entry.get("url", "")
        segment = entry.get("segment", "")

        # Scores - using .get() to avoid KeyError
        seo_score = entry.get("seo_status", {}).get("seo_status", {}).get("basic_seo_score", 0) or 0
        load_time_score = entry.get("load_time", {}).get("Performance Score", 0) or 0
        mobile_usability_score = entry.get("design_status", {}).get("Mobile Usability", {}).get("Mobile Usability Score", 0) or 0
        page_speed_score = entry.get("design_status", {}).get("PageSpeed Insights", {}).get("Performance Score", 0) or 0
        pwa_score = entry.get("pwa_features_status", {}).get("score", 0) or 0

        # Calculate total score and round to two decimal places
        total_score = round(sum([seo_score, load_time_score, mobile_usability_score, page_speed_score, pwa_score]), 2)

        # Append data for the CSV file
        csv_rows.append([url, segment, seo_score, load_time_score, mobile_usability_score, page_speed_score, pwa_score, total_score])
    except Exception as e:
        logging.error(f"Error processing entry for URL {url}: {e}")

# Sort csv_rows first by segment in alphabetical order and then by total score in ascending order
csv_rows_sorted = sorted(csv_rows, key=lambda x: (x[1].lower(), x[7]))

# Write data to CSV
with open(output_csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write headers
    writer.writerow(['URL', 'Segment', 'SEO Score', 'Load Time Performance Score', 'Mobile Usability Score', 'PageSpeed Insights Performance Score', 'PWA Features Score', 'Total Score'])

    # Write each sorted row
    for row in csv_rows_sorted:
        writer.writerow(row)

print("Data processed and sorted by segment and total score and saved to", output_csv_file)
