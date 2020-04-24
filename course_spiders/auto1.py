from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import re
import time
driver = webdriver.Chrome()
url = "https://www.library.uq.edu.au/"
dropbox_style = ".style-scope.uqlibrary-search.x-scope.paper-icon-button-0"
item_style = ".style-scope.uqlibrary-search.x-scope.paper-item-0"
input_style = ".style-scope.paper-input"
search_button = ".button-colored-accent.style-scope.uqlibrary-search.x-scope.paper-button-0"

driver.get(url)
action = ActionChains(driver)
element = driver.find_element_by_css_selector(dropbox_style)
action.move_to_element(element).click().perform()
elements = driver.find_elements_by_css_selector(item_style)
for i in elements:
    if re.search(r"Past exam papers", i.text):
        action.move_to_element(i).click().perform()
        break
textbox = driver.find_element_by_css_selector(input_style)
action.move_to_element(textbox).click().perform()
textbox.clear()
time.sleep(2)
textbox.send_keys("CSSE1001")
button = driver.find_element_by_css_selector(search_button)
button.click()
print(driver.current_url)
time.sleep(2)
driver.quit()