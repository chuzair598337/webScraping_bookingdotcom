import requests
from bs4 import BeautifulSoup
import openpyxl
import os

def create_excel_file(file_path):
    # Ensure the output folder exists
    folder = os.path.dirname(file_path)
    if not os.path.exists(folder):
        os.makedirs(folder)  # Create the folder if it doesn't exist

    # Create the Excel file
    if not os.path.exists(file_path):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Properties"
        sheet.append([
            "Title", "Image Link", "URL Link", "Star Rating", "Map Link", "Review Rating", "Review Comment", "ReviewBy Count"
        ])
        workbook.save(file_path)

def append_to_excel(file_path, data):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    for row in data:
        sheet.append(row)
    workbook.save(file_path)

def extract_properties(soup):
    results = []

    # Total properties found
    total_properties_div = soup.find('h1', class_='f6431b446c d5f78961c3')
    total_properties = total_properties_div.text if total_properties_div else "Unknown"

    # Extract property cards
    property_cards = soup.find_all('div', {'data-testid': 'property-card'})

    for card in property_cards:
        try:
            # Image link
            image_div = card.find('div', class_='a5922b8ca1')
            image_tag = image_div.find('img') if image_div else None
            image_link = image_tag['src'] if image_tag else ""

            # URL link
            url_tag = image_div.find('a') if image_div else None
            url_link = url_tag['href'] if url_tag else ""

            # Title
            title_div = card.find('div', {'data-testid': 'title'})
            title = title_div.text.strip() if title_div else ""

            # Star Rating
            star_div = card.find('div', class_='b3f3c831be')
            star_rating = star_div['aria-label'] if star_div else ""

            # Map Link
            map_div = card.find('div', class_='abf093bdfe ecc6a9ed89')
            map_link_tag = map_div.find('a') if map_div else None
            map_link = map_link_tag['href'] if map_link_tag else ""

            # Review Score, Comment, and Count
            review_div = card.find('div', {'data-testid': 'review-score'})

            review_score_div = review_div.find('div', class_='ac4a7896c7') if review_div else None
            review_score = review_score_div.text.strip() if review_score_div else ""

            review_comment_div = review_div.find('div', class_='a3b8729ab1 e6208ee469 cb2cbb3ccb') if review_div else None
            review_comment = review_comment_div.text.strip() if review_comment_div else ""

            review_count_div = review_div.find('div', class_='abf093bdfe f45d8e4c32 d935416c47') if review_div else None
            review_count = review_count_div.text.strip() if review_count_div else ""

            results.append([
                title, image_link, url_link, star_rating, map_link, review_score, review_comment, review_count
            ])
        except Exception as e:
            print(f"Error processing a property card: {e}")

    return total_properties, results

def main():
    base_url = "https://www.booking.com/searchresults.html"
    file_path = "output/properties.xlsx"

    # Input country from user
    country = input("Enter the country: ")

    # Prepare the search request
    params = {
        'ss': country,
        'checkin_monthday': 25,
        'checkin_year_month': '2024-12',
        'checkout_monthday': 26,
        'checkout_year_month': '2024-12',
        'group_adults': 2,
        'no_rooms': 1,
        'group_children': 0
    }

    # Send request
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        print("Error fetching the page")
        return

    # Parse HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract properties
    total_properties, properties = extract_properties(soup)

    # Print total properties
    print(f"Total properties found: {total_properties}")

    # Save data to Excel
    create_excel_file(file_path)
    append_to_excel(file_path, properties)

    print(f"Data saved to {file_path}")

if __name__ == "__main__":
    main()
