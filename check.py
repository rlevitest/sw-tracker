import requests
from bs4 import BeautifulSoup

url = "https://www.swroasting.coffee/"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Scrape all text on the homepage and look for the drop text
page_text = soup.get_text()
target_phrase = "Current drop is roast date"

if target_phrase in page_text:
    print("Success: The drop phrase is present on the page.")
else:
    # This will cause the workflow to fail and notify you
    raise Exception("ALERT: The target roast text changed or disappeared!")
