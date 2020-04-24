import requests
from bs4 import BeautifulSoup as bs
import re
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import csv
pattern = r"[a-zA-Z]{4,}\d{3,}"
def test():
    # start from Page 1
    start = 1
    limit = 10
    end = 371
    page = 1
    courses = []
    with open("aut.csv", 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["Program", "Major", "Course", "Course title"])
        for i in range(start, end, limit):
            url = "https://www.aut.ac.nz/s/search.html?query=&collection=aut-ac-nz-meta-dev&form=simple&sitetheme=orange&f.Tabs%7CT=Course&tab=Course&start_rank={}".format(i)
            response = requests.get(url).content
            print("Now in page: {}".format(page))
            soup = bs(response, "html.parser")
            lists = soup.find_all("li", class_="clearfix courseItem")
            for j in lists:
                div = j.find("div", class_="colInner")
                a1 = div.find("a")
                if a1:
                    link = a1.get("title")
                    program = a1.text
                    response1 = requests.get(link).content
                    # print("Go to {}".format(link))
                    soup1 = bs(response1, "html.parser")
                    for a2 in soup1.find_all("a"):
                        if a2.get("href") and a2.text:
                            if a2.get("href").startswith("#tab"):
                                if a2.text == "Majors":
                                    for div in soup1.find_all("div"):
                                        if div.get("id") == a2.get("href")[1:]:
                                            for a3 in div.find_all("a"):
                                                response2 = requests.get(a3.get("href"))
                                                soup2 = bs(response2.content, "html.parser")
                                                for b in soup1.find_all("a", class_="paperbox"):
                                                    csv_writer.writerow([program, a3.text, b.text.split(" ")[0].strip(), " ".join(b.text.split(" ")[1:])])
                                elif a2.text == "What you study":
                                    for a4 in soup1.find_all("a", class_="paperbox"):
                                        csv_writer.writerow([program, program, a4.text.split(" ")[0].strip(), " ".join(a4.text.split(" ")[1:])])
                                elif a2.text == "Minors":
                                    print("[      {}      ]".format(link))
            page += 1                           
test()
