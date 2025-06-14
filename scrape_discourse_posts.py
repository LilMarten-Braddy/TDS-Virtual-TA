import requests
import json
from datetime import datetime
import os # Import the os module

def login_and_scrape_discourse_posts(): # No arguments needed for username/password
    session = requests.Session()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/114.0.0.0 Safari/537.36",
        "Content-Type": "application/json"
    }
    
    # Step 1: Retrieve CSRF token.
    csrf_url = "https://discourse.onlinedegree.iitm.ac.in/session/csrf"
    csrf_response = session.get(csrf_url, headers=headers)
    if csrf_response.status_code == 200:
        csrf_token = csrf_response.json().get("csrf", None)
        if not csrf_token:
            print("Failed to retrieve CSRF token from the response.")
            return
        print("CSRF token retrieved:", csrf_token)
    else:
        print("Failed to get CSRF token; status code:", csrf_response.status_code)
        return
    
    # Step 2: Login using the CSRF token.
    login_url = "https://discourse.onlinedegree.iitm.ac.in/session"
    
    # Get credentials from environment variables
    username = os.environ.get("DISCOURSE_USERNAME")
    password = os.environ.get("DISCOURSE_PASSWORD")

    if not username or not password:
        print("Error: DISCOURSE_USERNAME and DISCOURSE_PASSWORD environment variables must be set.")
        return

    payload = {
        "login": username,
        "password": password
    }
    login_headers = headers.copy()
    login_headers["X-CSRF-Token"] = csrf_token

    login_response = session.post(login_url, headers=login_headers, json=payload)
    if login_response.status_code not in (200, 201):
        print("Failed to login; status code:", login_response.status_code)
        print("Response:", login_response.text)
        return
        
    print("Login successful!")
    
    # Step 3: Access the protected latest topics.
    url = "https://discourse.onlinedegree.iitm.ac.in/latest.json"
    response = session.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        posts = []
        
        for topic in data.get("topic_list", {}).get("topics", []):
            created_at = topic.get("created_at")
            if created_at:
                post_date = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
                start_date = datetime(2025, 1, 1)
                end_date = datetime(2025, 4, 14)
                if start_date <= post_date <= end_date:
                    posts.append(topic)
        
        with open("discourse_posts.json", "w", encoding="utf-8") as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)
        print("Scraped discourse posts saved in discourse_posts.json!")
    else:
        print("Failed to retrieve discourse posts; status code:", response.status_code)

if __name__ == '__main__':
    login_and_scrape_discourse_posts()
