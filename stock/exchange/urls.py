from django.urls import path

from . import views

app_name = 'exchange'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:symbol>/', views.detail, name='detail'),
    #path('article/create/', views.article_create, name='article_create'),
    #path('comment/create/<int:article_id>/', views.comment_create, name='comment_create'),
]