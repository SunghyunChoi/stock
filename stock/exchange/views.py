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
from django.conf import settings
from .models import Stock_list, User_result, Transaction_history
from common.models import MyUser
from django.utils import timezone
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    
    # stock_name 이 str인데 정렬이 성립하는가? -stock_name을 symbol순으로 바꿀 것
    stock_list = Stock_list.objects.order_by('symbol')

    # 입력 파라미터
    page = request.GET.get('page', '1')  # 페이지

    # 페이징처리
    paginator = Paginator(stock_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'stock_list': page_obj}


    context = {'stock_list': stock_list}
    return render(request, 'exchange/stock_list.html', context)


# return HttpResponse("exchange")
# 그래프 보여주는 부분 (수정 예정)
# home.html(가칭)에 img src 에도 추가해줘야함

def stock_list_page(request):
    stock_list = Stock_list.objects.all()
    context = {'stock_list': stock_list}
    return render(request, 'exchange/stock_list.html', context)



def find_stock(request):
    if request.user.is_authenticated:
        userID = request.user.id
    stock_requested = str(request.GET.get('stock_name', None))
    stock_list = stock_requested.objects.get(id=stock_name)
    context = {'stock_list': stock_list}
    return render(request, 'exchange/stock_list_page.html', context)


def home(request):
    plt.plot(range(10))
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return render(request, 'home.html', {'data':uri})


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