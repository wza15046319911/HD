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
regex = "#/cu/bulletin/uwb/"

urls = ["https://doc.search.columbia.edu/classes/+?site=Directory_of_Classes&instr=&days=&semes=20201", 
        "https://doc.search.columbia.edu/classes/+?site=Directory_of_Classes&instr=&days=&semes=20202"]
option = webdriver.ChromeOptions()
option.add_argument('headless')
try:
    f = open("cu.csv", 'w')
    driver = webdriver.Chrome(options=option)
    for url in urls:
        driver.get(url)
        driver.implicitly_wait(3)
        writer = csv.writer(f)
        writer.writerow(["Major", "Course", "Short description"])
        for li in driver.find_elements_by_css_selector(".row.ng-scope"):
            major, course, desc = "", "", ""
            h4 = li.find_element_by_tag_name("h4")
            course_title = h4.get_attribute("textContent").strip()
            course_link = li.find_element_by_class_name("url").find_element_by_tag_name("a").get_attribute("href")
            course_link = course_link.replace(regex, "")

            content = requests.get(course_link).content
            soup = bs(content, "html.parser")
            trs = soup.find_all("tr")
            fonts = trs[1].find_all("font")
            desc = fonts[1].text.strip()
            for tr in trs[2:-1]:
                tds = tr.find_all("td")
                a, b = tds
                if re.search(r"Subject", a.text):    
                    major = b.text.split(",")[0].strip()
                elif re.search(r"Number", a.text):
                    course = b.text.strip()
            print("Writing: {}".format([major, course, desc]))
            writer.writerow([major, course, desc])
    driver.quit()
except Exception as e:
    driver.quit()

