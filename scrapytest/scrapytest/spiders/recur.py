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
        callLog = response.selector.xpath("//td")
        for li in callLog:
            tmp = li.xpath("./span/img").extract()
            if (not(tmp) or tmp[0].find("CallRecords.ico") == -1):
                indexCall = indexCall + 1
                continue
            break
        indexMes = indexCall
        for li in callLog[indexCall:len(callLog):3]:
            tmp = li.xpath("./span/img").extract()
            if (tmp and tmp[0].find("CallRecords.ico") != -1):
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
                print "%d \n" %len(tdlist)
                print "%d \n" %index
                f.write(tdlist[index] + ',' + tdlist[index+1] + ',' + tdlist[index+2] + ',')
                f.write(tdlist[index+4] + ',' + tdlist[index+6] + ',' + tdlist[index+8] + ',')
                f.write(tdlist[index+10] + ',' + tdlist[index+12] + '\n')
                f.close()
                index = index + 13
            index = 4
