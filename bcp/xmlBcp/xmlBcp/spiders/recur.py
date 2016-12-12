 #coding=utf-8

import sys
import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import csv

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "http://127.0.0.1:8000/GAB_ZIP_INDEX.xml"
    ]

    def parse(self, response):
        reload(sys)
        sys.setdefaultencoding("utf-8")
        main = response.xpath("//DATASET/DATA/DATASET")[0]
        dataset = main.xpath('./DATA')
        for data in dataset:
            item = data.xpath('./ITEM')
            col = self.valFind(item[0].extract())
            col = self.transfer(col)
            row = self.valFind(item[1].extract())
            row = self.transfer(row)
            nameData = data.xpath('./DATASET')[0]
            name = self.valFind(nameData.xpath('./DATA/ITEM')[1].extract())
            listData = data.xpath('./DATASET')[1]
            listItem = listData.xpath('./DATA/ITEM').extract()
            colList = []
            for item in listItem:
                colList.append(self.nameFind(item))
            #print name, row, col ,colList
            self.stripFile(name, row, col ,colList)


    def valFind(self,itemTmp):
        indexF = itemTmp.find('val') + 5
        indexE = itemTmp[indexF:-1].find('"')+indexF
        return itemTmp[indexF:indexE]

    def nameFind(self,itemTmp):
        indexF = itemTmp.find('eng') + 5
        indexE = itemTmp[indexF:-1].find('"')+indexF
        return itemTmp[indexF:indexE]


    def stripFile(self,oldFName,row,col,listed):
        '''''remove the space or Tab or enter in a file,and output to a new file in the same folder'''
        fp = open(r"E:\大学\大三上\JZ大数据\137-705420347-350000-350000-1403534417-00001(数据较全的案例包)\\" + oldFName,"r+")
        newFp = file( oldFName[0:-4]+r'.csv',"a+")
        for i in range(0, len(listed)-1):
            newFp.write(listed[i]+',')
        newFp.write(listed[-1]+'\n')

        for eachline in fp.readlines():
            newStr = eachline.replace(col,",").replace(row,"\n").strip()
            #print "Write:",newStr
            newFp.write(newStr+'\n')
        fp.close()
        newFp.close()
    def transfer(self,a):
        b=''
        for i in a.split('\\'):
            if(len(i) == 0):
                continue
            if(i[0] == 't'):
                b += '\t'
                if(len(i)>1):
                    b += i[1:]
                continue
            if(i[0] =='n'):
                b += '\n'
                if(len(i)>1):
                    b += i[1:]
                continue
            if(i[0] == 'r'):
                b += '\r'
                if(len(i)>1):
                    b += i[1:]
                continue
            b += i
        return b
