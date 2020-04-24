import requests
from bs4 import BeautifulSoup as bs
import re
import time
import csv
import asyncio
import aiohttp

# f = open("IUB.csv", 'w')
# w = csv.writer(f)
# w.writerow(["Faculty/School", "Course", "Title"])

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    "Cookie": "__utmc=189522035; __utmz=189522035.1586945229.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utma=189522035.1808391622.1586945229.1586945229.1587003784.2",
    "Referer": "Referer: https://registrar.indiana.edu/browser/index.shtml",
    "Connection": "keep-alive"
}

# 信号量，控制协程数，防止爬的过快
num_of_semaphores = asyncio.Semaphore(10)

# url地址列表
url_list = ["https://utilities.registrar.indiana.edu/course-browser/prl/soc4202/"]


async def spider(url):
    async with num_of_semaphores:
        async with aiohttp.ClientSession() as s:
            async with s.request(url=url, headers=headers, method='GET') as response:
                content = await response.read()
                soup = bs(content, "html.parser")
                div = soup.find("div", attrs={"id": "crsebrowser"})
                tr = div.find("tr")
                faculties = [i.split(" ", 1)[1] for i in tr.text.split("\n") if i]
                course_prefix = [strong.contents[0] for strong in div.find_all("strong")]
                new = list(zip(course_prefix, faculties))
                for item in new:
                    a, faculty = item
                    suffix = a.get("href")
                    # print(a.text)
                    async with s.request(url=url_list[0] + suffix, headers=headers, method='GET') as re:
                        content1 = await re.read()
                        soup1 = bs(content1, "html.parser")
                        div1 = soup1.find("div", attrs={"id": "crsebrowser"})
                        for strong1 in div1.find_all("strong"):
                            a1 = strong1.contents[0]
                            regex = a1.get("href")
                            link = url_list[0] + suffix
                            async with s.request(url=link.replace("index.shtml", regex), headers=headers,method='GET') as r:
                                content2 = await r.read()
                                soup2 = bs(content2, "html.parser")
                                pres = soup2.find_all("pre")
                                if len(pres) > 0:
                                    course_info = pres[1]
                                    b = course_info.find("b")
                                    data = b.text.split("  ")
                                    course = data[0].replace(" ", "")
                                    if len(data) > 1:
                                        title = data[1]
                                        print("Writing row: {}".format([faculty, course, title]))


def main():
    # 创建事件循环对象
    loop = asyncio.get_event_loop()
    tasks = []
    for u in url_list:
        url = u + "index.shtml"
        tasks.append(spider(url))
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()


if __name__ == '__main__':
    main()
