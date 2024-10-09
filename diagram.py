from datetime import datetime, timedelta
import requests
import pprint
import matplotlib.pyplot as plt

def get_date():
    cur_date = datetime.now()
    date_7 = cur_date - timedelta(days=6)
    cur_date = cur_date.strftime('%Y%m%d')
    date_7 = date_7.strftime('%Y%m%d')
    return cur_date, date_7

cur_date, date_7 = get_date()
url = f'https://bank.gov.ua/NBU_Exchange/exchange_site?start={date_7}&end={cur_date}&valcode=usd&sort=exchangedate&order=desc&json'

response = requests.get(url)
response_json = response.json()

# pprint.pprint(response_json)

rates = [item['rate'] for item in response_json]
dates = [item['exchangedate'] for item in response_json]

dates = [datetime.strptime(date, '%d.%m.%Y') for date in dates]
date_labels = [date.strftime('%Y-%m-%d') for date in dates]

plt.figure(figsize=(10, 5)) # построение самой диаграммы
bars = plt.bar(date_labels, rates, color='skyblue')

plt.ylim(min(rates) - 0.05, max(rates) + 0.05) # установка границ Оси У


for bar in bars: #подпись каждого столбца
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')

plt.title('UAH to USD')
plt.ylabel('Rate')
plt.xticks(rotation=45)

plt.tight_layout()
plt.grid(axis='y')  # Сетка только по оси Y

plt.show()
