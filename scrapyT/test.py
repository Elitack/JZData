 #coding=utf-8

import scrapy
from scrapy.crawler import CrawlerProcess
import sys
import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import csv

class MySpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "file://127.0.0.1/home/jack/Desktop/file1/Contents0.html"
    ]

    def parse(self, response):
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
            yield scrapy.Request("file://127.0.0.1:8000/home/jack/Desktop/file1/Contents" + str(i) + ".html", callback = self.parseCallLog)



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

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})


reload(sys)
sys.setdefaultencoding( "utf-8" )

print "abcde\n\n\n\n\n\n\n\n\n\n\n\n\n"
process.crawl(MySpider)
process.start() # the script will block here until the crawling is finished
