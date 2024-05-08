import requests



h = {'Accept': 'application/json'}

response = requests.get("https://scholar.google.com/scholar?cites=691679248024618230&as_sdt=2005&sciodt=0,5&hl=en", headers=h)

data = response.json()

