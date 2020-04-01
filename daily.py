#!/usr/bin/python3

from bs4 import BeautifulSoup
import requests as req
from datetime import datetime

def parse():
  to_csv("https://www.eia.gov/dnav/ng/hist/rngwhhdD.htm", 'Daily')

def parse_week(s):
  parts = s.split(" ")
  year = int(parts.pop(0))
  start_year = year
  end_year = year

  date_range = " ".join(parts)

  [start, end] = date_range.split(" to ")
  [start_month, start_day] = start.split("-")
  [end_month, end_day] = end.split("-")

  if start_month == 'Dec' and end_month == 'Jan':
    end_year += 1

  return {
    "start": {
      "year": start_year,
      "month": start_month,
      "day": int(start_day)
    },
    "end": {
      "year": end_year,
      "month": end_month,
      "day": int(end_day)
    }
  }

def format_week(week):
  days = []

  if week['start']['month'] != week['end']['month']:
    week_end = []
    offset_end = 0
    while week['end']['day'] - offset_end != 0:
      week_end.insert(0, "{} {} {}".format(week['end']['day'] - offset_end, week['end']['month'], week['end']['year']))
      offset_end += 1

    week_start = []
    offset_start = 0
    while (len(week_start) + len(week_end)) < 5:
      week_start.append("{} {} {}".format(week['start']['day'] + offset_start, week['start']['month'], week['start']['year']))
      offset_start += 1

    days = [*week_start, *week_end]

  else:
    offset = 0
    while (week['start']['day'] + offset) <= week['end']['day']:
      days.append("{} {} {}".format(week['start']['day'] + offset, week['start']['month'], week['start']['year']))
      offset += 1

  return days


def to_csv(url, filename):
  resp = req.get(url)
  soup = BeautifulSoup(resp.text, 'lxml')

  csv = []
  table = soup.find_all('table')
  rows = table[5].find_all('tr')

  head = 'Date,Price'
  csv.append(head)

  for row in rows[1:]:
    cols = row.find_all('td')
    cols = [content.text.strip() for content in cols]
    [date_range, *prices] = cols

    if not date_range: continue

    week = parse_week(date_range)
    days = format_week(week)

    for i in range(5):
      price = prices[i]
      if price:
        csv.append("{},{}".format(days[i], prices[i]))

  time = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
  with open("{} {}.csv".format(filename, time), "wb") as file:
    file.write("\n".join(csv).encode('utf-8'))
