import requests
from bs4 import BeautifulSoup
import csv

def get_product_details(product_url):
    try:
        response = requests.get(product_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        product_items = soup.find_all('div', {'data-component-type': 's-search-result'})

        product_details = []
        for item in product_items:
            title_elem = item.find('span', {'class': 'a-text-normal'})
            title = title_elem.text.strip() if title_elem else ''

            asin = item['data-asin']

            product_desc_elem = item.find('span', {'class': 'a-size-base-plus a-color-base a-text-normal'})
            product_description = product_desc_elem.text.strip() if product_desc_elem else ''

            manufacturer_elem = item.find('span', {'class': 'a-size-base'})
            manufacturer = manufacturer_elem.text.strip() if manufacturer_elem else ''

            product_details.append([title, asin, product_description, manufacturer])

        return product_details
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None

if __name__ == "__main__":
    amazon_url = "https://www.amazon.in/Number-Backpack-Compartment-Charging-Organizer/dp/B09VTDMRY7/ref=sr_1_1_sspa?keywords=bags&qid=1690271434&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1"
    product_urls = [f"{amazon_url}&page={page}" for page in range(1, 11)]  # Scrape 10 pages (approximately 200 products)
    
    all_product_details = []
    for url in product_urls:
        product_details = get_product_details(url)
        if product_details:
            all_product_details.extend(product_details)

    # Export data to a CSV file
    with open('amazon_product_details.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Title', 'ASIN', 'Product Description', 'Manufacturer'])
        csv_writer.writerows(all_product_details)

    print("Data exported successfully to amazon_product_details2.csv")
