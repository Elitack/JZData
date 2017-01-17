from threading import Thread
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
import time

import os

from tool.tool import crawlXML
from tool.ziptool import zip_dir, unzip_file


from wsgiref.util import FileWrapper
class UserForm(forms.Form):
    username = forms.CharField()
    headImg = forms.FileField()


def register(request):
    uf = UserForm()
    return render(request, 'disk/register.html',{'uf':uf})


def show(request):
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
            unzip_file("upload/" + fileName, "upload/test/" + fileName[0:-4])

#crawl and store
            route = "disk/static/data/"
            os.mkdir(route+fileName[0:-4])
            crawlXML(fileName[0:-4])

            zip_dir(route + fileName[0:-4], route + fileName)
            fileListTmp = os.listdir(route + fileName[0:-4])
            fileList = []

            for fi in fileListTmp:
                fileList.append(fi[0:-4])
            clearFile(fileName)
            return render(request, 'disk/show.html', {'fileName':fileName[0:-4], 'fileList':fileList})


    else:
        uf = UserForm()
    return render(request, 'disk/register.html',{'uf':uf})

def download(request, fileName):
    file_name = fileName+'.zip'
    path_to_file = "disk/static/data/" + file_name
    response = HttpResponse(FileWrapper(file(path_to_file,'rb')), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename='+file_name
    clearFile(file_name)
    return response


def clearFile(fileName):
    os.remove("upload/" + fileName)



#def download(request):
#    file_name = #get the filename of desired excel file
#    path_to_file = #get the path of desired excel file
#    response = HttpResponse(mimetype='application/force-download')
#    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
#    response['X-Sendfile'] = smart_str(path_to_file)
#    return response
