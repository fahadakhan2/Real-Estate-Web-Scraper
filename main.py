from bs4 import BeautifulSoup
from selenium import webdriver

# Start a web driver
driver = webdriver.Chrome()
driver.get('https://www.realtor.com/realestateandhomes-search/Winnetka_IL')
html_text = driver.page_source # Get the HTML source code

soup = BeautifulSoup(html_text, 'lxml')




# Close the driver
driver.quit()