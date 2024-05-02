from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'weight_quantity', 'image', 'categories', 'digital', 'stock']
        # Exclude the farmer field from the form
        exclude = ['farmer']
