 #coding=utf-8

import sys
import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import csv

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "file://127.0.0.1/home/jack/Desktop/file1/Contents0.html"
    ]

    def parse(self, response):
        reload(sys)
        sys.setdefaultencoding( "utf-8" )
#CallLog
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
            yield scrapy.Request("file://127.0.0.1/home/jack/Desktop/file1/Contents" + str(i) + ".html", callback = self.parseCallLog)

#Adressbook
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
            yield scrapy.Request("file://127.0.0.1/home/jack/Desktop/file1/Contents" + str(i) + ".html", callback = self.parseAdressBook)


#Message
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
            yield scrapy.Request("file://127.0.0.1/home/jack/Desktop/file1/Contents" + str(i) + ".html", callback = self.parseMessage)



    def isMD5(self, tdlist):
        length = len(tdlist)
        length = length - 4
        if length % 13:
            return 1
        else:
            return 0

    def parseCallLog(self, response):

        index = 4
        tablelist = response.selector.xpath("//table[@class='OuterTable'][@border='1px']")
        for li in tablelist:
            lixpath = li.xpath(".//tr[@class='tablehead']/td[2]/text()").extract()[0]
            if lixpath != u'\u59d3\u540d':#中文:姓名
                continue
            tdlist = li.xpath(".//td/text()").extract()
            flagMD5 = self.isMD5(tdlist)
            while index < len(tdlist):
                f = file("real.csv", "a+")
                f.write(tdlist[index] + ',' + tdlist[index+1] + ',' + tdlist[index+2] + ',')
                f.write(tdlist[index+4] + ',' + tdlist[index+6] + ',' + tdlist[index+8] + ',')
                f.write(tdlist[index+10] + ',' + tdlist[index+12])
                if flagMD5:
                    f.write(',' + tdlist[index+14] + '\n')
                else:
                    f.write(',' + ' ' +'\n')
                f.close()
                index = index + 13 + 2*flagMD5
            index = 4

    def parseMessage(self, response):

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
                    tmp = tdlist[index+i].replace('\n', '')
                    f.write(tmp + ',')
                f.write('\n')
                f.close()
                index = index + rangeCol2 + 5
            index = 6


    def parseAdressBook(self, response):

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
