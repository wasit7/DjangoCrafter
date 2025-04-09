from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Bike
from django.db.models import Q  # For complex queries

# Home Page (FBV)
def home(request):
    return render(request, 'myapp/home.html')

#  (CBV)
class BikeListView(ListView):
    model = Bike
    template_name = 'myapp/bike_list.html'
    context_object_name = 'bikes'  # Name of the variable in the template
    
    def get_queryset(self):
        queryset = super().get_queryset()  # Get the default queryset (all bikes)
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