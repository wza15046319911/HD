
import requests
from bs4 import BeautifulSoup as bs
import re
import time
import csv


response = requests.get('https://www.latrobe.edu.au/handbook/2020/undergraduate/assc/arts/majors-minors.htm').content
soup = bs(response, 'html.parser')
lists = soup.find_all('tr')
divs = soup.find_all("h2", attrs={'class': 'accordion-title'})
with open("latrobe_courses.csv", 'w') as f:
    csv_writer = csv.writer(f)
    header = ["major", "cource_code", "description"]
    csv_writer.writerow(header)
    for div in divs:
        if not re.search(r"Major", div.text.strip()):
            for l in lists:
                tags = l.children
                for tag in tags:
                    if tag.name == 'td':
                        a = tag.a
                        if a:
                            course_code = a.text
                            desc = tag.text.split(" ")[1:]
                            csv_writer.writerow([div.text.strip(), course_code, " ".join(desc)])

