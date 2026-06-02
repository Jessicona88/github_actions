import requests

url = "https://api.quotable.io/random?tags=inspirational"

response = requests.get(url, timeout=10)
response.raise_for_status()  # raises an error for bad status codes

data = response.json()
print(f"\"{data['content']}\" — {data['author']}")
