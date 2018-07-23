"""
For the most part, candidates will have one twitter and one preferred email,
but we're looking through the data manually to pick the right one since
multiple handles and emails appear on their sites.
"""

import scrapy


class EmailAddress(scrapy.Item):
    domain = scrapy.Field()
    email = scrapy.Field()


class Twitter(scrapy.Item):
    domain = scrapy.Field()
    twitter = scrapy.Field()
