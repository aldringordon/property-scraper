import time
import http.client
from http.client import IncompleteRead
from bs4 import BeautifulSoup
import json

from DynamicScraper import Scraper
from Property import Property


def get_auth_headers():
    # Read in the auth headers from a json file return None if it fails
    filename = 'RealEstateComAu-Auth.json'
    try:
        with open(filename, 'r') as f:
            auth_headers = json.load(f)
        return auth_headers
    except FileNotFoundError:
        print(f'{filename} not found')
        return None


def get_price_range():
    price = input('Enter Price: ')
    price_range = f'between-0-{price}'
    return price_range


def get_suburb():
    suburb = input('Enter Suburb: ')
    return suburb


def get_initial_href(price, suburb):
    href = f'/buy/{price}-in-{suburb},+wa/list-1?numParkingSpaces=1&activeSort=price-desc'
    return href


def display_all_properties(properties):
    for property in properties:
        property.print_property()


def write_all_properties_to_json(properties):
    filename = 'RealEstateComAu-Properties-Output.json'
    with open(filename, 'w') as f:
        json.dump([property.get_property() for property in properties], f)


def main():

    print('starting...')
    price = get_price_range()
    suburb = get_suburb()

    # Initial Search Href
    initial_search_href = get_initial_href(price, suburb)
    search_href = initial_search_href

    print('Retrieving auth headers...')
    headers = get_auth_headers()

    payload = ""

    website_url = "www.realestate.com.au"

    scraper = Scraper(website_url, headers, payload)

    # Tracking
    pages_searched = 0
    properties_found = 0

    properties = []

    print(f'Beginning Search for: {search_href}')
    keep_on_keeping = True
    while keep_on_keeping:

        soup = scraper.scrape(search_href)

        # Todo: Add a check to see if the search returned any results

        for card in soup.find_all("div", {"class": "residential-card__content"}):

            house_info = card.find("div", {"class": "piped-content__inner"})
            property_details = []
            for property_detail in house_info.find_all("div"):
                detail = property_detail.get("aria-label")
                if detail:
                    property_details.append(detail)

            address_card = card.find(
                "a", {"class": "details-link residential-card__details-link"})
            address = address_card.find("span").text

            property_type = card.find(
                "span", {"class": "residential-card__property-type"}).text
            address_href = address_card.get("href")

            price = card.find("span", {"class": "property-price"}).text

            property = Property(address, price, property_type,
                                property_details, address_href)

            properties.append(property)

            properties_found += 1

        pages_searched += 1

        # Check if theres another page:
        next_button = soup.find('a', {'title': 'Go to Next Page'})
        if next_button:
            search_href = next_button.get('href')
            print('\nscraping next page...')
        else:
            keep_on_keeping = False

    # Ask user if they want to display all properties
    display = input('Display all properties? (y/n): ')
    if display == 'y':
        display_all_properties(properties)

    # Ask user if they want to write all properties to a json file
    write = input('Write all properties to a json file? (y/n): ')
    if write == 'y':
        write_all_properties_to_json(properties)

    print()
    print(f'Scraper Stats: {scraper.get_stats()}')
    print()
    print(f'Pages Searched: {pages_searched}')
    print(f'Properties Searched: {properties_found}')
    print(f'Original Search: https://{website_url}{initial_search_href}')
    print()


if __name__ == '__main__':
    main()
