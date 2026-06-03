import requests

#url = "https://zenquotes.io/api/random"
url = "https://api.quotable.io/random?"
response = requests.get(url, timeout=10)
response.raise_for_status()

data = response.json()[0]
#quote = f"\"{data['q']}\" — {data['a']}"
#quote = f"\"{data['content']}\" — {data['author']}"
print(quote)
