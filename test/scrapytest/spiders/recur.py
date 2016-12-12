 #coding=utf-8

import sys
import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import csv

class QuotesSpider(scrapy.Spider):
    name = "message"
    start_urls = [
        "file://127.0.0.1/home/jack/Desktop/file1/Contents3.html"
    ]

    def parse(self, response):
        reload(sys)
        sys.setdefaultencoding( "utf-8" )
        index = 6
        tablelist = response.selector.xpath("//table[@class='OuterTable'][@border='1px']")
        for li in tablelist:
            tdlist = li.xpath(".//td/text()").extract()
            for i in range(20, 30):
                f = file("real.csv", "a+")
                tmp = tdlist[index+i].replace('\n', '')
                f.write(tmp + ',')
                f.close()
            index = 6
