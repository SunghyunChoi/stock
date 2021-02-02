from django.urls import path

from . import views

app_name = 'exchange'

urlpatterns = [
    path('', views.index, name='index'),
    path('/<str:symbol>/', views.stock_list_page, name='stock_list_page'),
    #path('/', views.stock_list_page, name='stock_list'),
    path('buy/', views.buy, name='buy'),
    path('sell/', views.sell, name='sell'),
    path('mypage/', views.mypage, name='mypage')
    #path('article/create/', views.article_create, name='article_create'),
    #path('comment/create/<int:article_id>/', views.comment_create, name='comment_create'),
]

