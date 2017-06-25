import scrapy
import re
from .. import items

from scrapy.shell import inspect_response

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from pprint import pprint

from scrapy.selector import HtmlXPathSelector

from lxml import etree as ET
parser = ET.XMLParser(recover=True)



class ApartmentCrawler(CrawlSpider):
    apartments = []
    name = 'apartments'
    allowed_domains = ['kijiji.ca']
    start_urls = ['http://www.kijiji.ca/b-immobilier/grand-montreal/c34l80002?siteLocale=en_CA']

    # http://www.kijiji.ca/b-immobilier/grand-montreal/page-4/c34l80002

    links_allowed = "http://www.kijiji.ca/b-immobilier/grand-montreal/.+"
    links_allowed_pages = "http://www.kijiji.ca/b-immobilier/grand-montreal/.*?/page-[0-5]/.+"

    # "b-immobilier/grand-montreal/c34l80002?siteLocale=en_CA"

    rules = [
        Rule(
            LinkExtractor(
                allow=[links_allowed]
             ), callback='parse_item'),
        Rule(
            LinkExtractor(
                allow=[links_allowed_pages]
            )
        )
    ]


    # def __init__(self, *a, **kw):
    #     """Attach a callback to the spider_closed signal"""
    #     super(ApartmentCrawler, self).__init__(*a, **kw)
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    #     if USE_DB is True:
    #         self.open_database()
    #         if DRAW_ALL_DB is True and DRAW_NEW_AD_ONLY is False:
    #             # add already know marker
    #             for x in self.m_list:
    #                 self.add_marker(x, False)
    #
    #
    # def spider_closed(self, spider):
    #     """Handle the spider_closed event to save the map"""
    #
    #     # create the special marker for all the ads without geocode
    #     # print "found %d items without geocode" % (len(self.no_geocode))
    #     # if len(self.no_geocode) > 0:
    #     #     html = ""
    #     #     for x in self.no_geocode:
    #     #         html += "<a href=%s target=_blank>%s</a> : %s<br>" % (x["url"], x["title"], x["price"])
    #     #     iframe  = folium.element.IFrame(html=html, width=500, height=100)
    #     #     popup   = folium.Popup(iframe, max_width=500)
    #     #     folium.Marker(MAP_LATLNG,
    #     #                   popup=popup,
    #     #                   icon=folium.Icon()).add_to(self.m_map)
    #     #
    #     #
    #     #
    #     # print "found %d new items" % (self.new_items)
    #     # pickle.dump(self.m_list, open(DATABASE, 'wb'))
    #     # self.m_map.save('map.html')
    #     page = 1
    #     filename = 'apartments-%s.html' % page
    #     page += 1
    #     with open(filename, 'wb') as f:
    #         # f.write(response.body)
    #         quotes = response.xpath('//div[@class="quote"]/span[@class="text"]//text()').extract()
    #         for quote in quotes:
    #             # use encode() to convert to bytess
    #             f.write((quote + '\n').encode())
    #     self.log('Saved file %s' % filename)




    def parse_item(self, response):
        # inspect response at this point
        # inspect_response(response, self)

        # self.logger.info(">>> Item page")
        # item = scrapy.Item()
        # quotes = response.xpath('//div[@class="quote"]/span[@class="text"]//text()').extract()

        # apartment = items.ApartmentsItem()
        # # apartment["url"] = response.url
        # apartment["url"] = response.xpath('//div[@data-vip-url]/@data-vip-url').extract()
        # apartment["image"] = response.xpath("//div[@data-vip-url]/div[@class='clearfix']/div/div[@class='image']/img/@src").extract()
        # apartment["price"] = response.xpath("//div[@data-vip-url]/div[@class='clearfix']/div[@class='info']/div[@class='info-container']/div[@class='price']//text()").extract()
        # apartment["title"] = response.xpath("//div[@data-vip-url]/div[@class='clearfix']/div[@class='info']/div[@class='info-container']/div[@class='title']/a//text()").extract()
        # apartment["location"] = response.xpath("//div[@data-vip-url]/div[@class='clearfix']/div[@class='info']/div[@class='info-container']/div[@class='location']//text()").extract()
        # apartment["date_posted"] = response.xpath("//div[@data-vip-url]/div[@class='clearfix']/div[@class='info']/div[@class='info-container']/div[@class='location']/span[@class='date-posted']//text()").extract()
        # apartment["desc"] = response.xpath("//div[@data-vip-url]/div[@class='clearfix']/div[@class='info']/div[@class='info-container']/div[@class='description']//text()").extract()

        # tree = ET.fromstring(response.body, parser)
        # for apt in tree.xpath('//div[@data-vip-url]'):
        #     print(apt)
        #     print("image")
        #     print(apt.xpath('//img/@src').extract())
        #     input("Pause 1")
        #     # self.apartments.append(apt)

        # self.apartments.append()

        # response.xpath('//div[@data-vip-url]/@data-vip-url').extract()


        # print("apartment: ")
        # pprint(apartment)

        hxs = HtmlXPathSelector(response)
        # apts_node = hxs.xpath('//div[@data-ad-id]')
        apts_ids = hxs.xpath('//div[@data-ad-id]/@data-ad-id').extract()

        # get unique attrib from this xpath to use for inside loop
        # print(apts_node)

        # might be slower but we are finally getting each apartment using its id
        print(apts_ids)
        for apt in apts_ids:
            # print(hxs.xpath("//div[@class='title']/a//text()").extract())

            # DOESNT WORK, still gets everything
            # apt_node = hxs.xpath("//div[@data-ad-id='" + apt + "']")
            # print(apt_node.xpath("//div[@class='title']/a//text()"))
            apartment = items.ApartmentsItem()

            apartment["url"] = hxs.xpath("//div[@data-ad-id='" + apt + "']/@data-vip-url").extract()
            apartment["title"] = hxs.xpath("//div[@data-ad-id='" + apt + "']//div[@class='title']/a//text()").extract()

            print(apartment)


            # if this is slow, try this
            # "//div[@data-ad-id='" + apt + "'][descendant::]div[@class='title']/a//text()"

            input("PAUSE")

        # return apartment

    def _extract_address(self, response):
        pass
