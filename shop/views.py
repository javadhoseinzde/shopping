from django.db import models
from django.shortcuts import get_object_or_404, redirect, render
from .models import Category, Item

def home(request):
	context = {
		'products' : Item.objects.all(),
		'category' : Category.objects.filter(status=True)
	}
	return render(request, 'home.html', context)


def detail(request, slug):
    product = get_object_or_404(Item,slug=slug)

    return render(request,
                  'detail.html',
                  {'product': product})

def category(request, slug):
	context ={ 
		'category': get_object_or_404(Category, status=True, slug=slug)
	}
	return render(request, 'category_list.html', context)


