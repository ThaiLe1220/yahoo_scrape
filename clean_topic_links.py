# Function to check if a URL is valid
def is_valid_url(url):
    return url.startswith("https://espanol.yahoo.com/topics/") and not url.startswith(
        "https://espanol.yahoo.comhttps://"
    )


# List to hold valid URLs
valid_urls = []

# Open the file and filter URLs
with open("topic-yahoo-links.txt", "r") as file:
    for line in file:
        url = line.strip()  # Remove any leading/trailing whitespace characters
        if is_valid_url(url):
            valid_urls.append(url)

# Save valid URLs to a new file
with open("valid_topic_links.txt", "w") as output_file:
    for url in valid_urls:
        output_file.write(url + "\n")

print(f"Filtered and saved {len(valid_urls)} valid URLs to valid_topic_links.txt.")
