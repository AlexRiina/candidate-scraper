from collections import defaultdict
from scrapy.exceptions import DropItem
from scrapy.exporters import CsvItemExporter
from scraper import items
from urllib.parse import urlparse


class DeuplicatesPipeline:
    def __init__(self):
        self.emails_seen = set()
        self.twitter_handles_seen = set()

    def process_item(self, item, spider):
        if isinstance(item, items.EmailAddress):
            return self.process_email(item, spider)
        elif isinstance(item, items.Twitter):
            return self.process_twitter(item, spider)
        else:
            return item

    def process_email(self, item, spider):
        """ export unique email that looks valid """
        email = item['email'].lower()

        if any(x in email for x in [
                'godaddy.com', 'example.com', 'wordpress', 'webmaster',
                'donate']):
            raise DropItem("not candidate email")

        # sue me. candidate's email addresses don't look like user@[2001:DB8::1]
        if not any(map(email.endswith, ['.com', '.org', '.net', '.name'])):
            raise DropItem("not an email")

        if email in self.emails_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.emails_seen.add(email)
            return item

    def process_twitter(self, item, spider):
        handle = urlparse(item['twitter']).path.strip("/")
        key = handle.lower()

        if key in ["wix"]:
            raise DropItem("not candidate twitter")

        if key in self.twitter_handles_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.twitter_handles_seen.add(key)

            item['twitter'] = handle
            return item


class ExportPipeline:
    """
    Log items to different files by item and scraper domain.

    When running via CrawlerProcess with multiple scrapers, sharing a output
    files is not safe, so I log to different files by type (to make the csv
    headers meaningful, and by domain, to prevent multiprocessing issues.
    """

    def open_spider(self, spider):
        class Exporters(defaultdict):
            def __missing__(self, key):
                path = "{}-{}.csv".format(key, spider.domain)
                return CsvItemExporter(open(path, 'wb'))

        self.exporters = Exporters()

    def close_spider(self, spider):
        for exporter in self.exporters.values():
            exporter.finish_exporting()

    def process_item(self, item, spider):
        if isinstance(item, items.Twitter):
            exporter = self.exporters['twitter']
        elif isinstance(item, items.EmailAddress):
            exporter = self.exporters['email']
        else:
            # add an exporter key to look up if you get an error here
            raise ValueError("not a registered item type")

        exporter.export_item(item)
        return item
