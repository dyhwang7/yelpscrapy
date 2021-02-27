#-*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup


class OurfirstbotSpider(scrapy.Spider):
    name = 'ourfirstbot'
    allowed_domains = ['www.yelp.com/search?find_desc=Landmarks+%26+Historical+Buildings&find_loc=Los+Angeles%2C+CA']
    start_urls = ['www.yelp.com/search?find_desc=Landmarks+%26+Historical+Buildings&find_loc=Los+Angeles%2C+CA']

    def parse(self, response):
        names = response.css('.heading--h3__09f24__3gZ0A').extract()

        for item in zip(names):
            all_items = {
                'name' : BeautifulSoup(item[0]).text
            }
        pass
