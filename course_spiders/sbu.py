import requests
from bs4 import BeautifulSoup as bs
import re
import time
import csv
url_prefix = "https://www.stonybrook.edu/sb/bulletin/current/courses/"
"https://www.stonybrook.edu/sb/bulletin/current/courses/aas/"
url = 'https://www.stonybrook.edu/sb/bulletin/current/courses/browse/byabbreviation/'
f = open("sub.csv", 'w')
content = requests.get(url).content
soup = bs(content, "html.parser")
table = soup.find("table", attrs={"id": "bulletin_course_search_table"})
writer = csv.writer(f)
writer.writerow(["Major","Course", "Short description"])
trs = table.find_all("tr")
for tr in trs:
    data = tr.find_all("a")
    a, major = data
    suffix = a.text.strip().lower()
    major = re.sub("\(|\)", "", major.text.strip()) # \(\)
    course_info_link = url_prefix + suffix
    soup1 = bs(requests.get(course_info_link).content, "html.parser")
    for div in soup1.find_all("div", class_="course"):
        h3 = div.h3
        data = h3.text.strip().split(":")
        course, desc = data[0], data[1].strip()
        print("Writing: {}".format([major, course, desc]))
        writer.writerow([major, course, desc])
f.close()
        