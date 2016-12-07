 #coding=utf-8

import sys
import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import csv

class QuotesSpider(scrapy.Spider):
    name = "message"
    start_urls = [
        "file://127.0.0.1/home/jack/Desktop/file1/Contents0.html"
    ]

    def parse(self, response):
        reload(sys)
        sys.setdefaultencoding( "utf-8" )
        indexCall = 0
        indexMes = 0
        callLog = response.selector.xpath("//td")
        for li in callLog:
            tmp = li.xpath("./span/img").extract()
            if (not(tmp) or tmp[0].find("SMS.ico") == -1):
                indexCall = indexCall + 1
                continue
            break
        indexMes = indexCall
        for li in callLog[indexCall:len(callLog):3]:
            tmp = li.xpath("./span/img").extract()
            if (tmp and tmp[0].find("SMS.ico") != -1):
                indexMes = indexMes + 3
                continue
            break
        indexMes = indexMes - 3
        startA = callLog[indexCall].xpath("./span/a").extract()
        endA = callLog[indexMes].xpath("./span/a").extract()
        endNum = startA[0].find('.')
        start = int(startA[0][17:endNum])
        endNum = endA[0].find('.')
        end = int(endA[0][17:endNum])
        for i in range(start, end+1):
            yield scrapy.Request("file://127.0.0.1/home/jack/Desktop/file1/Contents" + str(i) + ".html", callback = self.parseCallLog)

    def isMD5(self, tdlist):
        length = len(tdlist)
        length = length - 4
        if length % 13:
            return 1
        else:
            return 0

    def parseCallLog(self, response):

        index = 6
        tablelist = response.selector.xpath("//table[@class='OuterTable'][@border='1px']")
        for li in tablelist:
            lixpath = li.xpath(".//tr[@class='tablehead']/td[2]/text()").extract()[0]
            if lixpath != u'\u7535\u8bdd\u4fe1\u606f':#中文:电话信息
                continue
            tdlist = li.xpath(".//td/text()").extract()
            col2 = li.xpath("./tr/td/table").extract()[0]
            rangeCol2 = len(Selector(text=col2).xpath(".//td").extract())-1
            while index < len(tdlist):
                f = file("real.csv", "a+")
                writeIndex = [0] + range(1, rangeCol2 + 5)
                for i in writeIndex:
                    f.write(str(tdlist[index+i]) + ',')
                f.write('\n')
                f.close()
                index = index + rangeCol2 + 5
            index = 6
