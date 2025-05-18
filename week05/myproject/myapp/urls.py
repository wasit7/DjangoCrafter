# /myproject/myapp/urls.py
from django.urls import path
from .views import home, BikeListView, BikeDetailView

urlpatterns = [
    path('', home, name='home'),  # Home page at root URL
    path('bikes/', BikeListView.as_view(), name='bike_list'),
    path('bikes/<int:pk>/', BikeDetailView.as_view(), name='bike_detail'),
]