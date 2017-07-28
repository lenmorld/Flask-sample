import scrapy
from scrapy.shell import inspect_response

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # get page number
        print(response.url)   # "http://quotes.toscrape.com/page/1/"

        # inspect response at this point
        # inspect_response(response, self)

        page = response.url.split("/")[-2]   # ['http:', '', 'quotes.toscrape.com', 'page', '1', '']
        print(page)
        filename = 'quotes-%s.html' % page

        with open(filename, 'wb') as f:
            # f.write(response.body)
            quotes = response.xpath('//div[@class="quote"]/span[@class="text"]//text()').extract()
            for quote in quotes:
                # use encode() to convert to bytes
                f.write((quote + '\n').encode())
        self.log('Saved file %s' % filename)