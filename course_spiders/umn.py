import csv
import multiprocessing
from multiprocessing import Pool
import requests
import urllib3
from fake_useragent import UserAgent
from lxml import etree
import sys
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
import re

# 需要转义的符号有:
# * . ? + $ ^ [ ] ( ) { } | \ /

# 禁用警告
urllib3.disable_warnings()

# 加载web驱动路径
web_path = 'D:/chromedriver'


class Pipeline(object):
    def __init__(self):
        # 打开文件，指定方式为写，利用newline=''参数把csv写数据时产生的空行消除
        self.file = open('umn1.csv', 'a+', newline='', encoding='utf-8-sig')
        # 设置文件第一行的字段名，注意要跟spider传过来的字典item的key名称相同
        self.fieldnames = ['t1', 't2', 't3', 'code', 'name']
        # 指定文件的写入方式为csv字典写入，参数1为指定具体文件，参数2为指定字段名
        self.writer = csv.DictWriter(self.file, fieldnames=self.fieldnames)
        # 写入第一行字段名，因为只要写入一次，所以文件放在__init__里面
        self.writer.writeheader()

    def process_item(self, item):
        self.writer.writerow(item)
        return item

    def __del__(self):
        self.file.close()


# 程序主入口
def Test(a1, a2):
    print('---初始化中---')
    p = Pipeline()
    # 定义chrome的配置
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    option.add_argument('no-sandbox')
    option.add_argument('disable-dev-shm-usage')
    option.add_argument('disable-gpu')
    # 修改chrome的配置
    prefs = {
        'profile.default_content_setting_values': {
            'images': 2,  # 限制图片加载
            # 'javascript': 2  # 禁用js
        }
    }
    # 将变量传入
    option.add_experimental_option('prefs', prefs)
    # 传入驱动路径，导入设置，生成webdriver.Chrome对象
    browser = webdriver.Chrome(executable_path=web_path, chrome_options=option)
    # 加载目标地址
    browser.get('https://www.myu.umn.edu/psp/psprd/EMPLOYEE/CAMP/c/SA_LEARNER_SERVICES.CLASS_SEARCH.GBL?')
    print('---加载中---')

    # def pares_1(self):
    #     # 切换句柄，选择框在iframe标签里面，需要定位并切换，切换到第一个iframe
    #     WebDriverWait(self.browser, 60).until(
    #         EC.presence_of_element_located((By.XPATH, '//iframe[@id="ptifrmtgtframe"]')))
    #     self.browser.switch_to.frame("ptifrmtgtframe")
    #     print('切换到第一个iframe')
    #
    #     # 点击选择查找数据的按钮
    #     WebDriverWait(self.browser, 60).until(
    #         EC.presence_of_element_located((By.XPATH, '//span[text()="Course Information"]')))
    #     self.browser.find_element_by_xpath('//span[text()="Course Information"]').click()
    #     print('点击查看数据的选项按钮')
    #
    #     # 获取并选择第一个下拉框
    #     WebDriverWait(self.browser, 60).until(EC.presence_of_element_located((By.ID, "CATLG_SRCH_WRK_INSTITUTION$5$")))
    #     selector_1 = Select(self.browser.find_element_by_id("CATLG_SRCH_WRK_INSTITUTION$5$"))
    #     selector_1.select_by_value('UMNCR')
    #     print('点击第一个选项:Crookston')
    #     time.sleep(3)
    #
    #     # 获取并选择第二个下拉框
    #     WebDriverWait(self.browser, 60).until(
    #         EC.presence_of_element_located((By.XPATH, "//select[@name='CATLG_SRCH_WRK_CAMPUS']/option")))
    #     selector_2 = Select(self.browser.find_element_by_id("CATLG_SRCH_WRK_CAMPUS"))
    #     selector_2.select_by_value('UMNCR')
    #     print('点击第二个选项:Crookston')
    #     time.sleep(3)
    #
    #     # 点击第三个弹出下拉框
    #     submit = WebDriverWait(self.browser, 60).until(
    #         EC.presence_of_element_located((By.ID, "CATLG_SRCH_WRK_SUBJECT$6$$prompt")))
    #     self.browser.execute_script("arguments[0].click();", submit)
    #     print('点击第三个按钮')
    #     time.sleep(3)
    #
    #     # 初始化iframe
    #     self.browser.switch_to.default_content()
    #     print('退出所有iframe，初始化')
    #
    #     # 切换到第二个iframe
    #     WebDriverWait(self.browser, 60).until(
    #         EC.presence_of_element_located((By.XPATH, '//iframe[contains(@name,"ptModFrame")]')))
    #     self.browser.switch_to.frame(self.browser.find_element_by_xpath('//iframe[contains(@name,"ptModFrame")]'))
    #     print('切换到第二个iframe')
    #
    #     # 获取并遍历下拉列表
    #     WebDriverWait(self.browser, 60).until(
    #         EC.presence_of_element_located((By.XPATH, "//td[@scope='row']/a[@class='PSSRCHRESULTSODDROW']")))
    #     # 创建下拉列表集合
    #     select_list = []
    #     for res in self.browser.find_elements_by_xpath("//td[@scope='row']/a[@class='PSSRCHRESULTSODDROW']"):
    #         select_list.append(res.find_element_by_xpath('.').get_attribute("id"))
    #
    #     print(select_list)

    # 切换句柄，选择框在iframe标签里面，需要定位并切换，切换到第一个iframe
    WebDriverWait(browser, 60).until(
        EC.presence_of_element_located((By.XPATH, '//iframe[@id="ptifrmtgtframe"]')))
    browser.switch_to.frame("ptifrmtgtframe")
    print('切换到第一个iframe')

    # 点击选择查找数据的按钮
    WebDriverWait(browser, 60).until(
        EC.presence_of_element_located((By.XPATH, '//span[text()="Course Information"]')))
    browser.find_element_by_xpath('//span[text()="Course Information"]').click()
    print('点击查看数据的选项按钮')

    # 获取并选择第一个下拉框
    WebDriverWait(browser, 60).until(EC.presence_of_element_located((By.ID, "CATLG_SRCH_WRK_INSTITUTION$5$")))
    selector_1 = Select(browser.find_element_by_id("CATLG_SRCH_WRK_INSTITUTION$5$"))
    selector_1.select_by_value(a1)
    print('点击第一个选项')
    time.sleep(3)

    # 获取并选择第二个下拉框
    WebDriverWait(browser, 60).until(
        EC.presence_of_element_located((By.XPATH, "//select[@name='CATLG_SRCH_WRK_CAMPUS']/option")))
    selector_2 = Select(browser.find_element_by_id("CATLG_SRCH_WRK_CAMPUS"))
    selector_2.select_by_value(a2)
    print('点击第二个选项')
    time.sleep(3)

    # 点击第三个弹出下拉框
    submit = WebDriverWait(browser, 60).until(
        EC.presence_of_element_located((By.ID, "CATLG_SRCH_WRK_SUBJECT$6$$prompt")))
    browser.execute_script("arguments[0].click();", submit)
    print('点击第三个按钮')
    time.sleep(3)

    # 初始化iframe
    browser.switch_to.default_content()
    print('退出所有iframe，初始化')

    # 切换到第二个iframe
    WebDriverWait(browser, 60).until(
        EC.presence_of_element_located((By.XPATH, '//iframe[contains(@name,"ptModFrame")]')))
    browser.switch_to.frame(browser.find_element_by_xpath('//iframe[contains(@name,"ptModFrame")]'))
    print('切换到第二个iframe')

    # 选择并点击下拉列表
    WebDriverWait(browser, 60).until(
        EC.presence_of_element_located((By.XPATH, "//td[@scope='row']/a[contains(@class,'PSSRCHR')]")))

    # 遍历
    for x in range(999):

        time.sleep(1)

        item_list = browser.find_elements_by_xpath("//td[@scope='row']/a[contains(@class,'PSSRCHR')]")

        time.sleep(1)

        try:
            time.sleep(1)
            print('开始循环选择并点击')
            browser.execute_script("arguments[0].click();", item_list[x])
            # item_list[x].click()
            time.sleep(3)
        except:
            print('未获取到选项列表终止循环')
            break

        # 初始化iframe
        browser.switch_to.default_content()
        print('退出所有iframe，初始化')

        # 切换到第一个iframe
        WebDriverWait(browser, 60).until(
            EC.presence_of_element_located((By.XPATH, '//iframe[@id="ptifrmtgtframe"]')))
        browser.switch_to.frame("ptifrmtgtframe")
        print('切换到第一个iframe')

        # 点击查找，无法click，只能js触发
        submit_2 = WebDriverWait(browser, 60).until(
            EC.presence_of_element_located((By.XPATH, '//input[@value="Search"]')))
        browser.execute_script("arguments[0].click();", submit_2)
        print('点击查找')

        time.sleep(1)

        # 判断是否有弹窗
        # 初始化iframe
        browser.switch_to.default_content()
        print('退出所有iframe，初始化')

        try:
            # 特殊情况出现弹窗点击ok
            WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, '//input[@id="#ICOK"]')))
            browser.find_element_by_xpath('//input[@id="#ICOK"]').click()
            print('有弹窗则点击ok继续')

            time.sleep(1)

            # 切换到第一个iframe
            WebDriverWait(browser, 60).until(
                EC.presence_of_element_located((By.XPATH, '//iframe[@id="ptifrmtgtframe"]')))
            browser.switch_to.frame("ptifrmtgtframe")
            print('切换到第一个iframe')

        except:
            # 切换到第一个iframe
            WebDriverWait(browser, 60).until(
                EC.presence_of_element_located((By.XPATH, '//iframe[@id="ptifrmtgtframe"]')))
            browser.switch_to.frame("ptifrmtgtframe")
            print('切换到第一个iframe')

            print('无弹窗则继续')

        try:
            # 解析数据
            WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.XPATH, '//td/div/span[@class="PALEVEL0SECONDARY"]')))
            for re in browser.find_elements_by_xpath('//td/div/span[@class="PALEVEL0SECONDARY"]'):
                item = {}
                item['t1'] = \
                    browser.find_element_by_xpath('//span[@id="DERIVED_CRSECAT_SSS_PAGE_KEYDESCR"]').text.split('|')[
                        0].strip()
                item['t2'] = \
                    browser.find_element_by_xpath('//span[@id="DERIVED_CRSECAT_SSS_PAGE_KEYDESCR"]').text.split('|')[
                        1].strip()
                item['t3'] = \
                    browser.find_element_by_xpath('//span[@id="DERIVED_CRSECAT_SSS_PAGE_KEYDESCR"]').text.split('|')[
                        2].strip()
                item['code'] = re.find_element_by_xpath('.').text.split('-')[0].strip()
                item['name'] = '-'.join(re.find_element_by_xpath('.').text.split('-')[1:]).strip()
                p.process_item(item)
                print(item)

            time.sleep(2)

            # 解析完毕后返回
            WebDriverWait(browser, 60).until(
                EC.presence_of_element_located((By.XPATH, '//a[@id="CATLG_SRCH_WRK_CLASS_BASIC_LINK"]')))
            browser.find_element_by_xpath('//a[@id="CATLG_SRCH_WRK_CLASS_BASIC_LINK"]').click()
            print('点击返回主页面继续查找')

        except:
            print('无数据')
            pass

        time.sleep(1)

        # 点击第三个弹出下拉框
        submit = WebDriverWait(browser, 60).until(
            EC.presence_of_element_located((By.ID, "CATLG_SRCH_WRK_SUBJECT$6$$prompt")))
        browser.execute_script("arguments[0].click();", submit)
        print('点击第三个按钮')
        time.sleep(3)

        # 初始化iframe
        browser.switch_to.default_content()
        print('退出所有iframe，初始化')

        # 切换到第二个iframe
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//iframe[contains(@name,"ptModFrame")]')))
        browser.switch_to.frame(browser.find_element_by_xpath('//iframe[contains(@name,"ptModFrame")]'))
        print('切换到第二个iframe')

        time.sleep(1)


if __name__ == '__main__':
    print('当前环境CPU核数是：%d核' % multiprocessing.cpu_count())
    p = Pool(5)  # 进程池
    for u in [{'a': 'UMNCR', 'b': 'UMNCR'}, {'a': 'UMNDL', 'b': 'UMNDL'}, {'a': 'UMNMO', 'b': 'UMNMO'},
              {'a': 'UMNTC', 'b': 'UMNRO'}, {'a': 'UMNTC', 'b': 'UMNTC'}]:
        p.apply_async(Test, args=(u['a'], u['b']))
    p.close()
    p.join()
