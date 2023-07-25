import requests
from bs4 import BeautifulSoup
import csv

def scrape_products_from_page(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    products = []
    product_cards = soup.find_all('div', {'data-component-type': 's-search-result'})

    for card in product_cards:
        try:
            product_url = card.find('a', {'class': 'a-link-normal'})['href']
            product_name = card.find('span', {'class': 'a-size-medium'}).text.strip()
            product_price = card.find('span', {'class': 'a-offscreen'}).text.strip()
            rating = card.find('span', {'class': 'a-icon-alt'}).text.strip()
            num_reviews = card.find('span', {'class': 'a-size-base'}).text.strip()

            products.append({
                'Product URL': product_url,
                'Product Name': product_name,
                'Product Price': product_price,
                'Rating': rating,
                'Number of Reviews': num_reviews,
            })
        except Exception as e:
            print(f"Error parsing product: {e}")

    return products

def scrape_multiple_pages(base_url, num_pages=20):
    all_products = []
    for page_number in range(1, num_pages + 1):
        page_url = f"{base_url}&page={page_number}"
        print(f"Scraping page {page_number}...")
        products = scrape_products_from_page(page_url)
        all_products.extend(products)

    return all_products

if __name__ == "__main__":
    base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
    num_pages_to_scrape = 20

    scraped_data = scrape_multiple_pages(base_url, num_pages=num_pages_to_scrape)

    # Save the data to a CSV file
    with open('amazon_bags_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(scraped_data)

    print("Scraping completed. Data saved to amazon_bags_data.csv.")
