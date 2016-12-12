 #coding=utf-8

import sys
import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import csv

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "http://127.0.0.1:8000/Contents0.html"
    ]

    def parse(self, response):
        reload(sys)
        sys.setdefaultencoding( "utf-8" )
        indexCall = 0
        indexMes = 0
        adressList = response.selector.xpath("//td")
        for li in adressList:
            tmp = li.xpath("./span/img").extract()
            if (not(tmp) or tmp[0].find("Contact.ico") == -1):
                indexCall = indexCall + 1
                continue
            break
        indexMes = indexCall
        for li in adressList[indexCall:len(adressList):3]:
            tmp = li.xpath("./span/img").extract()
            if (tmp and tmp[0].find("Contact.ico") != -1):
                indexMes = indexMes + 3
                continue
            break
        indexMes = indexMes - 3
        startA = adressList[indexCall].xpath("./span/a").extract()
        endA = adressList[indexMes].xpath("./span/a").extract()
        endNum = startA[0].find('.')
        start = int(startA[0][17:endNum])
        endNum = endA[0].find('.')
        end = int(endA[0][17:endNum])
        for i in range(start, end+1):
            yield scrapy.Request("http://127.0.0.1:8000/Contents" + str(i) + ".html", callback = self.parseCallLog)

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
            if lixpath != u'\u59d3\u540d':#中文:姓名
                continue
            tdlist = li.xpath(".//td/text()").extract()
            
            while index < len(tdlist):
                f = file("real.csv", "a+")
                f.write(tdlist[index] + ',' + tdlist[index+1] + ',' + tdlist[index+2] + ',')
                f.write(tdlist[index+3] + ',' + tdlist[index+4] + ',' + tdlist[index+5] + '\n')
                
                f.close()
                index = index + 6
            index = 6
