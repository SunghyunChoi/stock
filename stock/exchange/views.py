##### 주식 데이터, 그래프 관련 #####
import io
import urllib, base64
import FinanceDataReader as fdr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
import matplotlib.font_manager as fm
from mplfinance.original_flavor import candlestick2_ohlc
########################################################
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from .models import Stock_list, User_result, Transaction_history
from common.models import MyUser
from django.utils import timezone
from django.core.paginator import Paginator # 페이징 관련 (글 목록)
from django.db.models import Q # 검색 관련
from datetime import datetime, timedelta


# Create your views here.
def index(request):
    
#  ---------------------------------- 검색  ---------------------------------- #
    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어

    # 조회
    stock_list = Stock_list.objects.order_by('stock_name')
    if kw:
        stock_list = stock_list.filter(
            # contains : 대소문자 구분 / icontain : 대소문자 구분x
            Q(symbol__icontains=kw) |  # 종목 번호
            Q(stock_name__icontains=kw)  # 종목 이름 
        ).distinct()
# ---------------------------------------------------------------------------- #

# ----------------------------------- [페이징] --------------------------- #
    # 페이징처리
    paginator = Paginator(stock_list, 20)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'stock_list': page_obj, 'page': page, 'kw': kw}  # page와 kw가 추가되었다.
    print('kw:', kw)

    # context = {'stock_list': stock_list}
    return render(request, 'exchange/stock_list.html', context)
# ----------------------------------- [페이징] --------------------------- #


# 예은 : 그래프 만드는 부분 추가했습니다 (21.02.01)
# 예은 할일 : cur_price를 현재가로 불러오도록 (근데 이렇게하면 실시간 업데이트 or 호가창 필요), 전일대비 몇퍼 증감인지 보여주기
def stock_list_page(request, symbol):
    today = datetime.today()
    yesterday = datetime.today() - timedelta(days=1)
    stock = Stock_list.objects.get(symbol=symbol)

    df_specific = fdr.DataReader(symbol, today.strftime('%Y-%m-%d'))
    stock.cur_price = int(df_specific['Close'][0]) # 맨위 날짜 읽는거니까 오늘 정가 empty여도 가장 최근값 불러옴

    # 전일 데이터 불러오기 (주말, 연휴인 경우 data없으므로 data있을때까지 거슬러올라가기)
    yesterday_stock = fdr.DataReader(symbol, yesterday.strftime('%Y-%m-%d'))
    date = 1
    while (1):
        yesterday_stock = fdr.DataReader(symbol, yesterday.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'))
        if (len(yesterday_stock) > 1):
            yesterday_price = int(yesterday_stock['Close'][0])
            break
        else:
            date += 1
            yesterday = datetime.today() - timedelta(days=date)
    yesterday_price = int(yesterday_stock['Close'][0])

    difference = stock.cur_price - yesterday_price
    difference_percent = round((difference / yesterday_price) * 100, 2)
    # 색깔을 위한 Flag
    if difference > 0:
        flag = 1
    elif difference < 0:
        flag = -1
    else:
        flag = 0

    graph_uri = graph(request, symbol)

    context = {'stock': stock, 'data': graph_uri, 'yesterday':yesterday_price, 'difference':difference, 'diff_per':difference_percent, 'flag':flag}
    return render(request, 'exchange/stock_page.html', context)



def find_stock(request):
    if request.user.is_authenticated:
        userID = request.user.id
    stock_requested = str(request.GET.get('stock_name', None))
    stock_list = stock_requested.objects.get(id=stock_name)
    context = {'stock_list': stock_list}
    return render(request, 'exchange/stock_list_page.html', context)


def graph(request, symbol):
    stock = Stock_list.objects.get(symbol=symbol)
    title_font_name = 'sans-serif'
    tick_label_font_name = 'sans-serif'

    # 봉차트 그리기
    now = datetime.now()
    half_year = (now - timedelta(days=180)).strftime('%Y-%m-%d')
    df_specific = fdr.DataReader(symbol, half_year)

    df_specific['MA5'] = df_specific['Close'].rolling(5).mean()
    df_specific['MA10'] = df_specific['Close'].rolling(10).mean()
    df_specific['MA20'] = df_specific['Close'].rolling(20).mean()
    df_specific[['Close','MA5','MA10','MA20']].plot()

    fig = plt.figure(figsize=(20,10))
    ax = fig.add_subplot(111)
    index = df_specific.index.astype('str') # 캔들스틱 x축이 str로 들어감

    # 이동평균선 그리기
    ax.plot(index, df_specific['MA5'], label='5days MA', linewidth=0.7)
    ax.plot(index, df_specific['MA10'], label='10days MA', linewidth=0.7)
    ax.plot(index, df_specific['MA20'], label='20days MA', linewidth=0.7)

    # X축 티커 숫자 20개로 제한
    ax.xaxis.set_major_locator(ticker.MaxNLocator(20))

    # 그래프 title과 축 이름 지정
    # ax.set_title(stock_name, fontsize=22)
    ax.set_xlabel('Date')

    # 캔들차트 그리기
    candlestick2_ohlc(ax, df_specific['Open'], df_specific['High'],
                      df_specific['Low'], df_specific['Close'],
                      width=0.5, colorup='r', colordown='b')
    ax.legend()
    plt.grid()

    plt.plot()
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri


# get username, stockID, quantity from get request 
# find cur_price from Stock_list
# find cash from MyUser
# return : cash, cur_price

def request_stockinfo(userID, stockID):
    cur_price = int(Stock_list.objects.get(symbol=stockID).cur_price)
    cur_cash = int(MyUser.objects.get(id=userID).cash)
    return (cur_price, cur_cash)

# returns whether buy is possible
def judge_buy(cash, cur_price, quantity):
    
    if cash < cur_price * quantity:
        return False
    else:
        return True

# returns whether sell is possible
def judge_sell(userID, stockID, quantity):
    #Check if user has enough stocks to sell
    try:
        user_result = User_result.objects.get(user_ID=userID, stock_ID=stockID)
        if user_result.total_Qty < quantity:
            return False
        else:
            return True
    except:
        return False


###################################################
# function buy() : Buy Stocks                     #
# url : /buy?stockID=XXXXXX&quantity=YYYYYY       #
# stockID = XXXXXX                                #
# quantity = YYYYYY                               #
# 1. Check if user has enough stock : judge_buy() #
# 2. Save Transaction_history                     #
# 3. update user.cash, user_result.total_Qty      #
#    (function : transaction_save())              #
###################################################
def buy(request):
    if request.user.is_authenticated:
        userID = request.user.id
    stockID = str(request.GET.get('stockID', None))
    quantity = int(request.GET.get('quantity', None))
    ##Add Check if quantity is 0

    ########################
    user = MyUser.objects.get(id=userID)
    stock = Stock_list.objects.get(symbol=stockID)
    cur_price = int(stock.cur_price)
    cur_cash = int(user.cash)

    buy_available = judge_buy(cur_cash, cur_price, quantity)
    if buy_available:
        #save transaction history
        new_transaction = Transaction_history(Qty=quantity, cur_price=cur_price, date=str(timezone.now()), purchase=1, stock_ID=stock, user_ID=user)
        new_transaction.save()
        #Update user_result
        transaction_save(user, stock, quantity, 1)
        updated_cash = user.cash
        #Buy Success
        return HttpResponse("Buy Success : userID %s, quantity %s, Old cash %s, Current cash %s, cur_price : %s" % (userID, quantity, cur_cash, updated_cash, cur_price))
    else:
        #Buy Failed
        return HttpResponse("Buy Failed : userID %s, quantity %s, Current cash %s, cur_price : %s, need more : %s" % (userID, quantity, cur_cash, cur_price, cur_price*quantity-cur_cash))


###################################################
# function sell() : sell Stocks                   #
# url : /sell?stockID=XXXXXX&quantity=YYYYYY      #
# stockID = XXXXXX                                #
# quantity = YYYYYY                               #
# 1. Check if user has enough stock : judge_sell()#
# 2. Save Transaction_history                     #
# 3. update user.cash, user_result.total_Qty      #
#    (function : transaction_save())              #
###################################################
def sell(request):
    if request.user.is_authenticated:
        userID = request.user.id
    stockID = str(request.GET.get('stockID', None))
    quantity = int(request.GET.get('quantity', None))
    ##Add Check if quantity is 0

    ########################
    user = MyUser.objects.get(id=userID)
    stock = Stock_list.objects.get(symbol=stockID)
    cur_price = int(stock.cur_price)
    cur_cash = int(user.cash)
    sell_available = judge_sell(user.id, stock.id, quantity)
    user_result = User_result.objects.get(user_ID=userID, stock_ID=stock.id)

    if sell_available:
        #save transaction history
        new_transaction = Transaction_history(Qty=quantity, cur_price=cur_price, date=str(timezone.now()), purchase=0, stock_ID=stock, user_ID=user)
        new_transaction.save()
        #Update user_result
        transaction_save(user, stock, quantity, 0)
        updated_cash = user.cash
        # Sell Success
        return HttpResponse("Sell Success : userID %s, sell quantity %s,remain quantity %s, Old cash %s, Current cash %s, cur_price : %s" % (userID, quantity, user_result.total_Qty, cur_cash, updated_cash, cur_price))
    else:
        # Sell failed
        return HttpResponse("Sell Failed : userID %s, quantity %s" % (userID, quantity))




#########################################################
# function transaction_save() : update user_result      #
# type : buy = 1, sell = 0                              #
# 1. Buy                                                #
#   1) Check if user has user_result with same stock.id #
#   2) Update user_result                               #
# 2. update user.cash, user_result.total_Qty            #
#########################################################

#!!!!!!!!!!!!!!!!!!!NEEDS Update stock_id : id is being referenced rather than stock_id : symbol
def transaction_save(user, stock, quantity, type): # type : buy = 1, sell = 0
        
    cur_price = stock.cur_price
    cur_cash = user.cash
    
    if type:#BUY
        try:
            user_result = User_result.objects.get(user_ID=user.id, stock_ID=stock.id)
            user_result.avg_purchase_price = (user_result.total_Qty * user_result.avg_purchase_price + quantity * cur_price) / (user_result.total_Qty + quantity)
            user_result.total_Qty += quantity
            user_result.save()
        except Exception as e:
            # No Match in User result : First Buy for (UserID, StockID)
            print(f"First buy for Stockid {stock.id}")
            print(e)
            #Update User result
            first_buy = User_result(total_Qty=quantity, avg_purchase_price=cur_price, stock_ID=stock, user_ID=user)
            first_buy.save()
            
            #Update user cash
        user.cash = user.cash - cur_price * quantity
        user.save()

    else:#SELL
        try:
            user_result = User_result.objects.get(user_ID=user.id, stock_ID=stock.id)
            user_result.total_Qty -= quantity
            user_result.save()
        except Exception as e:
            # Why Error?
            print(f"Error Occured whild selling stocks.")
            print(e)
            #Update User result
            
            #Update user cash
        user.cash = user.cash + cur_price * quantity
        user.save()

def mypage(request):
    if request.user.is_authenticated:
        userID = request.user.id
    user = MyUser.objects.get(id=userID)
    userResult = User_result.objects.filter(user_ID=user.id)
    context = {'user_result': userResult}

    return render(request, 'exchange/mypage.html', context)
