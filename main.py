# Scraping Winnetka on realtor.com
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time


# Filtration System
print('Enter the amount you want to buy a house like this -> 1000000 (for a one million dollar house)')
price_filter = int(input(''))
print(f'Retrieving houses over {price_filter}')



def find_houses():
    # Start a web driver
    driver = webdriver.Chrome('--ignore-certificate-errors')
    driver.get('https://www.realtor.com/realestateandhomes-search/Winnetka_IL')
    html_text = driver.page_source # Get the HTML source code

    # Function for extracting text for the variables beds, baths, square_foot, and acre_lot
    # that some listings don't include these specific variables
    def extract_text(home, attr):
        element = home.find('li', attrs={'class': 'jsx-946479843 prop-meta srp_list', 'data-label': attr})
        if element is not None:
            return element.text
        else:
            return ''
    
    houses_list = [] # For dataframe

    soup = BeautifulSoup(html_text, 'lxml')
    homes = soup.find_all('li', class_ = 'jsx-1881802087 component_property-card') # For all home listings on first page
    for home in homes: 
        addresses = home.find('div', class_ = 'jsx-11645185 address ellipsis srp-page-address srp-address-redesign').text
        status_texts = home.find('span', class_ = 'jsx-3853574337 statusText').text
        
        prices = home.find('span', attrs={'class': 'Price__Component-rui__x3geed-0 gipzbd', 'data-label': 'pc-price'}).text
        prices = int(prices.replace('$', '').replace(',', '')) # removes the $ sign and commas and convert to float

        beds = extract_text(home, 'pc-meta-beds')
        baths = extract_text(home, 'pc-meta-baths')
        square_feet = extract_text(home, 'pc-meta-sqft')
        acre_lot = extract_text(home, 'pc-meta-sqftlot')
        more_info_link = home.div.a['href'] # to get the href link for more information on each house
        

        # Uncomment first if-statement for house prices below the value entered
        # if prices <= price_filter:

        # Uncomment second one if you want house prices above the value entered
        if prices >= price_filter:
            houses_list.append({
                'Address': addresses,
                'Status': status_texts,
                '$Price': prices,
                'Beds': beds,
                'Baths': baths,
                'Square Feet': square_feet,
                'Acre Lot': acre_lot,
                'More Info Link': more_info_link
            })
    # Close the driver
    driver.quit()

    houses_dataframe = pd.DataFrame(houses_list)
    return houses_dataframe



if __name__ == '__main__':
    while True:
        df = find_houses()
        df.to_csv('houses.csv', index=False)
        # print(df)
        time_wait = 10
        print(f'Waiting {time_wait} minutes...')
        time.sleep(time_wait * 60)













  # if beds:
    #     print(f'{beds}')
    # if baths:
    #     print(f'{baths}')
    # if square_feet:
    #     print(f'{square_feet}')
    # if acre_lot:
    #     print(f'{acre_lot}')