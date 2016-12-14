 #coding=utf-8

import scrapy
from scrapy.crawler import CrawlerProcess
import sys
import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import csv
import os
from scrapy.utils.project import get_project_settings

class MySpider(scrapy.Spider):
    name = "quotes"
    start_urls = ["http://127.0.0.1:80/file2/Contents0.html"]

    def start_requests(self):
        pages = []
        f = open("input.txt", "r")
        line = f.readline().replace('\n', '')
        print line
        print '\n'
        for filename in os.listdir(line):
            url = "http://127.0.0.1:80/" + filename + "/Contents0.html"
            page = scrapy.Request(url)
            pages.append(page)
        return pages

        
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
        if indexMes != indexCall-3:
            startA = callLog[indexCall].xpath("./span/a").extract()
            endA = callLog[indexMes].xpath("./span/a").extract()
            if startA[0][9] != '#':
                endNum = startA[0].find('.')
                start = int(startA[0][17:endNum])
            else:
                start = 0
            if endA[0][9] != '#':
                endNum = endA[0].find('.')
                end = int(endA[0][17:endNum])
            else:
                end = 0
        for i in range(start, end+1):
            theEndNum = response.url.find("Contents") + 8
            yield scrapy.Request(response.url[0:theEndNum] + str(i) + ".html", callback = self.parseCallLog, dont_filter=True)

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
        if indexMes != indexCall-3:
            startA = adressList[indexCall].xpath("./span/a").extract()
            endA = adressList[indexMes].xpath("./span/a").extract()
            if startA[0][9] != '#':
                endNum = startA[0].find('.')
                start = int(startA[0][17:endNum])
            else:
                start = 0
            if endA[0][9] != '#':
                endNum = endA[0].find('.')
                end = int(endA[0][17:endNum])
            else:
                end = 0
            for i in range(start, end+1):
                theEndNum = response.url.find("Contents") + 8
                yield scrapy.Request(response.url[0:theEndNum] + str(i) + ".html", callback = self.parseAdressBook, dont_filter=True)


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
        if indexMes != indexCall-3:
            startA = callLog[indexCall].xpath("./span/a").extract()
            endA = callLog[indexMes].xpath("./span/a").extract()
            if startA[0][9] != '#':
                endNum = startA[0].find('.')
                start = int(startA[0][17:endNum])
            else:
                start = 0
            if endA[0][9] != '#':
                endNum = endA[0].find('.')
                end = int(endA[0][17:endNum])
            else:
                end = 0
            for i in range(start, end+1):
                theEndNum = response.url.find("Contents") + 8
                yield scrapy.Request(response.url[0:theEndNum] + str(i) + ".html", callback = self.parseMessage, dont_filter=True)



    def isMD5(self, tdlist):
        length = len(tdlist)
        length = length - 4
        if length % 13:
            return 1
        else:
            return 0

    def getRoute(self):
        pages = []
        f = open("output.txt", "r")
        line = f.readline().replace('\n', '')
        return line


    def parseCallLog(self, response):
        route = self.getRoute()
        string = response.url[20:len(response.url)]
        end = string.find('Contents')
        outputFileName = response.url[20:20+end-1]
        index = 4
        tablelist = response.selector.xpath("//table[@class='OuterTable'][@border='1px']")
        for li in tablelist:
            lixpath = li.xpath(".//tr[@class='tablehead']/td[2]/text()").extract()[0]
            if lixpath != u'\u59d3\u540d':#中文:姓名
                continue
            tdlist = li.xpath(".//td/text()").extract()
            flagMD5 = self.isMD5(tdlist)
            while index < len(tdlist):
                f = file(route + outputFileName + '-' + "callLog.csv", "a+")
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
        route = self.getRoute()
        string = response.url[20:len(response.url)]
        end = string.find('Contents')
        outputFileName = response.url[20:20+end-1]

        tablelist = response.selector.xpath("//table[@class='OuterTable'][@border='1px']")
        for li in tablelist:
            lixTmp = li.xpath(".//tr[@class='tablehead']")
            lixpath = lixTmp.xpath("./td[2]/text()").extract()[0]
            if lixpath != u'\u7535\u8bdd\u4fe1\u606f':#中文:电话信息
                continue

            trlist = li.xpath("./tr")
            col2 = li.xpath("./tr/td/table").extract()[0]
            rangeCol2 = len(Selector(text=col2).xpath(".//td").extract())-1

            for trTmp in trlist[1:len(trlist)] :
                tdListText = trTmp.xpath(".//td/text()").extract()
                f = file(route + outputFileName + '-' + "Message.csv", "a+")
                f.write(tdListText[0] + ',')
                for i in range(1,rangeCol2):
                    tmp = tdListText[i].replace('\n', ' ').replace(',' , '，')
                    f.write(tmp + ' ')

                if len(tdListText) == (5 + rangeCol2):
                    for i in range(rangeCol2, 5+rangeCol2):
                        tmp = tdListText[i].replace('\n', ' ').replace(',' , '，')
                        f.write(tmp + ',')
                    f.write('\n')
                    f.close()

                elif len(tdListText) == (8+ rangeCol2):
                    indexListFate = [0,1,3,6,7,5]
                    indexListTrue = [i + rangeCol2 for i in indexListFate]
                    for i in indexListTrue:
                        tmp = tdListText[i].replace('\n', ' ').replace(',' , '，')
                        f.write(tmp + ',')
                    f.write('\n')
                    f.close()

                elif len(tdListText) == (7 + rangeCol2):
                    indexListFate = [0,1]
                    indexListTrue = [i + rangeCol2 for i in indexListFate]
                    for i in indexListTrue:
                        tmp = tdListText[i].replace('\n', ' ').replace(',' , '，')
                        f.write(tmp + ',')
                    tdList = trTmp.xpath(".//td")
                    tmp = (tdList[6+rangeCol2].xpath("./div/text()").extract()[0]).replace('\n',' ')
                    f.write(tmp + ',')
                    indexListFate = [5,6,4]
                    indexListTrue = [i + rangeCol2 for i in indexListFate]
                    for i in indexListTrue:
                        tmp = tdListText[i].replace('\n', ' ').replace(',' , '，')
                        f.write(tmp + ',')
                    f.write('\n')
                    f.close()


    def parseAdressBook(self, response):
        route = self.getRoute()
        string = response.url[20:len(response.url)]
        end = string.find('Contents')
        outputFileName = response.url[20:20+end-1]


        index = 6
        tablelist = response.selector.xpath("//table[@class='OuterTable'][@border='1px']")
        for li in tablelist:
            lixpath = li.xpath(".//tr[@class='tablehead']/td[2]/text()").extract()[0]
            if lixpath != u'\u59d3\u540d':#中文:姓名
                continue
            tdlist = li.xpath(".//td/text()").extract()

            while index < len(tdlist):
                f = file(route + outputFileName + '-' + "adressBook.csv", "a+")
                f.write(tdlist[index] + ',' + tdlist[index+1] + ',' + tdlist[index+2] + ',')
                f.write(tdlist[index+3] + ',' + tdlist[index+4] + ',' + tdlist[index+5] + '\n')

                f.close()
                index = index + 6
            index = 6
