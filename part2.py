import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape additional details from a product URL


def scrape_product_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    product_details = {}

    # Extract ASIN from the URL
    asin = url.split('/')[-1]
    product_details['ASIN'] = asin
    print(asin)
    # Extract product description
    product_description = soup.find('meta', {'name': 'description'})['content']
    product_details['Product Description'] = product_description

    # Extract manufacturer
    manufacturer = soup.find('a', {'id': 'bylineInfo'})
    if manufacturer:
        product_details['Manufacturer'] = manufacturer.text.strip()

    # Extract product details
    product_details_section = soup.find(
        'div', {'id': 'productDetails_feature_div'})
    if product_details_section:
        product_details_list = product_details_section.find_all('li')
        for detail in product_details_list:
            detail_text = detail.text.strip()
            if 'Manufacturer' in detail_text:
                product_details['Manufacturer'] = detail_text.replace(
                    'Manufacturer:', '').strip()

    return product_details

# Main scraping function


def scrape_and_export_to_csv(products):
    with open('product_details.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Product URL', 'Description',
                      'ASIN', 'Product Description', 'Manufacturer']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for product in products:
            product_url = product['Product URL']
            product_details = scrape_product_details(product_url)

            # Add basic details
            product_details['Product URL'] = product_url
            product_details['Description'] = product['Product Name']

            # Write to CSV
            writer.writerow(product_details)


# Replace this with your scraped product URLs
product_urls = [
    'https://www.amazon.in/dp/B08VSH3WCW',
    'https://www.amazon.in/dp/B07R44CWGC',
    # Add more URLs here
]

# Call the main function to scrape and export to CSV
scrape_and_export_to_csv(product_urls)
