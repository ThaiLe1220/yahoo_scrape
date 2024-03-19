from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os

# Set up Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)

# URL of Yahoo News in Español
url = "https://es-us.noticias.yahoo.com/?guccounter=1"

# Open the page
driver.get(url)

# Scroll down the page to ensure dynamic content loads. Adjust the range and sleep time as needed.
for i in range(50):  # Number of page downs

    if i == 0:
        time.sleep(3)

    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
    time.sleep(3)  # Wait for the content to load

# Get the page source and close the browser
page_source = driver.page_source
driver.quit()

# Use BeautifulSoup to parse the loaded page source
soup = BeautifulSoup(page_source, "html.parser")


# Initialize a set to store unique article links
article_links = set()


# Find all 'a' tags and filter by href attribute
a_tags = soup.find_all("a")
for a in a_tags:
    href = a.get("href")
    if href and href.startswith("https://es-us."):  # Adjusted filter condition
        article_links.add(href)


# Save the article links to a text file
with open("en-us-yahoo-links.txt", "w", encoding="utf-8") as file:
    for article_link in article_links:
        file.write(f"{article_link}\n")

print(f"Successfully saved {len(article_links)} links to yahoo_news_links.txt")
