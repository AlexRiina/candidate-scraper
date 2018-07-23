from urllib.parse import urljoin, urlparse

from scraper import items
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class Candidate(CrawlSpider):
    name = 'candidate'

    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 2,
        'CLOSESPIDER_PAGECOUNT': 50,
    }

    rules = [
        Rule(LinkExtractor(allow=()), callback='parse', follow=True),
    ]

    def __init__(self, domain):
        super().__init__()
        self.domain = urlparse(domain).path
        self.start_urls = [urljoin("http://", domain).replace('///', '//')]
        self.allowed_domains = [urlparse(u).netloc for u in self.start_urls]

    def parse(self, response):
        for handle in response.xpath("//a[contains(@href,'twitter.com')]/@href").extract():
            yield items.Twitter(twitter=handle, domain=self.domain)

        # regex will match all reasonable email addresses.
        # regex sort of courtesy of https://www.regular-expressions.info/email.html
        for email in response.xpath("//a/@href").re(r'\b[\w._%+-]+@[\w._%+-]+\b'):
            yield items.EmailAddress(email=email, domain=self.domain)
