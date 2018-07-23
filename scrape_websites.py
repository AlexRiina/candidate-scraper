"""
Script to trigger scrapers on all websites in websites.csv

Structured this as a CrawlerProcess instead of a single scraper with multiple
start_urls to avoid, having to passing the start_url into the item pipeline
to correlate the items with their original urls.

If I wrap this in a shell script to run over the websites.csv it doesn't take
advantage of parallel scraping and throttling as well I think.
"""

from scrapy.crawler import CrawlerProcess
from scraper.spiders.candidate_scraper import Candidate
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
with open('websites.csv') as fp:
    for website in fp.readlines():
        process.crawl(Candidate, website.strip())

process.start()
