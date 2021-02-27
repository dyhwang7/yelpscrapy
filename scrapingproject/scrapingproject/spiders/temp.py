
#-*- coding: utf-8 -*-
import scrapy
import re
from bs4 import BeautifulSoup
import pandas as pd


class OurfirstbotSpider(scrapy.Spider):
    name = 'ourfrstbot'
    allowed_domains = ['yelp.com']
    items = {'name': [], 'description': [], 'rating': [], 'review_count': []}
    start_urls = ['https://www.yelp.com/search?find_desc=Landmarks%20%26%20Historical%20Buildings&find_loc=Los%20Angeles%2C%20CA&ns=1&start=0/']

    def parse(self, response):
        urls = ['https://www.yelp.com/search?find_desc=Landmarks%20%26%20Historical%20Buildings&find_loc=Los%20Angeles%2C%20CA&ns=1&'
                'start={}'.format(i) for i in range (0, 70, 10)]
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_page)
        #return pandas data frame and do the sorting/splitting in another module
        #add to pandas dataframe
        global items

        x = pd.DataFrame(self.items)
        print('\n\n\n HELLO')
        print(x)

    def parse_page(self, response):
        print('\n\n\nPARSE_PAGE CALLED' + response.url)
        names = response.css('.heading--h4__09f24__2ijYq::text').extract()
        descriptions = response.css('.gutter-auto__09f24__2WJTk>.arrange-unit__09f24__1gZC1').extract()
        ratings = response.css('div[class*=i-stars__09f24__1T6rz]::attr(aria-label)').extract()
        review_count = response.css('.reviewCount__09f24__EUXPN::text').extract()
        global items
        for item in zip(names, descriptions, ratings, review_count):
                self.items['name'].append(BeautifulSoup(item[0]).text),
                self.items['description'].append(BeautifulSoup(item[1]).text),
                self.items['rating'].append(self.parsenum(BeautifulSoup(item[2]).text)),
                self.items['review_count'].append(BeautifulSoup(item[3]).text),

        # nextpage = response.css('a[class*=navigation-button__09f24__3F7Pt]::attr(href)').extract_first()
        # if nextpage:
        #     yield scrapy.Request(nextpage,callback=self.parse)
        # return

    def parsenum(self, string):
        m = re.search(r"(\d*\.?\d*)", string)
        return m.group() if m else None