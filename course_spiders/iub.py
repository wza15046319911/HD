import requests
from bs4 import BeautifulSoup as bs
import re
import time
import csv
import asyncio
import aiohttp
from aiohttp import ClientSession

f = open("IUB.csv", 'w')
w = csv.writer(f)
w.writerow(["Faculty/School", "Course", "Title"])

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    "Cookie": "__utmc=189522035; __utmz=189522035.1586945229.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utma=189522035.1808391622.1586945229.1586945229.1587003784.2",
    "Referer": "Referer: https://registrar.indiana.edu/browser/index.shtml",
    "Connection": "keep-alive"
}



tasks = []

# num_of_semaphores = aiohttp.Semaphore(10)

async def spider(url):
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            content = response.content
            soup = bs(content, "html.parser")
            div = soup.find("div", attrs={"id": "crsebrowser"})
            tr = div.find("tr")
            faculties = [i.split(" ", 1)[1] for i in tr.text.split("\n") if i]
            course_prefix = [strong.contents[0] for strong in div.find_all("strong")]
            new = list(zip(course_prefix, faculties))
            for item in new:
                a, faculty = item
                suffix = a.get("href")
                print(a.text)
    # content1 = requests.get(prefix+suffix).content
    # soup1 = bs(content1, "html.parser")
    # div1 = soup1.find("div", attrs={"id": "crsebrowser"})
    # for strong1 in div1.find_all("strong"):
    #     a1 = strong1.contents[0]
    #     regex = a1.get("href")
    #     link = prefix+suffix
    #     content2 = requests.get(link.replace("index.shtml", regex)).content
    #     soup2 = bs(content2, "html.parser")
    #     pres = soup2.find_all("pre")
    #     if len(pres) > 0:
    #         course_info = pres[1]
    #         b = course_info.find("b")
    #         data = b.text.split("  ")
    #         course = data[0].replace(" ", "")
    #         if len(data) > 1:
    #             title = data[1]
    #             print("Writing row: {}".format([faculty, course, title]))
    #             w.writerow([faculty, course, title])
    #             f.flush()

def run():
    prefix = "https://utilities.registrar.indiana.edu/course-browser/prl/soc4202/"
    url = prefix + "index.shtml"
    tasks.append(asyncio.ensure_future(spider(url)))
        

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    run()
    loop.run_until_complete(asyncio.wait(tasks))