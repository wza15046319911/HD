import requests
from bs4 import BeautifulSoup as bs
import re
import time
import csv

start_url = "https://www.imperial.ac.uk"
response = requests.get(start_url + "/study/pg/courses/").content
soup = bs(response, "html.parser")
for li in soup.find_all("li", class_="course"):
    a = li.find("a")
    program = a.get("title")
    response1 = requests.get(start_url + a.get("href")).content
    soup1 = bs(response1, "html.parser")
    for item_div in soup1.find_all("div", class_="item"):
        
