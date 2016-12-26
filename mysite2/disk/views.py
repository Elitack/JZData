
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
from disk.models import User
from django.utils.encoding import smart_str
import shutil
import os,sys
import zipfile
# Create your views here.

from scrapy.crawler import CrawlerProcess
import os

from tool.recur import MySpider
from tool.ziptool import zip_dir, unzip_file


from wsgiref.util import FileWrapper
class UserForm(forms.Form):
    username = forms.CharField()
    headImg = forms.FileField()


def register(request):
    if request.method == "POST":
        uf = UserForm(request.POST,request.FILES)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            headImg = uf.cleaned_data['headImg']
            user = User()
            user.username = username
            user.headImg = headImg
            user.save()
            fileName = request.FILES.get('headImg').name
            unzip_file("/home/jack/Documents/Project/JZData/mysite2/upload/" + fileName, "/home/jack/Documents/Project/JZData/mysite2/upload/test/" + fileName[0:-4])
            process = CrawlerProcess({
                'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
            })

            process.crawl(MySpider)
            process.start() # the script will block here until the crawling is finished
            zip_dir("/home/jack/Desktop/store/" + fileName[0:-4], "/home/jack/Desktop/store/" + fileName)

            file_name = fileName
            path_to_file = "/home/jack/Desktop/store/" + file_name
            response = HttpResponse(FileWrapper(file(path_to_file,'rb')), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename='+file_name
            clearFile(fileName)
            return response
    else:
        uf = UserForm()
    return render(request, 'disk/register.html',{'uf':uf})

def clearFile(fileName):
    shutil.rmtree("/home/jack/Documents/Project/JZData/mysite2/upload/test/" + fileName[0:-4])
    os.remove("/home/jack/Documents/Project/JZData/mysite2/upload/" + fileName)



#def download(request):
#    file_name = #get the filename of desired excel file
#    path_to_file = #get the path of desired excel file
#    response = HttpResponse(mimetype='application/force-download')
#    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
#    response['X-Sendfile'] = smart_str(path_to_file)
#    return response
