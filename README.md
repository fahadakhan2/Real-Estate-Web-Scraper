Real-Estate-Web-Scraper

A web scraping tool that allows users to gather real estate data from Realtor.com for any location and price of their choice. The information is scraped from multiple pages, with the number of pages specified by the user.

The tool features a filtration system that filters the location and price of the properties, catching any errors and prompting the user for another input if the input is not in the correct format.

The information retrieved includes addresses, status texts (for availability), prices, number of beds, baths, square feet, acre lot, and a more info link that can take you straight to the specific listing on Realtor.com where you can view all extra information. This information is then stored in a pandas dataframe for further analysis.

The program provides data analysis through the scraped data in tabulated format in a CSV file called "results". Additionally, a bar chart is generated that compares the addresses to their respective prices in the location specified by the user. Extra Information about the house listings including the mean price and square feet of the real estate scrape is outputted into the terminal.

To prevent overloading the website with requests and to avoid getting blocked, the tool includes a cooldown period before the next scrape.

This tool is useful for real estate professionals, data analysts, or anyone interested in gathering real estate data for a specific location and price range.
