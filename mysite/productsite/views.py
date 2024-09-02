from django.shortcuts import render
from django.http import HttpResponse
from .models import Products

# Create your views here.

def home(request):
    return HttpResponse("Hello, welcome to our product page!")

def product_view(request):
    products = Products.objects.all()  # Fetch products from database
    return render(request, 'productsite/products.html', {'products': products})
