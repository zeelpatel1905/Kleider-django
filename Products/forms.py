from django.forms import ModelForm
from .models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'gender', 'condition', 'category', 'occasion', 'featured', 'image1', 'image2', 'image3', 'image4']