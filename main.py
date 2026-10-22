import requests
import matplotlib.pyplot as plt
from datetime import date, timedelta, datetime

end = date.today()
start = end - timedelta(days=30)

for cur in ["USD", "EUR"]:
    url = (f"https://bank.gov.ua/NBU_Exchange/exchange_site"
       f"?start={start:%Y%m%d}&end={end:%Y%m%d}"
       f"&valcode={cur.lower()}&sort=exchangedate&order=asc&json")
    data = requests.get(url).json()
    print(cur, "entries:", len(data))
    dates = [datetime.strptime(d["exchangedate"], "%d.%m.%Y") for d in data]
    rates = [d["rate"] for d in data]
    plt.plot(dates, rates, marker="o", label=cur)

plt.title("Bank Exchange Rates")
plt.xlabel("Date")
plt.ylabel("Exchange Rates, UAH")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
#print (dates[:3])
#print(rates[:3])