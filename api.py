import requests as req
from datetime import datetime

ROOT_URL = 'https://api.eia.gov/series/'
API_KEY = '646e6d8dad13215f3612a7df88eaa13a'
ENDPOINT = '{}?api_key={}&series_id=NG.RNGWHHD.'.format(ROOT_URL, API_KEY)

def export_to_csv(rows, filename):
  with open('data/{}.csv'.format(filename), 'wb') as file:
    file.write('\n'.join(rows).encode('utf-8'))

def fetch(url, parse_year, parse_month, parse_day, filename):
  res = req.get(url).json()

  rows = ['date,price']
  pairs = res['series'][0]['data']

  for pair in pairs:
    [date, price] = pair
    year = parse_year(date)
    month = parse_month(date)
    day = parse_day(date)

    if price:
      rows.append('{}/{}/{},{}'.format(year, month, day, price))

  export_to_csv(rows, filename)

def daily():
  fetch(
    url = ENDPOINT + 'D',
    parse_year = lambda date: date[0:4],
    parse_month = lambda date: date[4:6],
    parse_day = lambda date: date[6:8],
    filename ='daily'
  )

def weekly():
  fetch(
    url = ENDPOINT + 'W',
    parse_year = lambda date: date[0:4],
    parse_month = lambda date: date[4:6],
    parse_day = lambda date: date[6:8],
    filename ='weekly'
  )

def monthly():
  fetch(
    url = ENDPOINT + 'M',
    parse_year = lambda date: date[0:4],
    parse_month = lambda date: date[4:6],
    parse_day = lambda date: '01',
    filename ='monthly'
  )

def annual():
   fetch(
    url = ENDPOINT + 'A',
    parse_year = lambda date: date[0:4],
    parse_month = lambda date: '01',
    parse_day = lambda date: '01',
    filename ='annual'
  )
