from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests


def index(request):
    keyword = request.GET.get('keyword')
    print(keyword)
    context = {'keyword': keyword, }
    return render(request, 'base.html', context)
