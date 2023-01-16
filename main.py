# Scraping Winnetka on realtor.com
from bs4 import BeautifulSoup
from selenium import webdriver


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
    
    beds = home.find('li', attrs={'class': 'jsx-946479843 prop-meta srp_list', 'data-label': 'pc-meta-beds'})
    if beds is not None:
        beds = beds.text
    else:
        beds = ''

    baths = home.find('li', attrs={'class': 'jsx-946479843 prop-meta srp_list', 'data-label': 'pc-meta-baths'})
    if baths is not None:
        baths = baths.text
    else:
        baths = ''

    # For the postings that don't include square_feet or acre_lot
    square_feet = home.find('li', attrs={'class': 'jsx-946479843 prop-meta srp_list', 'data-label': 'pc-meta-sqft'})
    if square_feet is not None:  
        square_feet = square_feet.text
    else:
        square_feet = ''

    acre_lot = home.find('li', attrs={'class': 'jsx-946479843 prop-meta srp_list', 'data-label': 'pc-meta-sqftlot'})
    if acre_lot is not None:
        acre_lot = acre_lot.text
    else:
        acre_lot = ''

    print(addresses, status_texts, prices, beds, baths, square_feet, acre_lot)

    print('')



# Close the driver
driver.quit()