from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.base import Model
from shop.models import Item,OrderItem, Order, UserProfile
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import redirect
import logging
from django.urls import reverse
from django.http import HttpResponse, Http404
from zeep import Client
from django.contrib.auth.models import User
from .forms import OrderDetailForm
import requests
import json




class OrderSummaryView(LoginRequiredMixin, View):
	def get(self, *args, **kwargs):
		try:
			order = Order.objects.get(user=self.request.user, ordered=False)
			return render(self.request, 'order_summary.html', context={'object':order})
		except ObjectDoesNotExist:
			messages.warning(self.request, "You do not have an active order")
			return redirect("shopping:home")


@login_required
def add_to_cart(request, slug):
	Prod = get_object_or_404(Item, slug=slug)
	order_item, created = OrderItem.objects.get_or_create(
		Prod = Prod,
		user = request.user,
		ordered=False
	)
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	if order_qs.exists():
		order = order_qs[0]
		if order.items.filter(Prod__slug=Prod.slug).exists():
			order_item.quantity += 1
			order_item.save()
			messages.info(request, "this item quantity was updated")
			return redirect("cart:order-summary")
		else:
			order.items.add(order_item)
			messages.info("this item was added to your cart.")
			return redirect("cart:order-summaty")
	else:
		ordered_date = timezone.now()
		order = Order.objects.create(
			user=request.user, ordered_date=ordered_date)
		order.items.add(order_item)
		messages.info(request, "this item was added to your cart.")
		return redirect("cart:order-summary")

@login_required
def remove_from_cart(request, slug):
	Prod = get_object_or_404(Item, slug=slug)
	order_qs = Order.objects.filter(
		user=request.user,
		ordered=False
	)
	if order_qs.exists():
		order = order_qs[0]
		if order.items.filter(Prod__slug=Prod.slug).exists():
			order_item = OrderItem.objects.filter(
				Prod=Prod,
				user=request.user,
				ordered=False
			)[0]
			order.items.remove(order_item)
			order_item.delete()
			messages.info(request, "this item was removed from your cart.")
			return redirect("cart:order-summary")
		else:
			messages.info(request, "this item was not in your cart")
			return redirect("shopping:detail", slug=slug)
	else:
		messages.info(request, "you do not have an active order")
		return redirect("shopping:detail", slug=slug)

@login_required
def remove_single_item_from_cart(request, slug):
	Prod = get_object_or_404(Item, slug=slug)
	order_qs = Order.objects.filter(
		user=request.user,
		ordered=False
	)
	if order_qs.exists():
		order = order_qs[0]
		if order.items.filter(Prod__slug=Prod.slug).exists():
			order_item = OrderItem.objects.filter(
				Prod=Prod,
				user=request.user,
				ordered=False
			)[0]
			if order_item.quantuty > 1:
				order_item.quantity -= 1
				order_item.save()
			else:
				order.items.remove(order_item)
			messages.info(request, "this item quantity was updated")
			return redirect("core:order-summary")
		else:
			messages.info(request, "this item was not in your cart")
			return redirect("core:order-summary")
	else:
		messages.info(request, "you do not have an active order")
		return redirect("shopping:detail", slug=slug)
		
@login_required
def OrderDetailView(request):
	Prod = get_object_or_404(Item)
	order_item, created = OrderItem.objects.get_or_create(
		Prod = Prod,
		user = request.user,
		ordered=False
	)
	order_qs = Order.objects.filter(user=request.user, ordered=False)
	try:
		if order_qs.exists():
			if request.method == 'POST':
				form = OrderDetailForm(request.POST)
				if form.is_valid():
					username_recive = form.cleaned_data['username_recive']
					phone_number = form.cleaned_data['phone_number']
					address = form.cleaned_data['address']
					code_posti = form.cleaned_data['code_posti']
			else:
				form = OrderDetailForm()
			return render(request, 'order_detail.html', {'form':form,})
	except ObjectDoesNotExist:
		messages.warning("sorry you're not order in your cart")
		return redirect("shopping:home")



'''

MERCHANT = 'KXSEFGHH-SWTV-WDGH-STYX-FHVRHJJSEWBX'
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
CallbackURL = 'http://localhost:8000/verify/' # Important: need to edit for realy server.
@login_required
def send_request(request, id):
	try:
		order = Order.objects.get(id=id, user=request.user)	
		amount = int(order.get_total()) #toman / required
		result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
		if result.Status == 100:
			return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
		else:
			return HttpResponse('Error code.' + str(result.Status))
	except Order.DoesNotExist:
		return HttpResponse("Order not found")
	except Exception as e:
		print(e)
		return HttpResponse('Server error')
@login_required
def verify(request): 
	order = Order.objects.get(id=id, user=request.user)	
	amount = int(order.get_total()) #toman / required
	if request.GET.get('Status') == 'OK':
		result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
		if result.Status == 100:
			Order.ordered = True
			return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))
		elif result.Status == 101:
			return HttpResponse('Transaction submitted : ' + str(result.Status))
		else:
			return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))
	else:
		return HttpResponse('Transaction failed or canceled by user') 

'''