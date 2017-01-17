 #coding=utf-8
from bs4 import BeautifulSoup
import codecs
import sys
def crawlXML(docuName):
    reload(sys)
    sys.setdefaultencoding( "utf-8" )
    soup = BeautifulSoup(open('upload/test/'+ docuName + '/GAB_ZIP_INDEX.xml'), 'xml')
    mainContent = soup.MESSAGE.DATASET.DATA.DATASET
    colVal=""
    rowVal=""
    for childMainContent in mainContent:
        itemList = childMainContent.find_all("ITEM")
        for item in itemList:
            if item['rmk'] == u'列分隔符（缺少值时默认为制表符\\t）':
                colVal = item['val']
            elif item['rmk'] == u'行分隔符（缺少值时默认为换行符\\n）':
                rowVal = item['val']
            elif item['rmk'] == u'文件名':
                fileName = item['val']
        columList = childMainContent.find_all(chn = True)
        resultList = []
        for colum in columList:
            resultList.append(colum['chn'])


        print colVal, rowVal, fileName, resultList
        stripFile(fileName, rowVal, colVal, resultList, docuName)

def stripFile(oldFName,row,col,listed,docuName):
    row = transfer(row)
    col=transfer(col)
    f = open("disk/tool/output.txt", "r")
    route = f.readline().replace('\n', '')
    f.close()
    g = open("disk/tool/input.txt", "r")
    rout = g.readline().replace('\n', '')
    g.close()
    outputFileName = docuName
    na = rout + outputFileName + '/' + oldFName
    fp = open(na,"r+")
    newFp = file(route+'/' + outputFileName + '/' +oldFName[0:-4]+r'.csv',"a+")
    newFp.write(codecs.BOM_UTF8)
    for i in range(0, len(listed)-1):
        newFp.write(listed[i]+',')
    newFp.write(listed[-1]+'\n')

    for eachline in fp.readlines():
        newStr = eachline.replace(col,",").replace(row,"\n").strip()
        newFp.write(newStr+'\n')

    newFp.close()
    fp.close()

def transfer(a):
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
