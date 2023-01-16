# Scraping Winnetka on realtor.com
from bs4 import BeautifulSoup
from selenium import webdriver

# Function for extracting text for the variables beds, baths, square_foot, and acre_lot
# that some listings don't include these specific variables
def extract_text(home, attr):
    element = home.find('li', attrs={'class': 'jsx-946479843 prop-meta srp_list', 'data-label': attr})
    if element is not None:
        return element.text
    else:
        return ''


# Start a web driver
driver = webdriver.Chrome()
driver.get('https://www.realtor.com/realestateandhomes-search/Winnetka_IL')
html_text = driver.page_source # Get the HTML source code

soup = BeautifulSoup(html_text, 'lxml')
homes = soup.find_all('li', class_ = 'jsx-1881802087 component_property-card') # For all home listings on first page
for home in homes: 
    addresses = home.find('div', class_ = 'jsx-11645185 address ellipsis srp-page-address srp-address-redesign').text
    status_texts = home.find('span', class_ = 'jsx-3853574337 statusText').text
    prices = home.find('span', attrs={'class': 'Price__Component-rui__x3geed-0 gipzbd', 'data-label': 'pc-price'}).text
    beds = extract_text(home, 'pc-meta-beds')
    baths = extract_text(home, 'pc-meta-baths')
    square_feet = extract_text(home, 'pc-meta-sqft')
    acre_lot = extract_text(home, 'pc-meta-sqftlot')

    print(f'{addresses}')  #  work on the spacing for the houses that dont list any of the 4 specific variables
    print(f'Status: {status_texts}')
    print(f'Price: {prices}')
    if beds or baths:
        print(f'{beds} {baths}', end=' ')
        print()
    if square_feet or acre_lot:
        print(f'{square_feet} {acre_lot}')
    # if beds:   //For having each variable on its own line for storing later in dataframe or base.
    #     print(f'{beds}')
    # if baths:
    #     print(f'{baths}')
    # if square_feet:
    #     print(f'{square_feet}')
    # if acre_lot:
    #     print(f'{acre_lot}')
    print('')









# Close the driver
driver.quit()