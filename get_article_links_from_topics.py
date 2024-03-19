from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


def scroll_to_end(driver):
    """
    Scrolls down the page until no more new content is loaded.

    :param driver: Selenium WebDriver instance
    """
    # Get initial scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(1)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # If heights are the same, it is the end of the page
        last_height = new_height


def scrape_articles(driver, url):
    """
    Scrape article links from a given URL, filter them to include only those ending with .html but not with index.html,
    prepend a specific domain, and save them to a file.

    :param driver: Selenium WebDriver instance
    :param url: URL to scrape
    """
    current_topic = url.split("/")[-2]
    print(f"Current Topic: {current_topic}")

    # Open the page
    driver.get(url)

    time.sleep(3)

    # Scroll down the page until the end
    scroll_to_end(driver)

    # Use BeautifulSoup to parse the loaded page source
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Initialize a set to store unique article links
    article_links = set()

    # Find all 'a' tags, filter by href attribute, and process
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.endswith(".html") and not href.endswith("index.html"):
            full_url = (
                f"https://es-us.noticias.yahoo.com{href}"
                if not href.startswith("http")
                else href
            )
            article_links.add(full_url)

    # Print the total number of links scraped for the current topic
    print(f"Total links scraped for {current_topic}: {len(article_links)}")

    # Save the article links to a text file
    filename = "source/es-us-yahoo-articles-links-by-topics.txt"
    with open(filename, "a", encoding="utf-8") as file:
        # Write the header with the current topic
        file.write(f"\nCurrent Topic: {url}\n\n")
        # Write each article link
        for article_link in article_links:
            file.write(f"{article_link}\n")

    print(f"Successfully saved {len(article_links)} links to {filename}")


def main():
    # Set up Chrome options
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Uncomment to run in headless mode

    # Initialize the WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    # Read URLs from file
    with open("source/en-us-yahoo-topics.txt", "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f.readlines()]

    # Iterate over each URL and process them
    try:
        for url in urls[119:]:
            scrape_articles(driver, url)
    finally:
        # Close the browser after all URLs are processed
        driver.quit()


if __name__ == "__main__":
    main()
