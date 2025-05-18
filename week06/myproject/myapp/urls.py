# /myproject/myapp/urls.py
from django.urls import path
from .views import (
    home, BikeListView, BikeDetailView, RentBikeView,dashboard,
    BikeListCreateAPIView, BikeRetrieveUpdateAPIView,
)

urlpatterns = [
    # Existing frontend URLs
    path('', home, name='home'),
    path('bikes/', BikeListView.as_view(), name='bike_list'),
    path('bikes/<int:pk>/', BikeDetailView.as_view(), name='bike_detail'),
    path('bikes/<int:pk>/rent/', RentBikeView.as_view(), name='rent_bike'),
    path('dashboard/', dashboard, name='dashboard'),
    # API URLs
    path('api/bikes/', BikeListCreateAPIView.as_view(), name='bike_api_list_create'),
    path('api/bikes/<int:pk>/', BikeRetrieveUpdateAPIView.as_view(), name='bike_api_retrieve_update'),
]