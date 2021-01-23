from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Stock_list(models.Model):
    market_name = models.CharField(max_length=50)
    symbol = models.IntegerField(max_length=50)
    stock_name = models.CharField(max_length=100)
    cur_price = models.IntegerField(max_length=100)


class Stock_search_page(models.Model):
    stock_ID = models.ForeignKey(Stock_list, on_delete=models.CASCADE)
    # 추후 필요 시, 용기 업데이트 예정


class Transaction_history(models.Model):
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_ID = models.ForeignKey(Stock_list, on_delete=models.CASCADE)
    Qty = models.IntegerField(max_length=50)
    cur_price = models.ForeignKey(Stock_list, on_delete=models.CASCADE)
    date = models.DateTimeField(timezone.now())
    purchase = models.BooleanField()


class User_result(models.Model):
    user_ID = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_ID = models.ForeignKey(Stock_list, on_delete=models.CASCADE)
    total_Qty = models.IntegerField(max_length=100)
    avg_purchase_price = models.IntegerField(max_length=100)

