import requests
import pprint # для обработки JSON-a

response = requests.get('https://bank.gov.ua/NBU_Exchange/exchange_site?start=20240930&end=20241005&valcode=usd&json')

print(response.status_code) # проверрка успешности запроса
response_json = response.json() # конвертация вывода в JSON формат
pprint.pprint(response_json) # функция для читаемого вывода JSON