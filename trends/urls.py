from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('scrapper/', views.scrap_test, name='scrapper')
]
