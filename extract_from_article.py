import requests
from bs4 import BeautifulSoup
import re


# Function to extract header and content from an article link
def extract_article_content(article_link):
    try:
        response = requests.get(article_link)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            header = soup.find("h1", {"data-test-locator": "headline"}).text.strip()
            content_div = soup.find("div", {"class": "caas-body"})
            paragraphs = content_div.find_all("p")
            content = "\n".join([p.text.strip() for p in paragraphs])
            return header, content
        else:
            print(f"Failed to retrieve article content for: {article_link}")
            return None, None
    except Exception as e:
        print(f"Error occurred while processing {article_link}: {str(e)}")
        return None, None


# Function to split content into sentences
def split_into_sentences(content):
    # Use regular expression to split the content into sentences based on '.', '?', and '!'
    sentences = re.split(r"(?<=[.!?]) +", content)
    return sentences


# Read the article links from the file
article_links = []
with open("es-us-yahoo-article.txt", "r", encoding="utf-8") as file:
    article_links = [line.strip() for line in file.readlines()]

# Create or clear the file
with open("es-us-yahoo-article-content.txt", "w", encoding="utf-8") as file:
    file.write("")

# Process each article link
for article_link in article_links:
    header, content = extract_article_content(article_link)
    if header and content:
        # Split content into sentences
        sentences = split_into_sentences(content)
        # Write header and sentences to the file
        with open("es-us-yahoo-article-content.txt", "a", encoding="utf-8") as file:
            file.write(f"{header}\n")
            file.write("\n".join(sentences))
            file.write("\n\n")

print("Article headers and sentences saved to yahoo_article_sentences.txt.")
