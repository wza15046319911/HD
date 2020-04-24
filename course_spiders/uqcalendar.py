import requests
from bs4 import BeautifulSoup as bs
import re
import time
import csv

headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    "Cookie": "_ga=GA1.3.1749078902.1567578553; _gcl_au=1.1.1949422585.1583415042; UQSECURE=1; zarget_user_id=1583824187839r0.36377726550673906; zarget_visitor_info=%7B%22BTUXQUQ%22%3A1549349%7D; __utmc=176970273; _hjid=7dbc872d-8930-47de-ba73-49577d521fad; __utma=176970273.1749078902.1567578553.1585021887.1586949689.2; __utmz=176970273.1586949689.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); uqlb=!s4homYoPDBao8BU+XJOGvcgnwHV0Viki2MDQiu+jJbCnlR8rSVSOK1wwlqp1B7zTUtoSsfM0it0Djho="
}

f = open("UQ2020日历.csv", 'w')
w = csv.writer(f)
w.writerow(["Date", "Event"])

DAYS = {
    "Mon": 'Monday',
    "Tue": "Tuesday",
    "Wed": "Wednesday",
    "Thu": "Thursday", 
    "Fri": "Friday",
    "Sat": "Saturday", 
    "Sun": "Sunday"
}

def process_date(date):
    d = date.split(" ")
    day = d[0]
    a, b, c = d[1].split("-")
    return "{}, {}".format("/".join([c, b, a]), DAYS.get(day))

url = "https://www.uq.edu.au/events/calendar_view.php?category_id=16&year=2020&month=&day=01"
content = requests.get(url=url, headers=headers).content
soup = bs(content, "html.parser")

ul = soup.find("ul", attrs={"class":"events-lists"})

first = ul.find_all("li", attrs={"class": "first"})
calendar_view = ul.find_all("li", attrs={"class": "description-calendar-view"})
for item in zip(first, calendar_view):
    a, event = item
    data = a.text.split("\n")
    date = process_date(data[0])
    w.writerow([date, event.text])
    f.flush()