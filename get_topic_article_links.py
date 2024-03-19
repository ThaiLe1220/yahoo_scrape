from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Set up Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uncomment to run in headless mode

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Read URLs from file
with open("valid_topic_links.txt", "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f.readlines()]

# Iterate over each URL
for url in urls:
    # Open the page
    driver.get(url)

    # Scroll down the page to ensure dynamic content loads. Adjust the range and sleep time as needed.
    for i in range(50):  # Number of page downs
        if i == 0:
            time.sleep(3)  # Initial wait for the page to load
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
        time.sleep(1)  # Wait for content to load after each page down

    # Get the page source
    page_source = driver.page_source

    # Use BeautifulSoup to parse the loaded page source
    soup = BeautifulSoup(page_source, "html.parser")

    # Initialize a set to store unique article links
    article_links = set()

    # Find all 'a' tags and filter by href attribute
    a_tags = soup.find_all("a")
    for a in a_tags:
        href = a.get("href")
        if href and href.startswith(
            "https://espanol.yahoo.com/"
        ):  # Adjust filter condition as needed
            article_links.add(href)

    # Save the article links to a text file
    filename = f"yahoo_links_{url.split('/')[-2]}.txt"
    with open(filename, "w", encoding="utf-8") as file:
        for article_link in article_links:
            file.write(f"{article_link}\n")

    print(f"Successfully saved {len(article_links)} links to {filename}")

# Close the browser after all URLs are processed
driver.quit()
