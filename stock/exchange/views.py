##### 주식 데이터, 그래프 관련 #####
import io
import urllib, base64
import FinanceDataReader as fdr
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
from mplfinance.original_flavor import candlestick2_ochl
########################################################
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    
    # stock_name 이 str인데 정렬이 성립하는가? -stock_name을 symbol순으로 바꿀 것
    stock_list = Stock_list.objects.order_by('stock_name')


    context = {'stock_list': stock_list}
    return render(request, 'exchange/stocklist.html', context)
    # return HttpResponse("exchange")
# 그래프 보여주는 부분 (수정 예정)
# home.html(가칭)에 img src 에도 추가해줘야함


def detail(request, symbol):
    "작업중"
    stock_list = Question.objects.get(id=symbol)
    context = {'stock_list': stock_list}
    return render(request, 'exchange/stock_list_detail.html', context)


def home(request):
    plt.plot(range(10))
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return render(request, 'home.html', {'data':uri})
