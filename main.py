import requests
from bs4 import BeautifulSoup

# Function to scrape product data from a single page
def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    products = []

    # Find all the product containers on the page
    product_containers = soup.find_all('div', {'data-component-type': 's-search-result'})
    
    for container in product_containers:
        product_info = {}
        
        # Extract product URL
        product_url = container.find('a', {'class': 'a-link-normal'})['href']
        product_info['Product URL'] = 'https://www.amazon.in' + product_url
        
        # Extract product name
        product_name = container.find('span', {'class': 'a-text-normal'}).text.strip()
        product_info['Product Name'] = product_name
        
        # Extract product price
        product_price = container.find('span', {'class': 'a-offscreen'}).text.strip()
        product_info['Product Price'] = product_price
        
        # Extract rating (if available)
        product_rating = container.find('span', {'class': 'a-icon-alt'})
        if product_rating:
            product_info['Rating'] = product_rating.text
            
        # Extract number of reviews (if available)
        num_reviews = container.find('span', {'class': 'a-size-base'})
        if num_reviews:
            product_info['Number of Reviews'] = num_reviews.text
        
        products.append(product_info)

    return products

# Main scraping function
def scrape_amazon_products(keyword, num_pages
                           ):
    base_url = f'https://www.amazon.in/s?k={keyword.replace(" ", "+")}&ref=nb_sb_noss'
    
    all_products = []
    
    for page in range(1, num_pages + 1):
        page_url = f'{base_url}&page={page}'
        products = scrape_page(page_url)
        all_products.extend(products)
    
    return all_products

# Call the main function to scrape products from multiple pages
keyword = 'bags'
num_pages = 20
scraped_data = scrape_amazon_products(keyword, num_pages)

# Print the scraped data
for product in scraped_data:
    print(product)
