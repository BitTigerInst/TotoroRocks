import re
from logging import getLogger

from crawler.items import AppstoreItem

import scrapy
from scrapy.selector import Selector


log = getLogger(__name__)

# constants
ENCODING = 'utf-8'
RANK_PAGE_XPATHS = {
  'hrefs': '//h4[@class="title"]/a/@href'
}

RELATED_RANKING_XPATHS = {
    'ranks': '//div[@class="open-info"]',
    'url': './p[@class="name"]/a/@href',
    'name': './p[@class="name"]/a/text()'
}

PRODUCT_PAGE_XPATHS = {
    'title': '//ul[@class="app-info-ul nofloat"]/li/p/span[@class="title"]/text()',
    'intro': '//meta[@name="description"]/@content',
    'related_apps': RELATED_RANKING_XPATHS
}

APPID_REGEX = r'http://.*/(?P<appid>.*)'


class HuaweiSpider(scrapy.Spider):
    name = 'huawei'
    allowed_domains = ['huawei.com']

    start_urls = [
        'http://appstore.huawei.com/more/all'
    ]

    def parse(self, response):
        page = Selector(response)

        hrefs = page.xpath(RANK_PAGE_XPATHS['hrefs'])

        for href in hrefs:
            url = href.extract()
            yield scrapy.Request(url, callback=self.parse_item)

    def parse_item(self, response):
        page = Selector(response)

        # parse app information from product page
        item = AppstoreItem()

        for field in ['title', 'intro']:
            item[field] = page.xpath(PRODUCT_PAGE_XPATHS[field]).extract_first().encode(ENCODING)
        item['url'] = response.url
        item['appid'] = re.match(APPID_REGEX, item['url']).group('appid')

        # parse related apps info
        rank_xpaths = PRODUCT_PAGE_XPATHS['related_apps']
        rank_divs = page.xpath(rank_xpaths['ranks'])
        related_apps = []
        for div in rank_divs:
            url = div.xpath(rank_xpaths['url']).extract_first()
            name = div.xpath(rank_xpaths['name']).extract_first().encode(ENCODING)
            recommended_appid = re.match(APPID_REGEX, url).group('appid')
            related_apps.append('{}:{}'.format(recommended_appid, name))
        item['recommended'] = ", ".join(related_apps)

        yield item
