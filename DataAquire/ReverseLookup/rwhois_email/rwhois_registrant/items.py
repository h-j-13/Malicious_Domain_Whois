#!/usr/bin/env python
# encoding:utf-8

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RwhoisRegistrantItem(scrapy.Item):
    # define the fields for your item here like:
    domain = scrapy.Field()
    registrant = scrapy.Field()
