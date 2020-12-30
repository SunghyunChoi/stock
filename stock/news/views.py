from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("안녕하세요 여기에 이제 기사가 써질 것.")