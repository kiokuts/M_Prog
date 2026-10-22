from datetime import date, timedelta

import requests

URL = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"

def get_rate(day: date, valcode: str = "EUR"):
    params = {
        "valcode": valcode,
        "date": day.strftime("%Y%m%d"),
        "json": "",
    }
    resp = requests.get(URL, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return data[0] if data else None

today = date.today()
this_monday = today - timedelta(days=today.weekday())
last_monday = this_monday - timedelta(days=7)

for i in range(7):
    day = last_monday + timedelta(days=i)
    rate = get_rate(day, "EUR")
    if not rate:
        print(f"{day.strftime('%d.%m.%Y')}: no data available")
    else:
        print(f"{rate['exchangedate']}: {rate['rate']} UAH")
