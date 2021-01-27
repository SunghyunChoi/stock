from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

class Stock_list(models.Model):
    market_name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=50)
    stock_name = models.CharField(max_length=100)
    cur_price = models.IntegerField()

class Stock_search_page(models.Model):
    stock_ID = models.ForeignKey(Stock_list, on_delete=models.CASCADE)
    # 추후 필요 시, 용기 업데이트 예정



class Transaction_history(models.Model):
    user_ID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stock_ID = models.ForeignKey(Stock_list, on_delete=models.CASCADE)
    Qty = models.IntegerField()
    cur_price = models.IntegerField()
    date = models.DateTimeField(timezone.now())
    purchase = models.BooleanField()

class User_result(models.Model):
    user_ID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stock_ID = models.ForeignKey(Stock_list, on_delete=models.CASCADE)
    total_Qty = models.IntegerField()
    avg_purchase_price = models.IntegerField()
