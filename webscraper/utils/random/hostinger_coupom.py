import json
from bs4 import BeautifulSoup


def get_hostinger_coupons():
    json_file_path = "C:\\Users\\luizm\\webscraper\\response.json"

    try:
        # Load HTML content from the JSON file
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            html_content = data['body']  # Assuming 'body' contains the HTML content

        # Print the HTML content for analysis
        print(html_content)

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Adjust the parsing logic based on the actual HTML structure
        # Assuming 'coupon-code' is the correct class
        coupons = soup.find_all(class_='coupon-code')
        coupon_data = []

        for coupon in coupons:
            # Extract and append coupon details
            # Adjust these based on actual structure
            code = coupon.find(class_='code').get_text()
            description = coupon.find(class_='description').get_text()
            coupon_data.append({'code': code, 'description': description})

        # Optionally save to a file or return the data
        with open('coupons.json', 'w') as file:
            json.dump(coupon_data, file)

    except json.JSONDecodeError as json_err:
        print(f'JSON decode error: {json_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

# Call the function to execute the code
get_hostinger_coupons()
