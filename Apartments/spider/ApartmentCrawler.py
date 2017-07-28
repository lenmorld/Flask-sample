import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class ApartmentCrawler(CrawlSpider):
    name = 'quotes.toscrape.com'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/page/1/']

    links_allowed = "http://quotes.toscrape.com/page.*"

    rules = [
        Rule(LinkExtractor(allow=(links_allowed), deny=("subsection\.php")))
    ]


    def parse_item(self, response):
        self.logger.info(">>> Item page")
        item = scrapy.Item()
        quotes = response.xpath('//div[@class="quote"]/span[@class="text"]//text()').extract()
        # item['tag'] = response.xpath('//div[@class="quote"]/span[@class="text"]//text()').extract()

        return item