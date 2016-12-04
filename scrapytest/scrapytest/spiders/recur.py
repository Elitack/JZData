 #coding=utf-8

import sys
import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import csv

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "file://127.0.0.1/home/jack/Desktop/file2/Contents0.html"
    ]

    def parse(self, response):
        reload(sys)
        sys.setdefaultencoding( "utf-8" )
        indexCall = 0
        indexMes = 0
        callLog = response.selector.xpath("//a")
        for li in callLog:
            if li.xpath("./text()").extract()[0] != u' \u901a\u8bdd\u8bb0\u5f55':
                indexCall = indexCall + 1
                continue
            break
        for li in callLog:
            if li.xpath("./text()").extract()[0] != u' \u5f69\u4fe1':
                indexMes = indexMes + 1
                continue
            break
        endNum = callLog[indexCall].extract().find('.')
        start = int(callLog[indexCall].extract()[17:endNum])
        endNum = callLog[indexMes].extract().find('.')
        end = int(callLog[indexMes].extract()[17:endNum])
        for i in range(start, end+1):
            yield scrapy.Request("file://127.0.0.1/home/jack/Desktop/file2/Contents" + str(i) + ".html", callback = self.parseCallLog)



    def parseCallLog(self, response):

        index = 4
        tablelist = response.selector.xpath("//table[@class='OuterTable'][@border='1px']")
        for li in tablelist:
            lixpath = li.xpath(".//tr[@class='tablehead']/td[2]/text()").extract()[0]
            if lixpath != u'\u59d3\u540d':#中文:姓名
                continue
            tdlist = li.xpath(".//td/text()").extract()
            while index < len(tdlist):
                f = file("real.csv", "a+")
                f.write(tdlist[index] + ',' + tdlist[index+1] + ',' + tdlist[index+2] + ',')
                f.write(tdlist[index+4] + ',' + tdlist[index+6] + ',' + tdlist[index+8] + ',')
                f.write(tdlist[index+10] + ',' + tdlist[index+12] + '\n')
                f.close()
                index = index + 13
            index = 4
