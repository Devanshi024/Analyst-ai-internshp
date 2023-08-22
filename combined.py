import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape product data from a single page
def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    products = []
    
    product_containers = soup.find_all('div', {'data-component-type': 's-search-result'})
    
    for container in product_containers:
        product_info = {}
        
        product_url = container.find('a', {'class': 'a-link-normal'})['href']
        product_info['Product URL'] = 'https://www.amazon.in' + product_url
        product_info['Product Name'] = container.find('span', {'class': 'a-text-normal'}).text.strip()
        product_info['Product Price'] = container.find('span', {'class': 'a-offscreen'}).text.strip()
        
        product_rating = container.find('span', {'class': 'a-icon-alt'})
        if product_rating:
            product_info['Rating'] = product_rating.text
            
        num_reviews = container.find('span', {'class': 'a-size-base'})
        if num_reviews:
            product_info['Number of Reviews'] = num_reviews.text
        
        products.append(product_info)

    return products

# Function to scrape additional details from a product URL
def scrape_product_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    product_details = {}
    
    asin = url.split('/')[-1]
    product_details['ASIN'] = asin
    
    product_description = soup.find('meta', {'name': 'description'})['content']
    product_details['Product Description'] = product_description
    
    manufacturer = soup.find('a', {'id': 'bylineInfo'})
    if manufacturer:
        product_details['Manufacturer'] = manufacturer.text.strip()
    
    product_details_section = soup.find('div', {'id': 'productDetails_feature_div'})
    if product_details_section:
        product_details_list = product_details_section.find_all('li')
        for detail in product_details_list:
            detail_text = detail.text.strip()
            if 'Manufacturer' in detail_text:
                product_details['Manufacturer'] = detail_text.replace('Manufacturer:', '').strip()
    
    return product_details

# Main scraping function
def scrape_amazon_products_and_export(keyword, num_pages):
    base_url = f'https://www.amazon.in/s?k={keyword.replace(" ", "+")}&ref=nb_sb_noss'
    
    all_products = []
    
    for page in range(1, num_pages + 1):
        page_url = f'{base_url}&page={page}'
        products = scrape_page(page_url)
        all_products.extend(products)
    
    with open('product_details.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews', 'Description', 'ASIN', 'Product Description', 'Manufacturer']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for product in all_products:
            product_url = product['Product URL']
            product_details = scrape_product_details(product_url)
            
            product_details['Product URL'] = product_url
            product_details['Description'] = product['Product Name']
            product_details['Product Name'] = product['Product Name']
            product_details['Product Price'] = product['Product Price']
            product_details['Rating'] = product.get('Rating', '')
            product_details['Number of Reviews'] = product.get('Number of Reviews', '')
            
            writer.writerow(product_details)

# Call the main function to scrape products from multiple pages and export to CSV
keyword = 'bags'
num_pages = 20
scrape_amazon_products_and_export(keyword, num_pages)
