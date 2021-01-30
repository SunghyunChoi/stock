from django.urls import path

from . import views

app_name = 'exchange'

urlpatterns = [
    path('', views.index, name='index'),
    # path('<int:symbol>/', views.stock_list_page, name='stock_list'),
    # path('stock_list/', views.stock_list_page, name='stock_list'),
    path('buy/', views.buy, name='buy'),
    path('sell/', views.sell, name='sell')
    #path('article/create/', views.article_create, name='article_create'),
    #path('comment/create/<int:article_id>/', views.comment_create, name='comment_create'),
]

