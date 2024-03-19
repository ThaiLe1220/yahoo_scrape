import requests
from bs4 import BeautifulSoup
import re


# Function to extract header and content from an article link
def extract_article_content(article_link):
    header = None
    content = None
    try:
        response = requests.get(article_link)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            header_tag = soup.find("h1", {"data-test-locator": "headline"})
            # Check if the header tag was found
            if header_tag:
                header = header_tag.text.strip()

            content_div = soup.find("div", {"class": "caas-body"})
            if content_div:
                # Remove Twitter links
                for a_tag in content_div.find_all("a", href=True):
                    if "twitter.com" in a_tag["href"]:
                        a_tag.decompose()
                # Remove Twitter links and paragraphs containing Twitter links
                for p in content_div.find_all("p"):
                    if "twitter.com" in p.text:
                        p.decompose()
                paragraphs = content_div.find_all("p")
                # Join the text from paragraphs to form the content
                content = "\n".join(p.text.strip() for p in paragraphs if p.text)

            if not header or not content:
                return (
                    "Missing Content",
                    "The article does not have a header or content.",
                )
            return header, content
        else:
            print(f"Failed to retrieve article content for: {article_link}")
            return (
                "HTTP Error",
                f"Failed to retrieve article content with status code: {response.status_code}",
            )
    except Exception as e:
        print(f"Error occurred while processing {article_link}: {str(e)}")
        return "Error", f"An error occurred while processing the article: {str(e)}"


def contains_emoji(sentence):
    # Regex pattern to match most emojis
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F700-\U0001F77F"  # alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        "\U0001FA00-\U0001FA6F"  # Chess Symbols
        "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "\U00002702-\U000027B0"  # Dingbats
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE,
    )
    return re.search(emoji_pattern, sentence)


# Function to split content into sentences
def split_into_sentences(content):
    # Split content into sentences
    sentences = re.split(r"(?<=[.!?])\s+", content)
    # Remove sentences with emojis
    sentences_without_emojis = [s for s in sentences if not contains_emoji(s)]
    return sentences_without_emojis


# Read the article links from the file, skipping "Current Topic" lines
article_links = []
with open("es-us-yahoo-articles-links-by-topics.txt", "r", encoding="utf-8") as file:
    for line in file:
        if line.startswith("https://"):  # Ensure the line is an article link
            article_links.append(line.strip())

# Create or clear the output file
with open(
    "es-us-yahoo-article-links-by-topics-content.txt", "w", encoding="utf-8"
) as file:
    file.write("")

# Process each article link
for article_link in article_links:
    header, content = extract_article_content(article_link)
    if header and content:
        sentences = split_into_sentences(content)
        with open(
            "es-us-yahoo-article-links-by-topics-content.txt", "a", encoding="utf-8"
        ) as file:
            file.write(f"{header}\n")
            file.write("\n".join(sentences))
            file.write("\n\n")

print("Article headers and sentences saved to es-us-yahoo-article-content.txt.")
