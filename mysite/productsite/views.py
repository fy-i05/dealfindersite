from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Products, Category


def home(request):
    return HttpResponse("Hello, welcome to our product page!")

def product_view(request):
    products = Products.objects.all()  #gets products from database
    categories= Category.objects.all()
    #print(categories)
    return render(request, 'productsite/products.html', {'products': products, 'categories': categories})

def products_by_category(request):
    category_id = request.GET.get('category_id')
    if not category_id:
        return JsonResponse({'error': 'Category ID is required'}, status=400)

    try:
        category = Category.objects.get(id=category_id)
        products = Products.objects.filter(category=category).values('id', 'name', 'image', 'link') 
        return JsonResponse({'products': list(products)}, safe=False)
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Category does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
