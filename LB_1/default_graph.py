from datetime import datetime, timedelta
import requests
import pprint
import matplotlib.pyplot as plt
from sympy.codegen.ast import break_


def get_date(): # функция для получения текущей даты и даты которая была неделю назад

    cur_date = datetime.now()

    date_7 = cur_date - timedelta(days=6)

    cur_date = cur_date.strftime('%Y%m%d')
    date_7 = date_7.strftime('%Y%m%d')
    return cur_date, date_7

# print(response.status_code)

cur_date, date_7 = get_date()
url = f'https://bank.gov.ua/NBU_Exchange/exchange_site?start={date_7}&end={cur_date}&valcode=usd&sort=exchangedate&order=desc&json'

response = requests.get(url)
response_json = response.json()

pprint.pprint(response_json)

# print(response_json[0]['rate'])

rates = [item['rate'] for item in response_json]
dates = [item['exchangedate'] for item in response_json]

plt.figure(figsize=(10, 5))
plt.plot(dates, rates,)
plt.grid()
plt.suptitle('UAH to USD')
plt.show()
