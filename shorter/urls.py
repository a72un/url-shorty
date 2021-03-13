from django.urls import path
from shorter import views

urlpatterns = [
    path('', views.home, name="Home"),
    path('shorten', views.generate_short_url, name="GenerateShortUrl"),
    path('<str:hash_id>/', views.expand_short_url, name="ExpandShortUrl"),

]