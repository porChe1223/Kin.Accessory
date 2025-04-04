from django.shortcuts import render, get_object_or_404
from .models import Product


def show_shop(request):
    """""""""""""""""""""""""""""""""""
    Productクラスの全データをHTMLに送信
    """""""""""""""""""""""""""""""""""
    products = Product.objects.all()

    return render(request, 'shop/show_shop.html', {'products': products})


def product_detail(request, pk):
    """""""""""""""""""""""""""""""""
    Productクラスの単体をHTMLに送信
    """""""""""""""""""""""""""""""""
    product = get_object_or_404(Product, pk=pk)
    
    return render(request, 'shop/product_detail.html', {"product": product})

