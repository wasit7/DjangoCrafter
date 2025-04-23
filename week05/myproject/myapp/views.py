from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Bike, Rental
from django.db.models import Q  # For complex queries
from .forms import RentalForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import generics
from .serializers import BikeSerializer

# Home Page (FBV)
def home(request):
    return render(request, 'myapp/home.html')

#  (CBV)
class BikeListView(ListView):
    model = Bike
    template_name = 'myapp/bike_list.html'
    context_object_name = 'bikes'  # Name of the variable in the template
    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-hourly_rate')  # Get the default queryset (all bikes)
        query = self.request.GET.get('q')  # Get the search term from the URL (e.g., ?q=mountain)
        if query:
            # Filter bikes where name or description contains the query (case-insensitive)
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        return queryset

# Bike Detail (CBV: DetailView)
class BikeDetailView(DetailView):
    model = Bike
    template_name = 'myapp/bike_detail.html'
    context_object_name = 'bike'  # Name of the variable in the template

class RentBikeView(LoginRequiredMixin, CreateView):
    model = Rental
    form_class = RentalForm
    template_name = 'myapp/rent_bike.html'
    success_url = reverse_lazy('bike_list')  # Redirect after successful rental

    def form_valid(self, form):
        # Set the user and bike before saving
        form.instance.user = self.request.user
        form.instance.bike = Bike.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bike'] = Bike.objects.get(pk=self.kwargs['pk'])
        return context
    
# New API Views
class BikeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer

class BikeRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer