from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup as bs
import re
import time
import csv
special_url = "http://services.bc.edu/PublicCourseInfoSched/courseinfoschedResults"

prefixes = [
    "AADS", "ARTH", "BIOL", "UNCP", 
    "CHEM", "CLAS", "COMM", "CSCI", 
    "UNCS", "EESC", "EALC", "ECON", 
    "ENGL", "ENVS", "FILM", "RREN", "GREM", 
    "HIST", "HONR", "INTL", "ICSP", "ITAL", 
    "JESU", "JOUR", "LING", "MATH", 'ROTC', 
    'MUSA', 'MUSP', 'NELC', 'PHIL', 'PHYS', 
    'POLI', 'PSYC', 'RLRL', 'SLAV', 'SOCY',
    'SPAN', 'ARTS', 'THTR', 'THEO', 'UNAS'
    ]
start = "https://services.bc.edu/PublicCourseInfoSched/"
urls = [
    "https://services.bc.edu/PublicCourseInfoSched/courseinfoschedResults!displayInput.action?authenticated=false&keyword=&presentTerm=2020S&registrationTerm=2021F&termsString=2020S%2C2020U%2C2021F%2C2021S&selectedTerm=2021F&selectedSort=&selectedSchool=6CSOM&selectedSubject=nullAll&selectedNumberRange=&selectedLevel=All&selectedMeetingDay=&selectedMeetingTime=&selectedCourseStatus=&selectedCourseCredit=&canvasSearchLink=https%3A%2F%2Fsyllabus-search.herokuapp.com%2Forganizations%2F1&personResponse=Gdprs6RFslG6GlulGd8cud2Wsl&googleSiteKey=6LdV2EYUAAAAACy8ROcSlHHznHJ64bn87jvDqwaf",
    "https://services.bc.edu/PublicCourseInfoSched/courseinfoschedResults!displayInput.action?authenticated=false&keyword=&presentTerm=2020S&registrationTerm=2021F&termsString=2020S%2C2020U%2C2021F%2C2021S&selectedTerm=2021F&selectedSort=&selectedSchool=7CSON&selectedSubject=nullAll&selectedNumberRange=All&selectedLevel=All&selectedMeetingDay=All&selectedMeetingTime=All&selectedCourseStatus=All&selectedCourseCredit=All&canvasSearchLink=https%3A%2F%2Fsyllabus-search.herokuapp.com%2Forganizations%2F1&personResponse=Gdprs6RFslG6GlulGd8cud2Wsl&googleSiteKey=6LdV2EYUAAAAACy8ROcSlHHznHJ64bn87jvDqwaf",
    "https://services.bc.edu/PublicCourseInfoSched/courseinfoschedResults!displayInput.action?authenticated=false&keyword=&presentTerm=2020S&registrationTerm=2021F&termsString=2020S%2C2020U%2C2021F%2C2021S&selectedTerm=2021F&selectedSort=&selectedSchool=3LAW&selectedSubject=nullAll&selectedNumberRange=All&selectedLevel=All&selectedMeetingDay=All&selectedMeetingTime=All&selectedCourseStatus=All&selectedCourseCredit=All&canvasSearchLink=https%3A%2F%2Fsyllabus-search.herokuapp.com%2Forganizations%2F1&personResponse=Gdprs6RFslG6GlulGd8cud2Wsl&googleSiteKey=6LdV2EYUAAAAACy8ROcSlHHznHJ64bn87jvDqwaf",
    "https://services.bc.edu/PublicCourseInfoSched/courseinfoschedResults!displayInput.action?authenticated=false&keyword=&presentTerm=2020S&registrationTerm=2021F&termsString=2020S%2C2020U%2C2021F%2C2021S&selectedTerm=2021F&selectedSort=&selectedSchool=8LSOE&selectedSubject=nullAll&selectedNumberRange=All&selectedLevel=All&selectedMeetingDay=All&selectedMeetingTime=All&selectedCourseStatus=All&selectedCourseCredit=All&canvasSearchLink=https%3A%2F%2Fsyllabus-search.herokuapp.com%2Forganizations%2F1&personResponse=Gdprs6RFslG6GlulGd8cud2Wsl&googleSiteKey=6LdV2EYUAAAAACy8ROcSlHHznHJ64bn87jvDqwaf",
    "https://services.bc.edu/PublicCourseInfoSched/courseinfoschedResults!displayInput.action?authenticated=false&keyword=&presentTerm=2020S&registrationTerm=2021F&termsString=2020S%2C2020U%2C2021F%2C2021S&selectedTerm=2021F&selectedSort=&selectedSchool=SSCHR&selectedSubject=nullAll&selectedNumberRange=All&selectedLevel=All&selectedMeetingDay=All&selectedMeetingTime=All&selectedCourseStatus=All&selectedCourseCredit=All&canvasSearchLink=https%3A%2F%2Fsyllabus-search.herokuapp.com%2Forganizations%2F1&personResponse=Gdprs6RFslG6GlulGd8cud2Wsl&googleSiteKey=6LdV2EYUAAAAACy8ROcSlHHznHJ64bn87jvDqwaf",
    "https://services.bc.edu/PublicCourseInfoSched/courseinfoschedResults!displayInput.action?authenticated=false&keyword=&presentTerm=2020S&registrationTerm=2021F&termsString=2020S%2C2020U%2C2021F%2C2021S&selectedTerm=2021F&selectedSort=&selectedSchool=5SSW&selectedSubject=nullAll&selectedNumberRange=All&selectedLevel=All&selectedMeetingDay=All&selectedMeetingTime=All&selectedCourseStatus=All&selectedCourseCredit=All&canvasSearchLink=https%3A%2F%2Fsyllabus-search.herokuapp.com%2Forganizations%2F1&personResponse=Gdprs6RFslG6GlulGd8cud2Wsl&googleSiteKey=6LdV2EYUAAAAACy8ROcSlHHznHJ64bn87jvDqwaf",
    "https://services.bc.edu/PublicCourseInfoSched/courseinfoschedResults!displayInput.action?authenticated=false&keyword=&presentTerm=2020S&registrationTerm=2021F&termsString=2020S%2C2020U%2C2021F%2C2021S&selectedTerm=2021F&selectedSort=&selectedSchool=9STM&selectedSubject=nullAll&selectedNumberRange=All&selectedLevel=All&selectedMeetingDay=All&selectedMeetingTime=All&selectedCourseStatus=All&selectedCourseCredit=All&canvasSearchLink=https%3A%2F%2Fsyllabus-search.herokuapp.com%2Forganizations%2F1&personResponse=Gdprs6RFslG6GlulGd8cud2Wsl&googleSiteKey=6LdV2EYUAAAAACy8ROcSlHHznHJ64bn87jvDqwaf",
    "https://services.bc.edu/PublicCourseInfoSched/courseinfoschedResults!displayInput.action?authenticated=false&keyword=&presentTerm=2020S&registrationTerm=2021F&termsString=2020S%2C2020U%2C2021F%2C2021S&selectedTerm=2021F&selectedSort=&selectedSchool=4ADV&selectedSubject=nullAll&selectedNumberRange=All&selectedLevel=All&selectedMeetingDay=All&selectedMeetingTime=All&selectedCourseStatus=All&selectedCourseCredit=All&canvasSearchLink=https%3A%2F%2Fsyllabus-search.herokuapp.com%2Forganizations%2F1&personResponse=Gdprs6RFslG6GlulGd8cud2Wsl&googleSiteKey=6LdV2EYUAAAAACy8ROcSlHHznHJ64bn87jvDqwaf",
]


def crawl_course_information(csvwriter, url):
    faculty, department, course, desc = "", "", "", ""
    soup = bs(requests.get(url).content, "html.parser")
    for future_course_link in soup.find_all("a", attrs={"class": "futureCourseLink"}):
        data = future_course_link.text.strip()
        course = data.split("(")[1].split(")")[0]
        desc = data.split("(")[0].strip()
        print(course, desc)
        # link = future_course_link.get("href")
        # soup1 = bs(requests.get(start + link).content, "html.parser")
        # maindiv = soup1.find("div", class_="center-block col-xs-12 col-sm-12 col-md-10 col-lg-8")
        # for rows in maindiv.find_all("div", class_='row'):
        #     for div in rows.find_all("div", class_="col-xs-4"):
        #         data = div.text.spilt()
        #         if re.search(r"Department", div.text):
        #             if len(data) > 1:
        #                 department = div.text.split()[1].strip()
        #             else:
        #                 departement = "N/A"
        #         elif re.search(r"Faculty", div.text):
        #             if len(data) > 1:
        #                 faculty = div.text.split()[1].strip()
        #             else:
        #                 faculty = "N/A"
        # print("Writing")
        # csvwriter.writerow([faculty, departement, course, desc]) 
        

def main():
    with open("boston.csv", 'w') as f:
        faculty, department, course, desc = "", "", "", ""
        csvwriter = csv.writer(f)
        csvwriter.writerow(["Faculty", "Department", "Course", "Description"])
        for url in urls:
            print("Go to {}".format(url))
            soup = bs(requests.get(url).content, "html.parser")
            crawl_course_information(csvwriter=csvwriter, url=url)
            # for future_course_link in soup.find_all("a", attrs={"class": "futureCourseLink"}):
            #     data = future_course_link.text.strip()
            #     course = data.split("(")[1].split(")")[0]
            #     desc = data.split("(")[0].strip()
            #     link = future_course_link.get("href")
            #     soup1 = bs(requests.get(start + link).content, "html.parser")
            #     maindiv = soup1.find("div", class_="center-block col-xs-12 col-sm-12 col-md-10 col-lg-8")
            #     for rows in maindiv.find_all("div", class_='row'):
            #         for div in rows.find_all("div", class_="col-xs-4"):
            #             data = div.text.spilt()
            #             if re.search(r"Department", div.text):
            #                 if len(data) > 1:
            #                     department = div.text.split()[1].strip()
            #                 else:
            #                     departement = "N/A"
            #             elif re.search(r"Faculty", div.text):
            #                 if len(data) > 1:
            #                     faculty = div.text.split()[1].strip()
            #                 else:
            #                     faculty = "N/A"

            #     csvwriter.writerow([faculty, department, course, desc])
        # option = webdriver.ChromeOptions()
        # option.add_argument('headless')
        # option.add_argument('no-sandbox')
        # option.add_argument('disable-dev-shm-usage')
        # option.add_argument('disable-gpu')
        # driver = webdriver.Chrome(options=option)
        # driver.get("http://services.bc.edu/PublicCourseInfoSched/")
        # for prefix in prefixes:
        #     print("searching for course: {}".format(prefix))
            
        #     WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="search"]')))
        #     search_button = driver.find_element_by_xpath('//*[@id="search"]')

        #     WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="keyword"]')))
        #     search_box = driver.find_element_by_xpath('//*[@id="keyword"]')
        #     search_box.clear()
            
        #     driver.execute_script("arguments[0].click();", search_box)
        #     search_box.send_keys(prefix)
        #     driver.execute_script("arguments[0].click();", search_button)
        #     current_url = driver.current_url
        #     crawl_course_information(csvwriter, current_url)
            
if __name__ == '__main__':
    main()