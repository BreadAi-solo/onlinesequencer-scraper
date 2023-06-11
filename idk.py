# Import requests, BeautifulSoup, tqdm, and itertools libraries
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from itertools import count
import time
import random
# Define the base url and the initial start parameter
base_url = "https://onlinesequencer.net/sequences?date=4&sort=2&start="
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
        # Construct the midi url with the numbers
        midi_url = f"https://onlinesequencer.net/app/midi.php?id={numbers}"
        # Try to get the midi file from the url
        midi_response = requests.get(midi_url)
        # Check if the status code is 200 (OK)
        if midi_response.status_code == 200:
            # Try to save the midi file to a local file with the same name as the url
            try:
                with open(midi_url.split("=")[-1]+str(random.randrange(1,1000000000000))+".mid", "wb") as f:
                    f.write(midi_response.content)
                # Print a message that the file was saved
                print(f"Saved {midi_url}")
                
            except PermissionError:
                # Print a message that the file could not be saved and skip it
                print(f"Could not save {midi_url}")
                
        else:
            # Print a message that there was no file
            print(f"No file at {midi_url}")
            
    # Increment the start parameter by 90 to go to the next page
    start += 90

