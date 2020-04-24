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
f = open("pu.csv", 'w')
w = csv.writer(f)

w.writerow(["Faculty/School", "Department", "Course", "Title"])

# 第一次请求
headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
        'Referer': 'https://selfservice.mypurdue.purdue.edu/prod/bwckctlg.p_disp_dyn_ctlg?'
    }

search_url = 'https://selfservice.mypurdue.purdue.edu/prod/bwckctlg.p_disp_cat_term_date'
option_content = requests.post(search_url, 
                              headers=headers,
                              data={"call_proc_in": "bwckctlg.p_disp_dyn_ctlg",
"cat_term_in": "202020"}).content
soup = bs(option_content, "html.parser")
table = soup.find("table", class_="dataentrytable")

trs = table.find_all("tr")
tr = trs[0]

# 构建请求数据中的subj
options = [option.get("value") for option in tr.find_all("option")]

# 第二次请求
url = "https://selfservice.mypurdue.purdue.edu/prod/bwckctlg.p_display_courses"
for subj in options:
    
    from_data = {
        "term_in": "202020",
        "call_proc_in": "bwckctlg.p_disp_dyn_ctlg",
        "sel_subj": ["dummy", subj],
        "sel_levl": ["dummy", "%"],
        "sel_schd": ["dummy", "%"],
        "sel_coll": ["dummy", "%"],
        "sel_divs": ["dummy", "%"],
        "sel_dept": ["dummy", "%"],
        "sel_attr": ["dummy", "%"],
        "sel_crse_strt": '',
        "sel_crse_end": '',
        "sel_title": '',
        "sel_from_cred":'',
        "sel_to_cred": '',
    }
    content = requests.post(url=url, 
                            headers=headers, 
                            data=from_data).content

    soup = bs(content, "html.parser")
    data_table = soup.find("table", class_="datadisplaytable")
    tds1 = data_table.find_all("td", class_="nttitle")
    tds2 = data_table.find_all("td", class_="ntdefault")
    new = list(zip(tds1, tds2))
    for item in new:
        a, b = item
        data = a.text.split(" - ")
        course, title = data[0].strip(), data[1].strip()
        raw_data = b.text
        if re.search(r"Offered By", raw_data):
            faculty = raw_data.split("Offered By:")[1].split("\n")[0].strip()
        else:
            faculty = "N/A"
        if re.search(r"Department:", raw_data):
            department = raw_data.split("Department:")[1].split("\n")[0].strip()
        else:
            department = "N/A"
        print("Writing data: {}".format([faculty, department, course, title]))
        w.writerow([faculty, department, course, title])
        f.flush()
        