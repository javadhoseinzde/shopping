from django.db import models
from django.shortcuts import get_object_or_404, redirect, render
from .models import Category, Item
from comments.models import Comment
from comments.forms import CommentForm
from django.urls import reverse

def home(request):
	context = {
		'products' : Item.objects.all(),
		'category' : Category.objects.filter(status=True)
	}
	return render(request, 'home.html', context)


def detail(request, slug):
	product = get_object_or_404(Item,slug=slug)
	comments = Comment.objects.all()
	new_comment = None
	# Comment posted
	if request.method == 'POST':
		comment_form = CommentForm(request.POST)
		if comment_form.is_valid():
			comment_form.instance.user = request.user
			new_comment = comment_form.save(commit=False)

			new_comment.item = product
			new_comment.save()
			return redirect(reverse('shopping:detail', kwargs={"slug": product.slug}))
	else:
		comment_form = CommentForm()
	return render(request,'detail.html',{'product': product,'comments':comments,'comment_form':comment_form,})

def category(request, slug):
	context ={ 
		'category': get_object_or_404(Category, status=True, slug=slug)
	}
	return render(request, 'category_list.html', context)


