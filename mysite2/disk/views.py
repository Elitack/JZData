
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
from disk.models import User

import scrapy
from scrapy.crawler import CrawlerProcess
import sys
import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import csv
import os
from scrapy.utils.project import get_project_settings
import codecs
import re, htmlentitydefs
from recur import MySpider
# Create your views here.

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

            process = CrawlerProcess({
                'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
            })

            process.crawl(MySpider)
            process.start() # the script will block here until the crawling is finished

    else:
        uf = UserForm()
    return render(request, 'disk/register.html',{'uf':uf})
