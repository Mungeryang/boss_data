# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BossZhipinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    location = scrapy.Field()
    company = scrapy.Field()
    salary = scrapy.Field()
    edu = scrapy.Field()
    experience = scrapy.Field()
    skills = scrapy.Field()
    demand = scrapy.Field()
    pass
