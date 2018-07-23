SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'
DOWNLOADER_MIDDLEWARES = {
    'scrapy.spidermiddlewares.offsite.OffsiteMiddleware': None,
}

ITEM_PIPELINES = {
    'scraper.pipelines.DeuplicatesPipeline': 100,
    'scraper.pipelines.ExportPipeline': 900,
}
