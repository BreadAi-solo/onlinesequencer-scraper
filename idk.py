# Import requests, BeautifulSoup, tqdm, itertools, time, random, and selenium libraries
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from itertools import count
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import os


download_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'midi')



# Set up the Chrome options
chrome_options = Options()
chrome_options.add_argument('--blink-settings=imagesEnabled=false')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--disable-plugins-discovery')
chrome_options.add_argument('--disable-plugins')
chrome_options.add_argument('--headless') # Run Chrome in headless mode

chrome_options.add_experimental_option('prefs', {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})
# Set up the web driver (replace with the path to your web driver)
driver = webdriver.Edge(options=chrome_options)

# Define the base url and the initial start parameter
base_url = "https://onlinesequencer.net/sequences?search=&sort=2&date=4&search="
start = 1

# Loop until there is no next page with a progress bar
for _ in tqdm(count(), desc="Scraping pages", unit="page"):
    # Construct the full url for each page
    url = base_url + str(start)
    # Get the html content of the page
    response = requests.get(url)
    # Parse the html with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    # Find all the div elements with class "preview"
    previews = soup.find_all("div", class_="preview")
    # Loop through the previews
    for preview in previews:
        # Find the a element inside the preview
        link = preview.find("a")
        # Get the href attribute of the link
        href = link["href"]
        # Get the numbers from the href
        numbers = href[1:]
        # Construct the sequence url with the numbers
        sequence_url = f"https://onlinesequencer.net/{numbers}"
        # Open the sequence page with Selenium
        driver.get(sequence_url)
        # Execute the exportMidi function in the console
        driver.execute_script('return exportMidi();')
        # Wait for a short time to allow the file to download (you may need to adjust this value)
        time.sleep(0.2)
            
    # Increment the start parameter by 90 to go to the next page
    start += 90

# Close the web driver when finished
driver.close()
