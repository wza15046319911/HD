import requests
from bs4 import BeautifulSoup as bs
import re
import time
import csv
import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import asyncio
import aiohttp

# f = open("MQ1.csv", "w")
# w = csv.writer(f)
# w.writerow(["Faculty", "Course", "Title"])

# 信号量，控制协程数，防止爬的过快
num_of_semaphores = asyncio.Semaphore(10)


async def spider_by_requests(i, data, step_size, url, headers):
    async with num_of_semaphores:
        async with aiohttp.ClientSession() as s:
            async with s.request(url=url, headers=headers, method='POST', json=data) as res:
                # t = await res.read()
                print("Now in page: {}".format(i // step_size + 1))
                r = await res.read()
                js1 = json.loads(r)
                for d in js1.get("contentlets"):
                    course_code, course_info, course_title = "N/A", "N/A", "N/A"
                    if d.get('code'):
                        course_code = d.get('code')
                    if d.get('title'):
                        course_title = d.get("title")
                    if d.get('data'):
                        # data 是以json格式返回，需要转化成字典
                        course_info = json.loads(d.get("data"))
                        if course_info.get("school"):
                            if course_info.get("school").get("value"):
                                faculty = course_info.get("school").get("value")
                                print("Writing row: {}".format([faculty, course_code, course_title]))
                                # 正则表达式直接匹配json格式的字符串，可能会报错
                                # regex = re.search(r'"school":\{"value":(?P<faculty>.*),"cl_id":.*,"enrolment_rules":.*\}', course_info)
                                # regex = regex.groupdict()
                                # faculty = re.sub(r'\"', '', regex['faculty'])
                                # w.writerow([faculty, course_code, course_title])
                                # f.flush()


def main():
    # 创建事件循环对象
    loop = asyncio.get_event_loop()
    tasks = []

    # 参数
    url = "https://coursehandbook.mq.edu.au/api/es/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
    }
    # Start from page 1
    start = 0
    # Until page 38
    end = 3760
    # Load 100 results per page
    step_size = 100
    for i in range(start, end, step_size):
        # 请求的同时，发送json数据
        data = {"query": {"bool": {"must": [{"term": {"live": True}}, [{"bool": {"minimum_should_match": "100%",
                                                                                 "should": [{"query_string": {
                                                                                     "fields": ["*implementationYear*"],
                                                                                     "query": "*2020*"}}]}}]],
                                   "filter": [
                                       {"terms": {"contenttype": ["mq2_psubject", "mq2_paos", "mq2_pcourse"]}}]}},
                "sort": {"mq2_psubject.code_dotraw": "asc", "mq2_paos.title_dotraw": "asc",
                         "mq2_pcourse.title_dotraw": "asc"}, "from": i, "size": step_size, "track_scores": True,
                "_source": {"includes": ["*.code", "*.name", "*.award_titles", "*.keywords", "urlmap", "contenttype"],
                            "excludes": ["", None]}}

        tasks.append(spider_by_requests(i, data, step_size, url, headers))

    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


if __name__ == '__main__':
    main()
