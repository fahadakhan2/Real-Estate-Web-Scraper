from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
import time
import re




# Regular expression to check if the input matches the pattern
location_pattern  = re.compile(r'^[A-Za-z-]+_[A-Za-z]{2}$')
# Filtration System
while True:
    print('Enter the location you want to search (e.g. Winnetka_IL, San-Diego_CA):')
    location = input('')
    if re.match(location_pattern, location):
        print('Enter the price you want to buy a house (e.g. 1000000 for a one million dollar house:')
        price_filter = int(input(''))
        print(f'Retrieving houses over {price_filter}')
        break
    else:
        print('Invalid Location. Please Provide a Correct Location Name:')



def find_houses(pages=1):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get('https://www.realtor.com/realestateandhomes-search/{}'.format(location))
    html_text = driver.page_source # Get the HTML source code
    
    # Function for extracting text for the variables beds, baths, square_foot, and acre_lot
    def extract_text(home, attr):
        element = home.find('li', attrs={'class': 'jsx-946479843 prop-meta srp_list', 'data-label': attr})
        if element is not None:
            return element.text
        else:
            return ''
    
    houses_list = [] # For dataframe
    for page in range(pages):
        soup = BeautifulSoup(html_text, 'lxml')
        homes = soup.find_all('li', class_ = 'jsx-1881802087 component_property-card') # For all home listings on first page
        for home in homes: 
            addresses = home.find('div', class_ = 'jsx-11645185 address ellipsis srp-page-address srp-address-redesign').text
            status_texts = home.find('span', class_ = 'jsx-3853574337 statusText').text
            prices = home.find('span', attrs={'class': 'Price__Component-rui__x3geed-0 gipzbd', 'data-label': 'pc-price'}).text
            prices = int(prices.replace('$', '').replace(',', ''))
            beds = extract_text(home, 'pc-meta-beds')
            baths = extract_text(home, 'pc-meta-baths')
            square_feet = extract_text(home, 'pc-meta-sqft')
            acre_lot = extract_text(home, 'pc-meta-sqftlot')
            more_info_link = home.div.a['href']

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
        try:  # Checks to see if there is a next button and if there is clicks it and scrapes the number of pages given in the main function
            time.sleep(5)
            next_button = driver.find_element_by_xpath('//*[@id="srp-body"]/section[1]/div/div[1]/div/a[8]')
            next_button.click()
        except:
            driver.quit()
            break
                                             

    # Creating and adding list to dataframe
    houses_dataframe = pd.DataFrame(houses_list)
    if houses_dataframe.shape[0] == 0:
        print("No houses found for the given location for the filtered price.")
    else:
        return houses_dataframe 


if __name__ == '__main__':
    should_continue = True
    while should_continue:
        df = find_houses(pages=3) # Enter how many pages to scrape
        print("View results.csv and barchart for results(Close barchart when ready for next scrape.") # Need to close the graph to stop the execution of program
        if df is not None:
            with open("results.csv", "w") as f: # Write tabulate to results.csv
                f.write(tabulate(df, headers='keys', tablefmt='psql'))

            df.plot(kind='bar', x='Address', y='$Price', color='green', legend=False) 
            plt.xlabel('Address', fontsize=12)
            plt.ylabel('$Price', fontsize=12)
            plt.title('House Prices', fontsize=14)
            plt.show()
            
            time_wait = 10  # cooldown before next scrape
            print(f'COOLDOWN: Waiting {time_wait} minutes...')
            time.sleep(time_wait * 60) 
        else:
            should_continue = False