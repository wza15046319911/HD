from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import re
import time
import pdfkit
import pymysql
import os

def download_course_profile(course, driver):
    url = "https://my.uq.edu.au/programs-courses/search.html?keywords={}&searchType=all&archived=true".format(course)
    print("Proceed course: {}\n".format(course))
    driver.get(url)
    action = ActionChains(driver)
    links = driver.find_elements_by_tag_name("a")
    for link in links:
        if re.search(course, link.text):
            action.move_to_element(link)
            action.click(link).perform()
            break
    for ilink in driver.find_elements_by_tag_name("tr"):
        if re.search(r"Semester 1, 2020.*St Lucia.*Internal", ilink.text):
            url1 = ilink.find_element_by_tag_name("a").get_attribute("href")
            print("Switching to new url: {}\n".format(url1))
            driver.get(url1)
            profile = driver.find_element_by_class_name("current").find_element_by_class_name("course-offering-profile")
            print(profile.text)
            if not re.search(r"COURSE PROFILE", profile.text):
                print("This course is still unavailable.\n")
                return 
            else:
                url2 = profile.find_element_by_tag_name("a").get_attribute("href")
                end = url2.rfind("/")
                first_part = url2.split("section_1")[0]
                serial_number = url2[end+1:]
                url3 = "{}print/{}?print_section_5=1".format(first_part, serial_number)
                print("Switching to the view printing page.\n")
                driver.get(url3)
                pdfkit.from_url(url3, "profiles/{}.pdf".format(course))
                print("Finish proceeding course: {}\n".format(course))
                break
def main():
    start = time.time()
    print("Start task\n")
    print("-----" * 5)
    try:
        os.mkdir("lab_profiles")
    except Exception as e:
        print("lab_profiles already exists!\n")
    driver = webdriver.Chrome()
    driver.set_window_size(400, 300)
    courses = [
        "ENGG1100", "ENGG1300", "ENGG1400", "ENGg1500",
        "MATH1052", "STAT1201", "CSSE1001", "CSSE7030",
        "CSSE2002", "CSSE7023", "CSSE2010", "CSSE7201",
        "CHEM1200", "INFS1200", "INFS7900", "CHEM1100",
        "INFS3200", "INFS7907", "MATH1050", "MATH1051",
        "MATH1052", "ELEC2003", "ELEC3400", "ELEC3004"
        "MATH1061", "MATH7861", "PHYS1002", "SCIE1000",
        "DECO7140", "DECO2500", "DECO7250", "INFS3202",
        "INFS7202", "INFS3208", "INFS7208", "CSSE2310",
        "CSSE7231", "DECO1400", "DECO1100"
    ]
    courses2 = ['FINM7401', 'FINM7402', 'FINM7403', 'FINM7405', 
            'FINM7406', 'ACCT7102', 'ACCT7103', 'ACCT7106', 
            'ACCT7104', 'ECON7000', 'ECON7110', 'ECON7021', 
            'ECON7310', 'MGTS7301', 'MGTS7608', 'MGTS7512', 
            'MGTS7610', 'BISM7202', 'ECON7002', 'FINM7409', 
            'ECON7070', 'ECON7030', 'ECON7300', 'ACCT7101', 
            'ACCT7107', 'LAWS7023', 'LAWS7012', 'BISM7206', 
            'ECON1310', 'BISM1201', 'ACCT1110', 'ECON2300', 
            'LAWS1100', 'FINM1415', 'MGTS3301', 'FINM2416', 
            'ECON1020', 'ECON1011', 'ECON1010', 'ACCT2102', 
            'ACCT2110', 'FINM3405', 'ACCT1101', 'MGTS1301']
    for course in courses:
        download_course_profile(course, driver)
    print("Procedure finishes lab profiles extraction.\n")
    print("Procedure starts extracting other profiles.\n")
    try:
        os.mkdir("other_profiles")
    except Exception as e:
        print("other_profiles already exists!\n") 
    for course in courses2:
        download_course_profile(course, driver)
    print("Procedure finishes in {} seconds.".format(time.time() - start)) 
    
    
# if __name__ == '__main__':
#     main()

def connect_database():
    db = pymysql.connect("localhost", "root", "wza7626222", "ECP") 
    cursor = db.cursor()
    cursor.execute("SHOW DATABASES")
    data = cursor.fetchone()
    print(data)
    db.close()
connect_database()