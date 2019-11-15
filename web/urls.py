from django.urls import path

from . import views

app_name = 'web'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('publisher/<str:origin>', views.Index.as_view(), name='news_by_origin'),
]
