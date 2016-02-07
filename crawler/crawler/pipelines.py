# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from logging import getLogger

from settings import OUTPUT_FILE


log = getLogger(__name__)


class CrawlerPipeline(object):
    def process_item(self, item, spider):
        log.info("recording item: {}".format(item['appid']))

        with open(OUTPUT_FILE, 'awb') as dat_file:
            dat_file.write("{}\t{}\t{}\t{}\n".format(item['appid'], item['title'], item['intro'], item['recommended']))
        return item
