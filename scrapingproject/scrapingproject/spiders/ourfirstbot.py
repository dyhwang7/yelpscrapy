# -*- coding: utf-8 -*-
import scrapy
import re
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess
import pandas as pd
import csv

class OurfirstbotSpider(scrapy.Spider):
    name = 'ourfirstbot'
    allowed_domains = ['yelp.com']
    output = pd.DataFrame(columns=['name', 'description', 'rating', 'review_count'])
    start_urls = []

    def __init__(self):
        url = 'https://www.yelp.com/search?find_desc=Landmarks%20%26%20Historical%20Buildings&find_loc=Los%20Angeles%2C%20CA&ns=1&start='

        for i in range(0, 70, 10):
            self.start_urls.append(url + str(i))

        # return pandas data frame and do the sorting/splitting in another module
        # add to pandas dataframe

    def parse(self, response):

        names = response.css('.heading--h4__09f24__2ijYq').extract()
        descriptions = response.css('.gutter-auto__09f24__2WJTk>.arrange-unit__09f24__1gZC1').extract()
        ratings = response.css('div[class*=i-stars__09f24__1T6rz]::attr(aria-label)').extract()
        review_count = response.css('.reviewCount__09f24__EUXPN::text').extract()

        for item in zip(names, descriptions, ratings, review_count):
            all_items = {
                'name': self.name_isolator(BeautifulSoup(item[0]).text),
                'description': BeautifulSoup(item[1]).text,
                'rating': float(self.parsenum(BeautifulSoup(item[2]).text)),
                'review_count': float(BeautifulSoup(item[3]).text),
            }
            self.output = self.output.append(all_items, ignore_index=True)


        self.output.to_csv('output.csv', index = False)
        # nextpage = response.css('a[class*=navigation-button__09f24__3F7Pt]::attr(href)').extract_first()
        # if nextpage:
        #     yield scrapy.Request(nextpage,callback=self.parse)
        # return

    def name_isolator(self, string):
        m = re.search(r'(?<=\s).*', string)
        return m.group() if m else None
    def parsenum(self, string):
        m = re.search(r"(\d*\.?\d*)", string)
        return m.group() if m else None

