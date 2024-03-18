# Read the content of en-us-yahoo-links.txt and filter the links
article_links = []
with open("en-us-yahoo-links.txt", "r", encoding="utf-8") as file:
    for line in file:
        link = line.strip()  # Remove leading/trailing whitespace
        if link.startswith("https://es-us.noticias.yahoo.com/") and link.endswith(
            ".html"
        ):
            article_links.append(link)

# Save the filtered article links to yahoo-article.txt
with open("en-us-yahoo-article.txt", "w", encoding="utf-8") as file:
    for article_link in article_links:
        file.write(f"{article_link}\n")

print(f"Successfully saved {len(article_links)} article links to yahoo-article.txt.")
