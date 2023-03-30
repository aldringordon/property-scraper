import time
import http.client
from http.client import IncompleteRead
from bs4 import BeautifulSoup
import json

TOTAL_REQUESTS = 0
FAILED_REQUESTS = 0


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


def scrape(href, headers, attempt=0):

    try:
        conn = http.client.HTTPSConnection("www.realestate.com.au")
        payload = ""

        print('Making request...')
        conn.request("GET", href, payload, headers)

        print('Waiting for response...')
        time.sleep(1)

        print('Getting response...')
        r = conn.getresponse()

        print('Reading response...')
        soup = BeautifulSoup(r, "html.parser")

        conn.close()

    except IncompleteRead:
        conn.close()

        # Oh well, reconnect and keep trucking
        print(f'\n\tAttempt({attempt}) - Incomplete Read  - ({href})')
        print('\tRecursively Trying Again lol..')
        return scrape(href, headers, attempt=attempt+1)

    print('Returning data...')
    return soup


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


def main():

    print('starting...')
    price = get_price_range()
    suburb = get_suburb()

    # Initial Search Href
    search_href = get_initial_href(price, suburb)

    # Tracking
    pages_searched = 0
    properties_found = 0

    print('Retrieving auth headers...')
    headers = get_auth_headers()

    print(f'Beginning Search for: {search_href}')

    keep_on_keeping = True
    while keep_on_keeping:

        soup = scrape(search_href, headers)

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

            print('\n------')
            print(f'Address: {address}')
            print(f'Price: {price}')
            print(f'Type: {property_type}')
            print('Property_Details:')
            for x in property_details:
                print(f'\t{x}')
            print(f'URL: https://www.realestate.com.au{address_href}')

            properties_found += 1

        pages_searched += 1

        # Check if theres another page:
        next_button = soup.find('a', {'title': 'Go to Next Page'})
        if next_button:
            search_href = next_button.get('href')
            print('\nscraping next page...')
        else:
            keep_on_keeping = False

    print()
    print(f'Pages Searched: {pages_searched}')
    print(f'Properties Searched: {properties_found}')
    print(f'Original Search: {search_href}')
    print()
    print(f'Total Requests: {TOTAL_REQUESTS}')
    print(f'Failed Requests: {FAILED_REQUESTS}')


if __name__ == '__main__':
    main()
