import scrapy
import re

from twisted.spread.pb import respond

from .. import items

from scrapy.shell import inspect_response

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from pprint import pprint

from scrapy import Request

from scrapy.selector import HtmlXPathSelector

from lxml import etree as ET
parser = ET.XMLParser(recover=True)

from pprint import pprint


class ApartmentCrawler(CrawlSpider):
    apartments = {}
    name = 'apartments'
    allowed_domains = ['kijiji.ca']
    base_url = 'https://www.kijiji.ca'
    start_urls = ['https://www.kijiji.ca/b-immobilier/grand-montreal/c34l80002?siteLocale=en_CA']

    # http://www.kijiji.ca/b-immobilier/grand-montreal/page-4/c34l80002
    # http://www.kijiji.ca/b-immobilier/grand-montreal/page-2/c34l80002

    links_allowed = "https://www.kijiji.ca/b-immobilier/grand-montreal/.+"
    # links_allowed_pages = "http://www.kijiji.ca/b-immobilier/grand-montreal/.*?/page-[0-5]/.+"
    links_allowed_pages = "https://www.kijiji.ca/b-immobilier/grand-montreal/page-[0-9]/.+"

    # "b-immobilier/grand-montreal/c34l80002?siteLocale=en_CA"

    # follow links from them (since no callback means follow=True by default).

    rules = [
        Rule(
            LinkExtractor(
                allow=[links_allowed]
             ), callback='parse_item'),
        Rule(
            LinkExtractor(
                allow=[links_allowed_pages]
            ), callback='parse_item'),
        # Rule(
        #     LinkExtractor(
        #         allow=[]
        #     )
        # )
    ]

    def clean_data(self, string):
        for unneeded in ['\n', '\r']:
            string = string.replace(unneeded, "")
        return string.strip()       # remove leading and trailing spaces


    def parse_item(self, response):
        # inspect_response(response, self)              # inspect response at this point
        # print(response.url)

        self.logger.info(">>> Item page")

        hxs = HtmlXPathSelector(response)
        # apartments = []
        apt_div = hxs.xpath('//div[@data-ad-id]')
        for apt in apt_div:
            # print(apt.xpath('./@data-vip-url').extract())

            # used string() instead of //text()
            # extract_first() isntead on extract() because extract always returns a list with 1 element anyways

            apartment = items.ApartmentsItem()
            apartment["apt_id"] = apt.xpath('./@data-ad-id').extract_first()
            apartment["url"] = apt.xpath("./@data-vip-url").extract_first()

            # these 4 fields need to be cleaned
            apartment["price"] = self.clean_data(apt.xpath(".//div[@class='price']/text()").extract_first())
            apartment["title"] = self.clean_data(apt.xpath(".//div[@class='title']/a/text()").extract_first())
            apartment["location"] = self.clean_data(apt.xpath(".//div[@class='location']/text()").extract_first())
            apartment["desc"] = self.clean_data(apt.xpath(".//div[@class='description']/text()").extract_first())

            apartment["date_posted"] = apt.xpath(".//span[@class='date-posted']/text()").extract_first()
            apartment["image"] = apt.xpath(".//div[@class='image']/img/@src").extract_first()

            # print(apartment)
            # input("PAUSE")

            # add as an object with apt_id as primary key
            # a = {
            #       '2341': {'room': 2, 'address': '123 asdaaaaxzxzx apt 56'},
            #       '1232': {'room': 3, 'address': 'dasdas 123 12312'}
            #      }


            ########## run another Request here based on crawled URLs ####
            link = self.base_url + apartment["url"]
            # print(">>> going to link: ", link)
            new_request = Request(link, callback=self.parse_apartment_page)
            new_request.meta['item'] = apartment

            # self.apartments[apartment["apt_id"]] = yield new_request
            # same result as simple yield ???

            yield new_request

            ### TODO! how to get item address in async way
            # parse_apartment_page isnt called

            # apartment["address"] = item["address"]
            # OR save obtained info from spawned request

            ### TODO instead of relying on parse_apartment_page to return item
            # create class member apartments that it can manipulate directly using apt_id as primary key

            ### SOLUTION CHOSEN: pass entire apartment object to 2nd Request, item yielded now contains all attribs including
            # address to be parsed from the individual page

            ##############################################################

        # return self.apartments        # return not needed with yield


    def parse_apartment_page(self, response):
        hxs = HtmlXPathSelector(response)
        # print("parse specific apartment page")

        item = response.meta["item"]
        # apt_id = item["apt_id"]

        # address
        # //th[ . = 'Address']/following-sibling::td//text()
        address = hxs.xpath("//th[ . = 'Address']/following-sibling::td//text()").extract()
        if address is None:
            item["address"] = "None"
        else:
            item["address"] = address

        # self.apartments[apt_id]["address"] = address

        yield item
