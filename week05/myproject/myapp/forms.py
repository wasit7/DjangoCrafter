# /myproject/myapp/forms.py
from django import forms
from .models import Rental

class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = []  # No fields needed in the form; user and bike are set programmatically