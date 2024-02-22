import csv

# Paths to the input and output files
input_csv_file = "C:\\Users\\luizm\\webscraper\\phase2\\score_list.csv"
output_csv_file = "C:\\Users\\luizm\\webscraper\\phase2\\filtered_low_scores.csv"

def filter_websites(input_file, output_file):
    filtered_websites = []

    with open(input_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader, None)  # Read the header

        for row in reader:
            try:
                if row[0].startswith('https://'):  # Check if the row starts with 'https://'
                    total_score = float(row[-1])  # Assuming total score is the last column
                    if 0 < total_score < 4:
                        filtered_websites.append(row[:2] + [total_score])  # Assuming URL is the first column
            except (ValueError, IndexError):
                # Handle the case where conversion to float fails or row format is incorrect
                continue

    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['URL', 'Total Score'])

        for website in filtered_websites:
            writer.writerow(website)

    print("Filtered data processed and saved to", output_file)

# Run the function
filter_websites(input_csv_file, output_csv_file)
