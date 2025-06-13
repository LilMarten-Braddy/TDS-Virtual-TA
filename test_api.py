import requests

url = "http://127.0.0.1:5000/api/"
headers = {"Content-Type": "application/json"}
data = {"question": "Should I use gpt-4o-mini or gpt3.5 turbo?"}

response = requests.post(url, json=data, headers=headers)
print(response.status_code)
print(response.text)