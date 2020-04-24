import requests
from bs4 import BeautifulSoup as bs
import re
import time
import csv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
f = open("gw.csv", 'w')
w = csv.writer(f)

w.writerow(["Faculty/School", "Course", "Title"])
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
}

start_url = "https://my.gwu.edu/mod/pws/coursesearch.cfm"
content = requests.get(url=start_url, headers=headers).content
soup = bs(content, "html.parser")
select_box = soup.find("select", attrs={"name": "dept", "class": "bodyFont", "id": "field_dept"})
subjects = [option.get("value") for option in select_box.find_all("option")]
faculties = [option.text.strip() for option in select_box.find_all("option")]
course_search_url = 'https://my.gwu.edu/mod/pws/searchresults.cfm'

faculty_data = list(zip(subjects, faculties))

for i in faculty_data[1:]:
    subject, faculty = i
    from_data = {
        "term": "202003",
        "campus": "1",
        "srchType": "All",
        "dept": subject,
        "courseNumSt": '',
        "courseNumEn": '',
        "courseAttrSt": '',
        "crn": '',
        "courseTitle":'' ,
        "courseInst":'' ,
        "beginTime":'' ,
        "endTime": '',
        "courseDays": ["M","T","W","R","F", "S", "U"],
        "addReq":"", 
        "pageNum": "1",
        "courseAttrSt":"" 
    }
    new_requests = requests.post(url=course_search_url,
                                 headers=headers,
                                 data=from_data).content
    
    soup = bs(new_requests, "html.parser")
    basic_tables = soup.find_all("table", attrs={"class":"basicTable"})
    max_pages = 0
    course = ""
    title = ""
    if len(basic_tables) > 0:
        basic_table = basic_tables[0]
        page_tr = basic_table.find("tr")
        page_td = page_tr.find("td", attrs={"class": "alignCenter"})
        page_as = page_td.find_all("a")
        if len(page_as) > 0:
            max_pages = int(page_as[-1].text.strip())
            for i in range(1, max_pages + 1):
                from_data["pageNum"] = str(i)
                r2 = requests.post(url=course_search_url,
                                   headers=headers,
                                   data=from_data).content
                soup1 = bs(r2, "html.parser")
                course_header = soup1.find("table", class_="bodyFont basicTable courseListingHeader courseListingSetWidths")
                course_headers = [td.text for td in course_header.find_all("td")]
                for table in soup1.find_all("table", class_="courseListing basicTable courseListingSetWidths"):
                    trs = table.find_all("tr")
                    if len(trs) > 0:
                        tr = trs[0]
                        tds = []
                        for td in tr.find_all("td"):
                            if len(td.find_all("span")) > 0:
                                spans = td.find_all("span")
                                temp = ""
                                for span in spans:
                                    temp += span.text.strip()
                                tds.append(temp)
                            else:
                                tds.append(td.text) 
                        new = list(zip(course_headers, tds))
                        for item in new:
                            a, b  = item
                            if a == "SUBJECT":
                                course = b.strip().replace(" ", "")
                            elif a == "COURSE":
                                title = b.strip()
                        
                        print("Writing row: {}".format([faculty, course, title]))
                        w.writerow([faculty, course, title])
                        f.flush()
    else:
        print("No results are returned.")
    