import requests
from bs4 import BeautifulSoup
import openpyxl
import os
import urllib.parse
from datetime import datetime


def validate_date(date_str):
    """Validate the date format as YYYY-MM-DD."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def get_valid_input(prompt, validation_func=None, example_value=None):
    """
    Repeatedly prompt the user until they provide valid input.
    Optionally validate the input with a validation function.
    """
    while True:
        user_input = input(f"{prompt} (Example: {example_value}): ").strip()
        if not user_input and example_value:
            user_input = example_value  # Use the hard-coded default if no input
        if validation_func and not validation_func(user_input):
            print(f"Invalid input. Please try again.")
        else:
            return user_input

def generate_booking_link(ss, dest_id, checkin, checkout, group_adults, no_rooms, group_children):
    base_url = "https://www.booking.com/searchresults.html"

    # Parameters from function arguments
    parameters = {
        "ss": ss,
        "label": "gen173nr-1FCAQoggI49ANIM1gEaLUBiAEBmAExuAEHyAEM2AEB6AEB-AECiAIBqAIDuAKi6LC7BsACAdICJDhiMjE3ZWVhLTgxNjQtNDIxOS05OTRjLTM0YmQwNjRkNTY3YdgCBeACAQ",
        "aid": "304142",
        "lang": "en-us",
        "sb": "1",
        "src_elem": "sb",
        "src": "searchresults",
        "dest_id": dest_id,
        "dest_type": "country",
        "ac_position": "0",
        "ac_click_type": "b",
        "ac_langcode": "en",
        "ac_suggestion_list_length": "5",
        "search_selected": "true",
        "search_pageview_id": "a0717491e092030b",
        "ac_meta": "GhBhMDcxNzQ5MWUwOTIwMzBiIAAoATICZW46DVNhdWRpYSBBcmFiaWFAAUoMc2F1ZGkgYXJhYmlhULUB",
        "checkin": checkin,
        "checkout": checkout,
        "group_adults": group_adults,
        "no_rooms": no_rooms,
        "group_children": group_children,
    }

    # Encode parameters and generate the full URL
    query_string = urllib.parse.urlencode(parameters)
    full_url = f"{base_url}?{query_string}"

    return full_url

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

    # Collect validated input from the user
    # country = get_valid_input("Enter the country", example_value="Saudia Arabia")
    # checkin = get_valid_input("Enter check-in date (YYYY-MM-DD)", validate_date, "2024-12-25")
    # checkout = get_valid_input("Enter check-out date (YYYY-MM-DD)", validate_date, "2024-12-26")
    # group_adults = get_valid_input("Enter number of adults", lambda x: x.isdigit() and int(x) > 0, "8")
    # no_rooms = get_valid_input("Enter number of rooms", lambda x: x.isdigit() and int(x) > 0, "3")
    # group_children = get_valid_input("Enter number of children", lambda x: x.isdigit() and int(x) >= 0, "0")

    # Hard-coded data
    country = "Saudia Arabia"
    checkin = "2024-12-25"
    checkout = "2024-12-26"
    group_adults = "2"
    no_rooms = "1"


    custom_link = generate_booking_link(
        ss=country,
        dest_id="0",
        checkin=checkin,
        checkout=checkout,
        group_adults=group_adults,
        no_rooms=no_rooms,
        group_children= "0"
    )

    # custom_link = "https://www.booking.com/searchresults.html"
    custom_link = "https://www.booking.com/searchresults.html?ss=Saudia+Arabia"

    print("\nGenerated Booking Link:")
    print(custom_link)


    # Send request and handle errors
    try:
        # Cookies extracted from your browser
        cookies = {
            "pcm_personalization_disabled": "0",
            "pcm_consent": "consentedAt%3D2024-12-25T19%3A05%3A40.536Z%26countryCode%3DPK%26expiresAt%3D2025-06-23T19%3A05%3A40.536Z%26implicit%3Dfalse%26regionCode%3DPB%26regulation%3Dnone%26legacyRegulation%3Dnone%26consentId%3D00000000-0000-0000-0000-000000000000%26analytical%3Dfalse%26marketing%3Dfalse",
            "aws-waf-token": "a43d4f8c-2469-44bc-a1f6-4571a11e7990:BQoAjyWKBDhtAAAA:GmUWlkxKD68L9fDEBlzVsrWdM1EwkJJUCnkc4NFWkCzuT1KwvGGWqaVZAH9EqajbFXkTXCurMNn2I3GCoEIuip/LXqCpYz08P4E/dyb7LZLTIJ8+WSza9Bwo6QgKFLK6+G+X6Cy1ZfRS6PMEFRCydpOON1vaOrkbVU35SRjy3YocEF3ShqFIDsSwSYldwqCrIUhVWmyaU3p0JaCP0IDUXvZn/sz4Q2tgGibju5hAfppDLx7M3cqtBG7gJc43Pm6GSY8=",
            "OptanonConsent": "isGpcEnabled=0&datestamp=Thu+Dec+26+2024+00%3A33%3A07+GMT%2B0500+(Pakistan+Standard+Time)&version=202403.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=29e3769b-c2af-49e6-8728-3067c567ef16&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1&implicitConsentCountry=nonGDPR&implicitConsentDate=1735153293058&AwaitingReconsent=false"
        }

        # Build the Cookie header
        cookie_header = "; ".join([f"{key}={value}" for key, value in cookies.items()])

        # Headers including the cookies
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            "Cookie": cookie_header
        }

        response = requests.get(custom_link, headers=headers)

        response.raise_for_status()  # Raise exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')

        # Create output directory if it doesn't exist
        output_dir = os.path.join(os.getcwd(), "output")
        os.makedirs(output_dir, exist_ok=True)

        # Save parsed HTML to a file
        output_file_path = os.path.join(output_dir, "index.html")
        with open(output_file_path, "w", encoding="utf-8") as file:
            file.write(soup.prettify())

        print(f"HTML content saved to: {output_file_path}")

        # Extract properties
        total_properties, properties = extract_properties(soup)

        # Print total properties
        print(f"Total properties found: {total_properties}")

        # Save data to Excel
        create_excel_file(file_path)
        append_to_excel(file_path, properties)

        print(f"Data saved to {file_path}")

    except requests.RequestException as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
