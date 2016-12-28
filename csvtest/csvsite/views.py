from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse
from django.utils.encoding import smart_str
from wsgiref.util import FileWrapper

def index(request):
    return render(request, 'index.html', {})
