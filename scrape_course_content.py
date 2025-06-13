import requests
from bs4 import BeautifulSoup
import json

def scrape_course_content():
    url = "https://tds.s-anand.net/#/2025-01/"
    response = requests.get(url)
    if response.status_code == 200:
        # Note: if content is rendered via JavaScript you might need Selenium or similar.
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Ideally, inspect the page structure and extract relevant pieces.
        # This example just pulls all text:
        content = soup.get_text(separator="\n").strip()
        
        # Save the scraped content to a JSON file for later use (in your answer logic).
        with open("course_content.json", "w", encoding="utf-8") as f:
            json.dump({"content": content}, f, ensure_ascii=False, indent=2)
        print("Scraped course content saved in course_content.json!")
    else:
        print("Failed to retrieve course content; status code:", response.status_code)

if __name__ == '__main__':
    scrape_course_content()