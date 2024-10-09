import json
import matplotlib.pyplot as plt
import requests

url = f'https://bank.gov.ua/NBU_Exchange/exchange_site?start=20240930&end=20241005&valcode=usd&json'

response = requests.get(url)
response_json = response.json()
response_dict = json.loads(response.content)
# print(response_json)
# print('-----')
# print(response_dict)

exchange_dict = {}

for item in response_dict:
    # print('>', item['exchangedate'], '-', item['rate'])
    exchange_dict[item['exchangedate']]=item['rate']

# print(exchange_dict)

