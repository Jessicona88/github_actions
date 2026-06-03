import requests

url = "https://zenquotes.io/api/random"
response = requests.get(url, timeout=10)
response.raise_for_status()

data = response.json()[0]
quote = print(f"\"{data['q']}\" — {data['a']}")
