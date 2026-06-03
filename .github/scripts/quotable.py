import requests

url = "https://quotes.rest/qod?language=en"
response = requests.get(url, timeout=10)
response.raise_for_status()

data = response.json()[0]
print (data)
#quote = f"\"{data['content']}\" — {data['author']}"
#print(quote)
