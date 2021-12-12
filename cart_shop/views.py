from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from shop.models import Item,OrderItem, Order, UserProfile
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import redirect



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
		if order.items.filter(item__slug=Item.slug).exists():
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
		if order.items.filter(item__slug=Item.slug).exists():
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


'''
@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("cart:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("cart:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("cart:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("cart:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("cart:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("cart:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("cart:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("cart:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("cart:product", slug=slug)
'''