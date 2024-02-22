import os
import re
import json
import requests
from bs4 import BeautifulSoup


def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.text
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")


def find_contact_info(soup, base_url):
    # Attempt to find direct contact information first
    contact_info = {
        'phones': [],
        'emails': [],
        'addresses': [],
        'cnpjs': [],
    }

    # Define the missing patterns
    phone_pattern = re.compile(r'\(\d{2}\)\s?9?\d{4}-\d{4}')
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    address_pattern = re.compile(
        r'\b(?:Rua|Avenida|Av|Travessa|Alameda)\b[^,]+,\s*\d+[^,]*,\s*[^,]+-\s*[A-Z]{2}\s*CEP:\s*\d{5}-\d{3}',
        re.IGNORECASE)
    cnpj_pattern = re.compile(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}')

    # If the contact page is just a form, try to find contact info in the footer or homepage
    if not any(contact_info.values()):
        footer = soup.find('footer')
        if footer:
            contact_info['phones'] = list(set(phone_pattern.findall(footer.get_text())))
            contact_info['emails'] = list(set(email_pattern.findall(footer.get_text())))
            contact_info['addresses'] = list(set(address_pattern.findall(footer.get_text())))
            contact_info['cnpjs'] = list(set(cnpj_pattern.findall(footer.get_text())))

        # If still no contact info found, try the homepage
        if not any(contact_info.values()):
            html_content = fetch_html(base_url)
            if html_content:
                homepage_soup = BeautifulSoup(html_content, 'html.parser')
                contact_info['phones'] = list(set(phone_pattern.findall(homepage_soup.get_text())))
                contact_info['emails'] = list(set(email_pattern.findall(homepage_soup.get_text())))
                contact_info['addresses'] = list(set(address_pattern.findall(homepage_soup.get_text())))
                contact_info['cnpjs'] = list(set(cnpj_pattern.findall(homepage_soup.get_text())))

    return contact_info


def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Regular expressions for Brazilian contact information
    phone_pattern = re.compile(r'\(\d{2}\)\s?9?\d{4}-\d{4}')  # Matches (11) 97594-4116 and similar patterns
    cnpj_pattern = re.compile(r'\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}')  # Matches CNPJ format
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    address_pattern = re.compile(
        r'\b(?:Rua|Avenida|Av|Travessa|Alameda)\b[^,]+,\s*\d+[^,]*,\s*[^,]+-\s*[A-Z]{2}\s*CEP:\s*\d{5}-\d{3}',
        re.IGNORECASE)  # Example: "Rua Afonso Pena, 322 São Paulo - SP CEP: 01124-000"

    # Find contact information
    text = soup.get_text()
    phones = set(phone_pattern.findall(text))
    emails = set(email_pattern.findall(text))
    addresses = set(address_pattern.findall(text))
    cnpjs = set(cnpj_pattern.findall(text))

    # Attempt to find a 'contact us' link
    contact_links = soup.find_all('a', href=re.compile(r'/(contato|fale-conosco)', re.IGNORECASE))
    contact_urls = [link['href'] for link in contact_links if 'href' in link.attrs]

    # ... rest of your extraction logic

    return {
        # ... other extracted data
        'phones': list(phones),
        'emails': list(emails),
        'addresses': list(addresses),
        'cnpjs': list(cnpjs),
        'contact_urls': contact_urls,
    }


def update_json_data(client_folder, url, json_data):
    # Fetch HTML content
    html_content = fetch_html(url)

    # If HTML content was successfully fetched
    if html_content:
        # Parse the HTML content
        parsed_data = parse_html(html_content)

        # Update the original JSON data with the new extracted information
        json_data.update(parsed_data)

        # Define the path for final.json in the client's folder
        final_json_path = os.path.join(client_folder, 'final.json')

        # Save the updated JSON data back to final.json
        with open(final_json_path, 'w', encoding='utf-8') as file:
            json.dump(json_data, file, indent=4)

        print(f"Updated data saved to {final_json_path}")
    else:
        print(f"Failed to fetch HTML content for {url}")


def main(base_dir):
    # Loop through client folders and update each with scraped HTML data
    for client_name in os.listdir(base_dir):
        client_folder = os.path.join(base_dir, client_name)
        json_file_path = os.path.join(client_folder, 'consolidated_data.json')

        if os.path.isfile(json_file_path):
            with open(json_file_path, 'r') as json_file:
                client_data = json.load(json_file)

            # Extract the URL from the client data
            url = client_data.get('url')
            update_json_data(client_folder, url, client_data)


if __name__ == '__main__':
    # Define the base directory where client folders are located
    base_client_dir = 'C:\\Users\\luizm\\webscraper\\clientes'
    main(base_client_dir)
