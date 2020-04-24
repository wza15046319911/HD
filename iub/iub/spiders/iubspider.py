# -*- coding: utf-8 -*-
import copy

import scrapy
from bs4 import BeautifulSoup as bs

from ..items import IubItem


class IubspiderSpider(scrapy.Spider):
    name = 'iubspider'
    allowed_domains = ['https://utilities.registrar.indiana.edu']
    start_urls = ['https://utilities.registrar.indiana.edu/course-browser/prl/soc4202/index.shtml']

    def parse(self, response):
        item = IubItem()
        for res in response.xpath('//div[@id="crsebrowser"]//td/strong/a'):
            faculty = res.xpath('../following-sibling::text()').extract_first().strip()
            item['faculty'] = faculty
            u = res.xpath('./@href').extract_first()
            url = response.urljoin(u)
            yield scrapy.Request(url=url, meta={'item': copy.deepcopy(item)}, dont_filter=True,
                                 callback=self.parse_next)

    def parse_next(self, response):
        item = response.meta['item']
        for re in response.xpath('//div[@id="crsebrowser"]//strong/a'):
            course = re.xpath('./text()').extract_first().strip()
            title = re.xpath('../following-sibling::text()').extract_first().strip()
            item['course'] = course
            item['title'] = title
            print(item)
            yield item
