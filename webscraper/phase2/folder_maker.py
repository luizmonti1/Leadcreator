import json
import os
import urllib.parse

def create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def save_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def populate_template_with_basic_data(client_folder, template):
    """Populate the template with data from a client's consolidated data file."""

    consolidated_data_path = os.path.join(client_folder, 'consolidated_data.json')

    if not os.path.exists(consolidated_data_path):
        print(f"No consolidated data file found for client in {client_folder}")
        return template

    with open(consolidated_data_path, 'r', encoding='utf-8') as file:
        client_data = json.load(file)

    template["url"] = client_data.get("url", "URL not found")
    template["segment"] = client_data.get("segment", "Segment not found")
    template["seo_status"] = client_data.get("seo_status", {})
    template["load_time"] = client_data.get("load_time", {})
    template["design_status"] = client_data.get("design_status", {})
    template["pwa_features_status"] = client_data.get("pwa_features_status", {})
    template["emails"] = client_data.get("emails", [])

    return template

def main():
    base_dir = 'C:\\Users\\luizm\\webscraper\\clientes'
    create_directory(base_dir)

    # Load company data and email data
    with open('C:\\Users\\luizm\\webscraper\\extracted_data.json', 'r') as file:
        company_data = json.load(file)

    with open('C:\\Users\\luizm\\webscraper\\phase2\\final_data.json', 'r') as file:
        email_data = json.load(file)
    
    email_lookup = {item['url']: item.get('emails', []) for item in email_data}

    for company in company_data:
        url = company['url']
        company_name = urllib.parse.urlparse(url).netloc
        company_dir = os.path.join(base_dir, company_name)
        create_directory(company_dir)

        # Populate the template with basic data (URL, segment, emails, etc.)
        populated_data = populate_template_with_basic_data(company_dir, company)
        populated_data['emails'] = email_lookup.get(url, [])

        # Save the populated data
        save_json(populated_data, os.path.join(company_dir, 'consolidated_data.json'))

if __name__ == "__main__":
    main()
